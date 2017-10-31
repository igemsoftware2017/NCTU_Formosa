import time, DAN, requests, random
from sql_io import *
import sqlite3 as sql
import numpy as np
import datetime

ServerIP = '140.113.199.199' #Change to your IoTtalk IP or None for autoSearching
Reg_addr=None # if None, Reg_addr = MAC address
# feature_in : input feature;feature_tmp;feature_out;feature_day
DAN.profile['dm_name']='Data_model'
DAN.profile['df_list']=feature_in+['Model_out']
DAN.profile['d_name']= None # None for autoNaming
DAN.device_registration_with_retry(ServerIP, Reg_addr)
# make sql database
tmp_sql_name="Tmp_data.db"
day_sql_name="Day_data.db"
ini_Tmp = None
last_time_str=''
set_time_f = '%H:%M'
#set model time
set_time = '01:00'
reset_time = '10:00'
out_flag = 0

#Set predict model
import tensorflow as tf
import tensorlayer as tl

n_feature = 11 #11FEATURE
Feature_list = ['StnPres_Mean','StnPres_Max','StnPres_Min','T_Mean','T_Max','T_Min','RH_Mean','RH_Min','Precp_Mean','Tc','T_cd']
n_steps = 14
Model_name = 'cnn_82.npz'
config = tf.ConfigProto()
config.gpu_options.allocator_type = 'BFC'
sess=tf.InteractiveSession(config=config)
#data process
ALL_std=[13.637058,21.102041,13.888361,4.590726,5.135409,4.681896,
8.672514,12.812692,15.377318,3.014554,1.355240]
ALL_mean=[
1000.861722,1003.132525,998.901895,22.525746,27.146857,
19.232888,79.269329,61.696226,4.574348,7.913970,1.394389]
# data numpy array
def process_data(data):
    print('start processing')
    for _ in range(0,11):
        print(_)
        data[:,_] = (data[:,_]-ALL_mean[_])/ALL_std[_]
    return data

#read data
def predict_run(sess,network,x_predict,x,y_op):
    x_predict = x_predict.reshape((-1,n_steps,n_feature))
    pred_out = tl.utils.predict(sess, network,x_predict,x, y_op,None)
    pred_out = pred_out.reshape((-1,2))
    pred_out = pred_out[:,1]
    pred_out = pred_out.reshape((-1))
    return pred_out.tolist()
#transform data
def trans_data(data,sort_list=None):
    print('Start converting data')
    if sort_list:
        out_array=None
        first = 0
        for key in sort_list:
            print('key : %s processing Len : %d'%(key,len(data[key])))
            features = np.array([float(n) for n in data[key]],dtype=np.float32)
            print(features)
            if first==0:
                out_array = features
                first = 1
            else:
                out_array = np.vstack([out_array,features])
        return out_array.T
    else:
        return data

###Model Structure###
x = tf.placeholder("float32", [None, n_steps, n_feature])
y_ = tf.placeholder("int64", [None,])
#create network:set hidden cell
c_hidden=256
nn_hidden=128

network=tl.layers.InputLayer(x,name='input_layer')
network=tl.layers.ReshapeLayer(network,shape=[-1,n_steps,1,n_feature],name='reshape_1')
network=tl.layers.Conv2dLayer(layer=network, act=tf.nn.relu, shape=[5, 1, n_feature,c_hidden], strides=[1, 1, 1, 1]
                              , padding='SAME', name='cnn_layer')
network=tl.layers.MaxPool2d(network, filter_size=(5, 1),strides=(2,1), padding='VALID', name='maxpool')
network = tl.layers.FlattenLayer(network,name='flatten')
def add_dense(network,number,hidden):
    for n in range(number):
        network = tl.layers.DropoutLayer(network,keep=0.5,name='dropout%d'%(n))
        network = tl.layers.DenseLayer(network,n_units=hidden,act = tf.nn.relu,name='dense%d'%(n))
    return network
network = add_dense(network,number=4,hidden=nn_hidden)
network = tl.layers.DropoutLayer(network,keep=0.5,name='dropout_f')
network = tl.layers.DenseLayer(network,n_units=2,act = tf.identity,name='output')
y = network.outputs
cost = tl.cost.cross_entropy(y,y_,name='loss')
l2=0
for w in network.all_params:
    l2 += tf.contrib.layers.l2_regularizer(2e-3)(w)
cost += l2
# the accuracy of model
correct_prediction = tf.equal(tf.argmax(y, 1),y_)
acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
y_op = tf.nn.softmax(y,-1)
#Initialize
tl.layers.initialize_global_variables(sess)
#read the model
params=tl.files.load_npz(name=Model_name)
tl.files.assign_params(sess, params, network)

try:
    print('Loop start')
    tmp_sql = sql.connect(tmp_sql_name)
    tmp_c = tmp_sql.cursor()
    day_sql = sql.connect(day_sql_name)
    day_c = day_sql.cursor()
    tmp_name = make_table(tmp_sql,tmp_c,"tmp_test",feature_tmp)
    day_name = make_table(day_sql,day_c,"day_test",feature_day)
    while True:
        
        now = datetime.datetime.now()
        now_str = now.strftime(set_time_f)
        tomorrow = now-datetime.timedelta(1)
        out_dic = None
        try:
            #Pull data get data from iot talk，and save to tmp
            feature_in_dic={}
            for feature in feature_in:
                value=DAN.pull(feature)
                if not value :break
                if value[0] != value[0]:
                    print('find nan')
                    break
                feature_in_dic[feature] = float(value[0])
            else:
                pull2tmpsql(tmp_sql,tmp_c,tmp_name,feature_in_dic)
            
            if feature_in_dic : print(feature_in_dic)
            #when reach time , save data to day sql
            if now_str == set_time and out_flag==0:
                print('start send info')
                day_dic = tmpsql2dic(tmp_sql,tmp_c,tmp_name,tomorrow)
                out_flag=1
                if day_dic:
                    writer(day_sql,day_c,day_name,day_dic)
                #output dic
                out_dic = daysql2dic(day_sql,day_c,day_name,now,delta=14)
            
            #Push data to a device feature called "acc_data" push to sent out data
            if out_dic:
                #print(out_dic)
                x_data = trans_data(out_dic,Feature_list)
                #print(x_data)
                x_predict = process_data(x_data)   #process
                print(x_predict)
                y_predict = predict_run(sess,network,x_predict,x,y_op)
                #print(y_predict)
                #Push data to a device feature called "Dummy_Sensor" push sent out data
                value_out=y_predict[0]
                print('Probability : %f'%(value_out))
                DAN.push ('Model_out', value_out)
            if now_str == reset_time and out_flag==1:
                out_flag=0
                print('out_flag : %d'%(out_flag))

        except Exception as e:
            print(e)
            DAN.device_registration_with_retry(ServerIP, Reg_addr)
        #record time
        last_time_str = now
        time.sleep(1.0)

except Exception as e:
    print(e)

finally:
    tmp_sql.close()
    day_sql.close()

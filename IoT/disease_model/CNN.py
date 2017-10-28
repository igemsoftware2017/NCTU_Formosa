import numpy   as np
from optparse import OptionParser #markliou
import tensorflow as tf
import tensorlayer as tl
import read_csv

cmdparser = OptionParser()
cmdparser.add_option("-f", "--file", action="store", dest="filename", default=0, help="input a training data filename")
cmdparser.add_option("-t", "--test", action="store", dest="testname", default=0, help="input a testing data filename")
cmdparser.add_option("-s", "--save", action="store", dest="save", default=0, help="input a saving model name")
cmdparser.add_option("-l", "--learning_rate", action="store", dest="learning_rate", default=0.001, help="input a learning rate")
cmdparser.add_option("-b", "--batch_size", action="store", dest="batch", default=128, help="input a batch size")
cmdparser.add_option("-e", "--epoch", action="store", dest="epoch", default=200, help="input a epoch")
cmdparser.add_option("-d", "--days", action="store", dest="days", default=14, help="input days you want to read")
cmdparser.add_option("-m", "--model", action="store", dest="model", default=None, help="input model to retrain ?")
cmdparser.add_option("-g", "--graph", action="store_true", dest="graph", default=False, help="using tensorboard")
(options, args) = cmdparser.parse_args()
if(options.filename == 0):
    print ("  the input filename is not specified!! Please use -f or --file option...")
    exit(" For more information, use -h or --help")
if(options.testname == 0):
    print ("  the input testname is not specified!! Please use -t or --test option...")
    exit(" For more information, use -h or --help")
if(options.save == 0):
    print ("  can not find save name...")
    exit(" For more information, use -h or --help")

filename = options.filename
testname = options.testname
save_name=options.save
model_name = options.model
learning_rate = float(options.learning_rate)

n_feature = 11 # 11 features
n_steps = int(options.days) # rnn read days
Batch = int(options.batch)
config = tf.ConfigProto()
config.gpu_options.allocator_type = 'BFC'
sess=tf.InteractiveSession(config=config)

##Read the training data
x_train,y_train,_ = read_csv.read_data(filename,n_steps,n_feature)
x_train = x_train.reshape((-1,n_steps,n_feature))
#print(x_train[:5,:,:])
x_test,y_test,_ = read_csv.read_data(testname,n_steps,n_feature)
x_test = x_test.reshape((-1,n_steps,n_feature))

###Model Structure###
#time sequnce features
x = tf.placeholder("float32", [None, n_steps, n_feature])
#label
y_ = tf.placeholder("int64", [None,])

#create network
c_hidden=256
lstm_hidden=512
nn_hidden=128

#network layer
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
    l2 += tf.contrib.layers.l2_regularizer(3e-3)(w)
cost += l2

train_params = network.all_params
train_op = tf.train.AdamOptimizer(learning_rate=learning_rate, beta1=0.9, beta2=0.999,
                            epsilon=0.001, use_locking=False).minimize(cost, var_list=train_params)

# count accuracy
correct_prediction = tf.equal(tf.argmax(y, 1),y_)
acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

#initialize
tl.layers.initialize_global_variables(sess)

if model_name:
    params=tl.files.load_npz(name=model_name)
    tl.files.assign_params(sess, params, network)
network.print_layers()
#training
tl.utils.fit(sess, network, train_op, cost, x_train, y_train, x, y_,
            acc=acc, batch_size=Batch, n_epoch=int(options.epoch), print_freq=5,X_val=x_test, y_val=y_test,
            eval_train=True,tensorboard=options.graph, tensorboard_epoch_freq=5)

# evaluate model
tl.utils.test(sess, network, acc, x_test, y_test, x, y_, batch_size=Batch, cost=cost)
#save model
tl.files.save_npz(network.all_params , name=save_name+'.npz')
sess.close()

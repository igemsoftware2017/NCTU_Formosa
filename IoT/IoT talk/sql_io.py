import sqlite3 as sql
import json_io
import numpy as np
import math
import datetime
feature_in = ['StnPress','Temp','RH_in','Precp_in']
feature_tmp = feature_in+['Time']
feature_out = ['StnPres_Mean','StnPres_Max','StnPres_Min','T_Mean','T_Max','T_Min','RH_Mean','RH_Min','Precp_Mean','Tc','T_cd']
feature_day = ['StnPres_Mean','StnPres_Max','StnPres_Min','T_Mean','T_Max'
                ,'T_Min','RH_Mean','RH_Min','Precp_Mean','Tc','T_cd','Date']
day_fmt = '%Y-%m-%d'
time_fmt = '%Y-%m-%d %H:%M:%S'
# 昨天溫度
global ini_Tmp
ini_Tmp = None
#時間相關
query = "select %s from '%s' where Date between '%s' and '%s'"
def get_time():
    now = datetime.datetime.now()
    now = now.strftime(time_fmt)
    return now
    
def readfrom_sql(mydb,cursor,cmd,listed=False):

    result=cursor.execute(cmd)
    mydb.commit()
    if listed:
        result = [n for n in result]
    else:
        result = (n for n in result)
    return result

def writer(mydb,c,table_name,dictionary):
    try:
        ctitle = []
        ccontent = []
        for item in dictionary.items():
            ctitle.append(str(item[0]))
            ccontent.append(str(item[1]))

        title = '("'+'", "'.join(ctitle)+'")'
        content = '("'+'", "'.join(ccontent)+'")'
        c.execute('insert into ' + table_name +' ' + title + ' values ' + content)
        mydb.commit()
    except Exception as e:
        print(e)
        
def make_table(mydb,c,table_name,feature_list):
    # feature dic 是字典 feature : type
    #feature_list = sorted(feature_dic)
    table_feature = "'%s'"%("','".join(feature_list))
    try:
        c.execute('create table '+table_name+' ('+table_feature+')')
        mydb.commit()
    except:
        print('table exist')
    return table_name

def pull2tmpsql(mydb,c,table_name,fearture_dic): #不包含時間
    # 加入時間 ******
    fearture_dic['Time'] = get_time()
    #寫入sql
    writer(mydb,c,table_name,fearture_dic)
    
def tmpsql2dic(db,c,table_name,date):
    # cmd 取前一日,用feature_tmp
    global ini_Tmp
    day_query = date.strftime(day_fmt)+'%'
    cmd = "SELECT %s from '%s' where Time LIKE '%s'"%(",".join(feature_in),table_name,day_query)
    print(cmd)
    data = np.array(readfrom_sql(db,c,cmd,listed=True),dtype=np.float32).T.tolist()
    print(data)
    if data==[]:
        return None
    data_dic = {feature_in[i]:data[i] for i in range(len(feature_in))}
    out_dic = {'StnPres_Mean':sum(data_dic['StnPress'])/len(data_dic['StnPress'])
    ,'StnPres_Max':max(data_dic['StnPress'])
    ,'StnPres_Min':min(data_dic['StnPress'])
    ,'T_Mean':sum(data_dic['Temp'])/len(data_dic['Temp'])
    ,'T_Max':max(data_dic['Temp'])
    ,'T_Min':min(data_dic['Temp'])
    ,'RH_Mean':sum(data_dic['RH_in'])/len(data_dic['RH_in'])
    ,'RH_Min':min(data_dic['RH_in'])
    ,'Precp_Mean':max(data_dic['Precp_in'])
    ,'Tc':max(data_dic['Temp'])-min(data_dic['Temp'])
    #,'T cd':math
    }
    if ini_Tmp==None:
        out_dic['T_cd'] = 1.394389
    else:
        out_dic['T_cd'] = math.abs(out_dic['T_Mean']-ini_Tmp)
    ini_Tmp = out_dic['T_Mean']
    out_dic['Date'] = day_query
    return out_dic
def daysql2dic(db,c,table_name,date,delta=14): #ok
    # cmd 取14日，用feature_day
    today = date-datetime.timedelta(1) #前一日
    start_date = today - datetime.timedelta(delta-1)
    cmd = query % (",".join(feature_out),table_name, start_date.strftime(day_fmt),today.strftime(day_fmt))
    data = np.array(readfrom_sql(db,c,cmd,listed=True),dtype=np.float32).T.tolist()
    print(len(data[0]))
    if len(data[0])<delta:
        return None
    push_dic = {feature_out[i]:data[i] for i in range(len(feature_out))}
    return push_dic
    
if __name__ == "__main__":
    db = sql.connect('test.db')
    c = db.cursor()
    date = datetime.datetime.strptime("2011-10-04", "%Y-%m-%d")
    #f = tmpsql2dic(db,c,"tmp_test",date)
    #print(f)
    make_table(db,c,"test_tmp",feature_tmp)
    make_table(db,c,"test_day",feature_day)
    dic={}
    for n in feature_in:
        dic[n]=1
    print(dic)
    pull2tmpsql(db,c,"test_tmp",dic)

import pandas as pd
import numpy as np
import random
def split_data(name='process_data.csv'):
    data = pd.read_csv(name).drop(['Unnamed: 0','Unnamed: 0.1'],1)
    data.dropna(axis=0)
    #data.sample(frac=1)
    #print(len(data.index))
    long = int(len(data.index)/3)
    train = data.iloc[long:,:]
    test = data.iloc[:long,:]
    return train,test
#train,test = split_data('process_data2.csv')
#train.to_csv('train.csv')
#test.to_csv('test.csv')
def read_data(name,days,feature):
    data = pd.read_csv(name).dropna(axis=0)
    x = np.array(data.iloc[:,2:days*feature+2].values,dtype=np.float32)
    z = np.array(data.iloc[:,days*feature+2:].values,dtype=np.float32)
    #print(z.shape)
    #print(data.iloc[:,2:days*feature+2].head())
    #print(data.iloc[:,days*feature+2:].head())
    y = np.array(data['label'].values,dtype=np.float32)
    return x,y,z
    
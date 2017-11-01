import math
from optparse import OptionParser #markliou
# usr option method  markliou
cmdparser = OptionParser()
cmdparser.add_option("-f" , "--file", action="store", dest="filename", default=0, help="input a training data filename")
cmdparser.add_option("-g", "--gap", action="store", dest="gap", default=0, help="gap number, default is 0")
cmdparser.add_option("-t", "--test", action="store", dest="filenamet", default=0, help="input a testing data filename")
cmdparser.add_option("-s", "--score", action="store", dest="scorename", default=0, help="input a scorecard data filename")
cmdparser.add_option("-V", "--W1", action="store", dest="w1", default=0.9, help="Weight 1 AUC, default is 0.9")
cmdparser.add_option("-W", "--W2", action="store", dest="w2", default=0.1, help="Weight 2 Correlation, default is 0.1")
cmdparser.add_option("-v", "--cvfold", action="store", dest="nfold", default=10, help="cross validation fold, default is 10")
(options, args) = cmdparser.parse_args()
if(options.filename == 0):
    print ("  the input filename is not specified!! Please use -f or --file option...")
    exit(" For more information, use -h or --help")
if(options.filenamet == 0):
    print ("  the input test is not specified!! Please use -t or --test option...")
    exit(" For more information, use -h or --help")
if(options.scorename == 0):
    print ("  the input scorecard is not specified!! Please use -s or --score option...")
    exit(" For more information, use -h or --help")
#all key to zero
filename3 = options.filename
filename1 = options.filenamet
scorename = options.scorename
gap = int(options.gap)
W1 = float(options.w1)
W2 = float(options.w2)
nfold = int(options.nfold)
# aalist and dipep
aalist= ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
dipep = [x1+x2 for x1 in aalist for x2 in aalist]
boundMAX = 1000
boundMIN = 0
length = 400 
#========== Load Traing Data ====================
v1= open(filename3)
samplelist= [n.strip('\n').split('\t') for n in v1.readlines()]
v1.close()
### some function
#initialize dic to all 0
def ini_dic(dic=None,key_list=None):
    if key_list:
        return {k:0 for k in key_list }
    elif dic:
        return {k:0 for k in dic.keys() }
    else:
        return None
#count the aa score
def count_aa_score(scorecard):
    avg_aa_score = [0]*20
    k=0;
    for i in range(400):
        if (k == 20):
            k=0
        avg_aa_score[k] += float(scorecard[i])
        avg_aa_score[int(i/20)] += float(scorecard[i])
        k = k+1
    for i in range(20):
        avg_aa_score[i] = avg_aa_score[i]/40
    return avg_aa_score
#calculate average
def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)
#calculate corr
def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff
    return diffprod / math.sqrt(xdiff2 * ydiff2)
#read scoring card by filename
def make_sc(scorecard):
    f3 = open(scorecard)
    count = 0
    tmpscore = []
    for line in f3.readlines():
        if count==3:
            tmpscore1 = line.strip('\n').split('[')
            tmpscore2 = tmpscore1[1].strip(']').split(',')
            for tmpval in tmpscore2:
                tmpscore.append(float(tmpval))
        count = count + 1
    f3.close()
    return tmpscore
#Read Score List
tmpscore = make_sc(scorename)
#Read Score dic
scoring= {dipep[i] : tmpscore[i] for i in range(len(dipep))}

#make ts_file
sco= []
x= 0.0
dipep_test = ini_dic(key_list=dipep)
ts_file= []
index = 1
indexl = []
for line in samplelist:
    assert len(line)==2
    seq = line[0]
    clas = line[1]
    dipep_test = ini_dic(dipep_test)
    for aa in range(0, len(seq)-(gap+1)):  
        tempaa= seq[aa]+seq[aa+(gap+1)]
        dipep_test[tempaa] += 1
    gg=0.0
    for x6 in dipep:
        gg += float((scoring[x6])*dipep_test[x6])
        
    ts_file.append([gg/(len(seq)-(gap+1)),clas])
    indexl.append(index % nfold)
    index = index + 1

# K-fold Cross to test training set
auc_score = 0
kfoldacc = 0
for i in range(nfold):
    test = []
    train = []
    count = 0
    for selectedIndex in ts_file:
        if indexl[count] == i:
            test.append(ts_file[count])
        else:
            train.append(ts_file[count])
        count = count + 1
    for everysample in train:
        sco.append(everysample[0])
    TPRl=[]
    FPRl=[]
    x= min(sco)
    max_s = max(sco)
    maxacc = -1
    while x<= max_s:
        thre= x
        TP=0.000001
        FP=0.000001
        TN=0.000001
        FN=0.000001
        TPR= 0.000001
        FPR= 0.000001
        for everysample in test:
            ss= everysample[0]
            clas= everysample[1]
        
            if ss> thre:
                clas2= "1"
            else:
                clas2= "0"
            if clas== "1" and clas2== "1":
                TP+= 1
            elif clas== "1" and clas2== "0":
                FN+= 1
            elif clas== "0" and clas2== "1":
                FP+= 1
            elif clas== "0" and clas2== "0":
                TN+= 1
        TPR= TP/(TP+FN)
        FPR= FP/(FP+TN)
        TPRl.append(TPR)
        FPRl.append(FPR)
        acc = (TP+TN)/(TP+FP+TN+FN)
        if (acc > maxacc):
            maxacc = acc
        x= x+1
    ARC=0.0
    area=0.0
    high=0.0
    bottom=0.0
    for pp in range(0, len(TPRl)-2):
        high= float(FPRl[pp])-float(FPRl[pp+1])
        bottom= float(TPRl[pp])+float(TPRl[pp+1])
        area= float(bottom*high)/2.0
        ARC+= area
    auc_score = auc_score+ARC
    kfoldacc = kfoldacc + maxacc        
auc_score = (auc_score/nfold)
kfoldacc = (kfoldacc/nfold)

#full train accuracy
totalACC = 0
for everysample in ts_file:
    sco.append(everysample[0])
maxACC = 0
maxTHE = 0
x= min(sco)
while x<= max(sco):
    thre= x
    TP=0.000001
    FP=0.000001
    TN=0.000001
    FN=0.000001
    for everysample in ts_file:
        ss= everysample[0]
        clas= everysample[1]
        if ss> thre:
            clas2= "1"
        else:
            clas2= "0"
        if clas== "1" and clas2== "1":
            TP+= 1
        elif clas== "1" and clas2== "0":
            FN+= 1
        elif clas== "0" and clas2== "1":
            FP+= 1
        elif clas== "0" and clas2== "0":
            TN+= 1
    ACC= ((TP+TN)/len(train))*100
    if ACC >= maxACC:
        maxACC = ACC
        maxTHE = thre
    x= x+1

#Load Test Data
v1= open(filename1)
samplelist= [n.strip('\n').split('\t') for n in v1.readlines()]
v1.close()

#Testing
boundMAX = 1000
boundMIN = 0
length = 400
sco= []
x= 0.0
dipep_test= ini_dic(key_list=dipep)
ts_file= []
#read samplelist
for line in samplelist:
    seq = line[0]
    clas = line[1]
    
    dipep_test= ini_dic(key_list=dipep)
    for aa in range(0, len(seq)-(gap+1)):  
        tempaa= seq[aa]+seq[aa+(gap+1)]
        dipep_test[tempaa] += 1
    gg=0.0
    for x6 in dipep:
        gg+= float((scoring[x6])*dipep_test[x6])
        
    ts_file.append([gg/(len(seq)-(gap+1)),clas])
#calculate full test accuracy
totalACC = 0
test = ts_file
thre= maxTHE
TP=0.000001
FP=0.000001
TN=0.000001
FN=0.000001
for everysample in test:
    ss= everysample[0]
    clas= everysample[1]
    if ss> thre:
        clas2= "1"
    else:
        clas2= "0"
    if clas== "1" and clas2== "1":
        TP+= 1
    elif clas== "1" and clas2== "0":
        FN+= 1
    elif clas== "0" and clas2== "1":
        FP+= 1
    elif clas== "0" and clas2== "0":
        TN+= 1
        
totalACC = (((TP+TN)/len(test))*100)

print ("\n---------- Result ----------")
print ("FullTrain_acc="+str(maxACC))
print ("CV acc(train)="+str(kfoldacc*100))
print ("CV auc(train)="+str(auc_score*100))
print ("Theshold="+str(thre))
print ("Test_acc="+str(totalACC))
print ("Sensitivity="+str(TP/(TP+FN)))
print ("Specitivity="+str(TN/(TN+FP))+"\n")

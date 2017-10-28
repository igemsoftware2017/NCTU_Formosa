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

def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

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


filename3= options.filename
filename1= options.filenamet
filename2= options.scorename
gap = int(options.gap)
W1 = float(options.w1)
W2 = float(options.w2)
f1= open(filename1)
f2= open("dipep");
f3 = open(filename2)
nfold = int(options.nfold)

#========== Load Traing Data ====================
v1= open(filename3)
samplelist= v1.readlines()
v1.close()

#========== Original Score =================
aalist= ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
dipep_0= {}
for x1 in aalist:
    for x2 in aalist:
        dipep_0[x1+x2]= 0
dipep_1= {}
for x1 in aalist:
    for x2 in aalist:
        dipep_1[x1+x2]= 0

sodipep_0=[n for n in dipep_0.keys()]
sodipep_0.sort()
sodipep_1= [n for n in dipep_1.keys()]
sodipep_1.sort()
f = {}
for tmp in range(1):
    k = 0
    samplelistsub = []
    
    for x1 in aalist:
        for x2 in aalist:
            dipep_0[x1+x2]= 0
    
    for x1 in aalist:
        for x2 in aalist:
            dipep_1[x1+x2]= 0
    
    for line in samplelist:
        if (tmp==k%1):
            samplelistsub.append(line)
        k = k+1
    
    for line in samplelistsub:       
        tmpp = line.split('\t')
        seq= tmpp[0]
        tmpp = tmpp[1].split('\n')
        tmpp = tmpp[0]
        clas = tmpp[0:1]
        #print seq
        if int(clas)==0:
            for aa in range(0, len(seq)-(gap+1)):
                tempaa=seq[aa]+seq[aa+(gap+1)]
                dipep_0[tempaa]= int(dipep_0[tempaa])+1
                #print tempaa

        elif int(clas)==1:
            for aa in range(0, len(seq)-(gap+1)):
                tempaa=seq[aa]+seq[aa+(gap+1)]
                dipep_1[tempaa]= int(dipep_1[tempaa])+1

    y=0
    for x3 in sodipep_0:
        y= y+dipep_0[x3]
           

    z=0
    for x4 in sodipep_1:
        z= z+dipep_1[x4]

    scoring = []
    so_scoring= []
    for x5 in sodipep_0:
        eachscore = float(((float(dipep_1[x5])/z)-(float(dipep_0[x5])/y))*1000)
        scoring.append(eachscore)
        so_scoring.append(eachscore)
    
    so_scoring.sort()
    new_scoring= []
    for i in scoring:
        n= (i-so_scoring[0])/(so_scoring[-1]-so_scoring[0])*1000
        new_scoring.append(round(n))
    
    f[tmp] = new_scoring

    avg_aa_score = [0 for i in range(20)]
    k=0;
    for i in range(400):
        if (k == 20):
           k=0
        avg_aa_score[k] = avg_aa_score[k] + f[0][i]
        avg_aa_score[int(i/20)] = avg_aa_score[int(i/20)] + f[0][i] 
        k = k+1
        
    for i in range(20):
        avg_aa_score[i] = avg_aa_score[i]/40
      
    ori_dipep_score = f[0]


#========== Read Score Val ======================
count = 0
tmpscore = []
for line in f3.readlines():
    if count==2:
        tmpscore1 = line.split(':')
        bestfit = float(tmpscore1[1]);
        bestfit = bestfit/100;
    if count==3:
        tmpscore1 = line.split('[')
        tmpscore2 = tmpscore1[1].split(',')
        for tmpval in tmpscore2:
            t = tmpval.split(']');
            tmpscore.append(float(t[0]))
    count = count + 1

cur_aa_score = [0 for i in range(20)]
k=0
for i in range(400):
    if (k == 20):
        k=0
    cur_aa_score[k] = cur_aa_score[k] + tmpscore[i]
    cur_aa_score[int(i/20)] = cur_aa_score[int(i/20)] + tmpscore[i]
    k = k+1
for i in range(20):
    cur_aa_score[i] = cur_aa_score[i]/40    
#========== Read Score Key ======================
scoring= {}
count = 0
for line in f2:
    scoring[line[0:2]]= tmpscore[count];
    count = count+1

sosco_key= [n for n in scoring.keys()]
sosco_key.sort()

#========== Training =======================
boundMAX = 1000
boundMIN = 0
length = 400
sco= []
x= 0.0
dipep_test= {}
for x1 in sosco_key:
    dipep_test[x1]= 0
ts_scor_clas= []
ts_file= []
ts_pop= []

index = 1
indexl = []
for line in samplelist:
    tmp = line.split('\t')
    seq= tmp[0]
    tmp = tmp[1].split('\n')
    tmp = tmp[0]
    clas = tmp[0:1]
    for fea in dipep_test:
        dipep_test[fea]= 0
    
    for aa in range(0, len(seq)-(gap+1)):  
        tempaa= seq[aa]+seq[aa+(gap+1)]
        dipep_test[tempaa]= int(dipep_test[tempaa])+1
    gg=0.0
    for x6 in sosco_key:
        gg+= float((scoring[x6])*dipep_test[x6])
        
    ts_scor_clas.append(gg/(len(seq)-(gap+1))) 
    ts_scor_clas.append(clas)
    ts_file.append(ts_scor_clas)
    ts_scor_clas= [] 
    indexl.append(index % nfold)
    index = index + 1


###########################################################
# K-fold Cross Validation
totalACC = 0
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

    # Train to find Best Score
    for everysample in train:
        sco.append(everysample[0])
    sco.sort() 

    TPRl=[]
    FPRl=[]
    x= sco[0]
    maxacc = -1
    while x<= sco[len(sco)-1]:
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



###########################################################  
totalACC = 0
train = []
count = 0
for selectedIndex in ts_file:
    train.append(ts_file[count])
    count = count + 1

# Train to find Best Threshold
for everysample in train:
    sco.append(everysample[0])
sco.sort() 

maxACC = 0
maxTHE = 0
x= sco[0]
while x<= sco[len(sco)-1]:
    thre= x
    TP=0.000001
    FP=0.000001
    TN=0.000001
    FN=0.000001
    for everysample in train:
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


#========== Load Test Data ====================
v1= open(filename1)
samplelist= v1.readlines()
v1.close()

#========== Testing =======================
boundMAX = 1000
boundMIN = 0
length = 400
sco= []
x= 0.0
dipep_test= {}
for x1 in sosco_key:
    dipep_test[x1]= 0
ts_scor_clas= []
ts_file= []
ts_pop= []


for line in samplelist:
    tmp = line.split('\t')
    seq= tmp[0]
    tmp = tmp[1].split('\n')
    tmp = tmp[0]
    clas = tmp[0:1]
    for fea in dipep_test:
        dipep_test[fea]= 0
    
    for aa in range(0, len(seq)-(gap+1)):  
        tempaa= seq[aa]+seq[aa+(gap+1)]
        dipep_test[tempaa]= int(dipep_test[tempaa])+1
    gg=0.0
    for x6 in sosco_key:
        gg+= float((scoring[x6])*dipep_test[x6])
        
    ts_scor_clas.append(gg/(len(seq)-(gap+1))) 
    ts_scor_clas.append(clas)
    
    ts_file.append(ts_scor_clas)
    ts_scor_clas= [] 
    
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
MCC = ((TP*TN)-(FP*FN))/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

print ("\n---------- Result ----------")
print ("FullTrain_acc="+str(maxACC))
print ("CV acc(train)="+str(kfoldacc*100))
print ("CV auc(train)="+str(auc_score*100))
print ("Theshold="+str(thre))
print ("Test_acc="+str(totalACC))
print ("Sensitivity="+str(TP/(TP+FN)))
print ("Specitivity="+str(TN/(TN+FP))+"\n")

corr_pep = pearson_def(avg_aa_score,cur_aa_score)

auc = ((bestfit) - (W2*(corr_pep)))/W1;

f3.close()
f2.close()
f1.close()

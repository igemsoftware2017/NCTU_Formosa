
import genetic
import random
import math
from optparse import OptionParser #markliou
from multiprocessing import Pool
#============== Initial Population ====================#
# usr option method  markliou
######size=60######
cmdparser = OptionParser()
cmdparser.add_option("-f", "--file", action="store", dest="filename", default='example/istr', help="input a training data filename")
cmdparser.add_option("-g", "--gap", action="store", dest="gap", default=0, help="gap number, default is 0")
cmdparser.add_option("-v", "--cvfold", action="store", dest="nfold", default=10, help="cross validation fold, default is 10")
cmdparser.add_option("-G", "--Generation", action="store", dest="ngen", default=20, help="number of Generation, default is 20")
cmdparser.add_option("-V", "--Weight1", action="store", dest="w1", default=0.9, help="Weight 1 AUC, default is 0.9")
cmdparser.add_option("-W", "--Weight2", action="store", dest="w2", default=0.1, help="Weight 2 Correlation, default is 0.1")
cmdparser.add_option("-t", "--time", action="store", dest="time", default='0', help="time is a number to store time")
cmdparser.add_option("-s", "--scorecard", action="store", dest="scorecard", default='0', help="input scorecard name")

(options, args) = cmdparser.parse_args()
if(options.filename == 0):
    print ("  the input filename is not specified!! Please use -f or --file option...")
    exit(" For more information, use -h or --help")
if(options.time != '0' and options.scorecard == '0'):
    print ("  the input scorecard is not specified!! Please use -s")
    exit(" For more information, use -h or --help")
filename1 = options.filename
v1= open(filename1)
gap = int(options.gap)
nfold = int(options.nfold)
ngen = int(options.ngen)
W1 = float(options.w1)
W2 = float(options.w2)
time = int(options.time)
scorecard = options.scorecard


gen_score=[]
samplelist= v1.readlines()
v1.close()
f = {};
#####

aalist= ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
dipep_0= {}
dipep_1= {}
for x1 in aalist:
    for x2 in aalist:
        dipep_0[x1+x2]= 0
        dipep_1[x1+x2]= 0

sodipep_0= sorted(dipep_0.keys())
sodipep_1= sorted(dipep_1.keys())

for tmp in range(1):
    k = 0
    samplelistsub = []
    
    for x1 in aalist:
        for x2 in aalist:
            dipep_0[x1+x2]= 0
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
        eachscore = float(((float(dipep_0[x5])/y)-(float(dipep_1[x5])/z))*1000)
        scoring.append(eachscore)
        so_scoring.append(eachscore)
    
    so_scoring.sort()
    new_scoring= []
    for i in scoring:
        n= (i-so_scoring[0])/(so_scoring[-1]-so_scoring[0])*1000
        new_scoring.append(round(n))

    #f[0]=new_scoring
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
    #print (f[0])
    #print (avg_aa_score)
    
#========== k-Fold Cross Validation ====================
v1= open(filename1)
samplelist= [n.strip('\n').split('\t') for n in v1.readlines()]
v1.close()

###batch=samplelist
#read and make a scoring card
def make_sc(filename2):
    f3 = open(filename2)
    count = 0
    tmpscore = []
    for line in f3.readlines():
        if count==3:
            tmpscore1 = line.split('[')
            tmpscore2 = tmpscore1[1].split(',')
            for tmpval in tmpscore2:
                t = tmpval.split(']');
                tmpscore.append(float(t[0]))
        count = count + 1
    
    scoring= {}
    count = 0
    f2= open("dipep")
    
    for line in f2:
        scoring[line[0:2]]= tmpscore[count];
        count = count+1
    f2.close()
    sosco_key= [n for n in scoring.keys()]
    sosco_key.sort()
    
    return sosco_key,scoring,tmpscore

#========== cac_score ======================= (input seq output score)
def cuc_sc(seq,sosco_key,scoring):
    gap=0
    dipep_test= {}
    for x1 in sosco_key:
        dipep_test[x1]= 0
    
    for aa in range(0, len(seq)-(gap+1)):  
        tempaa= seq[aa]+seq[aa+(gap+1)]
        dipep_test[tempaa]= int(dipep_test[tempaa])+1
    # caculate score
    gg=0.0
    for x6 in sosco_key:
        gg+= float(scoring[x6]*dipep_test[x6])
    
    score = float(gg/(len(seq)-(gap+1)))
    
    return score

#=========== construct 400  names of dipeptide ==========
sosco_key= sorted(dipep_0.keys())


boundMAX = 1000
boundMIN = 0


def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)
#regularation
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

    
def p_evaluate(chromosome):
    sco= []
    x= 0.0
    dipep_test= {}
    for x1 in sosco_key:
        dipep_test[x1]= 0

    
    ts_scor_clas= []
    ts_file= []

    
    index = 1
    indexl = []
    
    #samplelist have all sample
    
    for line in samplelist:

        
        seq= line[0]
        clas = line[1]
        
        for fea in dipep_test:
            dipep_test[fea]= 0
        
        #making dipeptide score card
        for aa in range(0, len(seq)-(gap+1)):  
            tempaa= seq[aa:aa+(gap+2)]
            dipep_test[tempaa]= int(dipep_test[tempaa])+1
        gg=0.0
        j= 0
        for x6 in sosco_key:
            gg+= float((chromosome[j])*dipep_test[x6])
            j+=1
        ts_scor_clas.append(gg/(len(seq)-(gap+1))) 
        ts_scor_clas.append(clas)
        
        # ts_scor_clas=[gg/(len(seq)-(gap+1)),clas]
        ts_file.append(ts_scor_clas)
        ts_scor_clas= [] 
        indexl.append(index % nfold)
        index = index + 1
        

    auc_score = 0
    kfoldacc = 0
    
    #nfold=10
    for i in range(nfold):
        test = []
        train = []
        count = 0
        
        # make 1 test group,and 9 train group
        # ts_file is a list of score [[gg/(len(seq)-(gap+1)),real],......]
        for selectedIndex in ts_file:
            if indexl[count] == i:
                test.append(ts_file[count])
            else:
                train.append(ts_file[count])
            count = count + 1
    
        # Train to find Best Score , train is a list of score [[gg/(len(seq)-(gap+1)),real],[gg/(len(seq)-(gap+1)),real]......]
        for everysample in train:
            sco.append(everysample[0])
        sco.sort()
        

        TPRl=[]
        FPRl=[]
        x= sco[0] #x is the min
        maxacc = -1
        
        #sco is a list of score [predict,predict,predict] sorted,from small to large
        while x<= sco[-1]:
            thre= x
            TP=0.0 #true positive
            FP=0.0
            TN=0.0
            FN=0.0
            TPR= 0.0
            FPR= 0.0
            for everysample in test:
                ss= everysample[0] #predict score
                clas= everysample[1] #real clas
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
        ###something wrong
        for pp in range(0, len(TPRl)-2):
            high= float(FPRl[pp])-float(FPRl[pp+1])
            bottom= float(TPRl[pp])+float(TPRl[pp+1])
            area= float(bottom*high)/2.0
            ARC+= area
        #print(ARC)
        auc_score = auc_score+ARC
        kfoldacc = kfoldacc + maxacc    

    auc_score = (auc_score/nfold) #average
    #print('auc_score : '+str(auc_score))
    kfoldacc = (kfoldacc/nfold) #average
    
    #caculate aa score for each aa
    cur_aa_score = [0 for i in range(20)]
    k=0
    for i in range(400):
        if (k == 20):
           k=0
        cur_aa_score[k] = cur_aa_score[k] + chromosome[i] #後項
        cur_aa_score[int(i/20)] = cur_aa_score[int(i/20)] + chromosome[i] #前項
        k = k+1
    for i in range(20):
        cur_aa_score[i] = cur_aa_score[i]/40

    corr_score = pearson_def(avg_aa_score, cur_aa_score)
    #corr_dipep_score = 1-pearson_def(ori_dipep_score,self.chromosome)
    score = (W1*auc_score + W2*corr_score)*100 
    #conpute score w1=0.9 w2=0.1 ，smaller better
    return kfoldacc,score
    
    
class Environment(genetic.Environment):
    def evaluate_pop(self):
        chrom_list=[n.chromosome for n in self.population]
        acc_score = pool.map(p_evaluate,chrom_list)
        
        num=0

        print('===== acc_score =====')
        print(acc_score)
        for ind in self.population:
            ind.kfoldacc = acc_score[num][0]
            ind.score = acc_score[num][1]
            num += 1
            
        
class OneMax(genetic.Individual):
    boundMAX = 1000
    boundMIN = 0
    length = 400
    #optimization = genetic.MINIMIZE

    def evaluate(self, optimum=None):
        sco= []
        x= 0.0
        dipep_test= {}
        for x1 in sosco_key:
            dipep_test[x1]= 0

        
        ts_scor_clas= []
        ts_file= []

        
        index = 1
        indexl = []
        
        #samplelist have all sample
        
        for line in samplelist:

            
            seq= line[0]
            clas = line[1]
            
            for fea in dipep_test:
                dipep_test[fea]= 0
            
            #making dipeptide score card
            for aa in range(0, len(seq)-(gap+1)):  
                tempaa= seq[aa:aa+(gap+2)]
                dipep_test[tempaa]= int(dipep_test[tempaa])+1
            gg=0.0
            j= 0
            for x6 in sosco_key:
                gg+= float((self.chromosome[j])*dipep_test[x6])
                j+=1
            ts_scor_clas.append(gg/(len(seq)-(gap+1))) 
            ts_scor_clas.append(clas)
            
            # ts_scor_clas=[gg/(len(seq)-(gap+1)),clas]
            ts_file.append(ts_scor_clas)
            ts_scor_clas= [] 
            indexl.append(index % nfold)
            index = index + 1
            

        auc_score = 0
        kfoldacc = 0
        
        #nfold=10
        for i in range(nfold):
            test = []
            train = []
            count = 0
            
            # make 1 test group,and 9 train group
            # ts_file is a list of score [[gg/(len(seq)-(gap+1)),real],......]
            for selectedIndex in ts_file:
                if indexl[count] == i:
                    test.append(ts_file[count])
                else:
                    train.append(ts_file[count])
                count = count + 1
        
            # Train to find Best Score , train is a list of score [[gg/(len(seq)-(gap+1)),real],[gg/(len(seq)-(gap+1)),real]......]
            for everysample in train:
                sco.append(everysample[0])
            sco.sort()
            

            TPRl=[]
            FPRl=[]
            x= sco[0] #x is the min
            maxacc = -1
            
            #sco is a list of score [predict,predict,predict] sorted,from small to large
            while x<= sco[-1]:
                thre= x
                TP=0.0 #true positive
                FP=0.0
                TN=0.0
                FN=0.0
                TPR= 0.0
                FPR= 0.0
                for everysample in test:
                    ss= everysample[0] #predict score
                    clas= everysample[1] #real score
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

        auc_score = (auc_score/nfold) #average
        kfoldacc = (kfoldacc/nfold) #average
        #caculate aa score for each aa
        cur_aa_score = [0 for i in range(20)]
        k=0
        for i in range(400):
            if (k == 20):
               k=0
            cur_aa_score[k] = cur_aa_score[k] + self.chromosome[i] #後項
            cur_aa_score[int(i/20)] = cur_aa_score[int(i/20)] + self.chromosome[i] #前項
            k = k+1
        for i in range(20):
            cur_aa_score[i] = cur_aa_score[i]/40
    
        corr_score = pearson_def(avg_aa_score, cur_aa_score)
        #corr_dipep_score = 1-pearson_def(ori_dipep_score,self.chromosome)
        self.kfoldacc = kfoldacc
        self.score = (W1*auc_score + W2*corr_score)*100 #conpute score w1=0.9 w2=0.1 ，smaller better

    def crossover(self, other):
        
        
        
        chromosomesList = [];
        chromosomesList.append(self)
        chromosomesList.append(other)
        
        papa = self.chromosome[:]
        mama = other.chromosome[:]
        
        #???
        child1 = self.__class__(papa)
        child2 = self.__class__(papa)

        #---------- Find Different -------------------------
        indif = [Temp for Temp in range(1,self.length) if papa[Temp] != mama[Temp]]
        ndif = len(indif)        
        if ndif == 0:
            return self, other
    
        #---------- OA -------------------------------------
    
        oaarray= []
        level=2
        factor= ndif
        temp= level-1

        #number of exp setting
        J=1
        while (((level**J)-1)/temp)< factor:
            J+=1
        
        exp= int(level**J)
        
        #initialize the array ; oaarray factor*exp 
        oaarray= [[0 for j in range(factor)] for i in range(exp)]

        #******not understand*****#
        remaind= exp
        pow_level_k= 1
        for k in range(0, J):
            j= int((pow_level_k-1)/temp )
            remaind/= level 
            for i in range(0, exp):
                oaarray[i][j]= (int(i/int(remaind)))%level
            pow_level_k*= level

        pow_level_k= level
        for k in range(1, J):
            j= int((pow_level_k-1)/temp )
            for s in range(0, j): 
                for t in range(1, temp+1): 
                    if (t+j+s*temp)<factor:
                        for i in range(0, exp):
                            oaarray[i][t+j+s*temp]= (oaarray[i][s]*t+oaarray[i][j])%level
            pow_level_k*= level
        #oaarray 是0,1所組成的序列
        #------------------------ OA-end ---------------------------------
        
        exp_fitness= []
        #對每個數字
        for experiment in oaarray:
            childfit= papa[:]
            for k in range(0,ndif):
                if experiment[k]== 0:
                    childfit[indif[k]] = papa[indif[k]]

                elif experiment[k]== 1:
                    childfit[indif[k]] = mama[indif[k]]
                    
            oaChromosome = self.__class__(childfit)
            #oaChromosome.evaluate()
            chromosomesList.append(oaChromosome)
            #exp_fitness.append(oaChromosome.score)
         
        chrom_list=[n.chromosome for n in chromosomesList]
        acc_score = pool.map(p_evaluate,chrom_list)
        num=0
        #print('===== acc_score ====='*10)
        #print(acc_score)
        for ind in chromosomesList:
            ind.kfoldacc = acc_score[num][0]
            ind.score = acc_score[num][1]
            exp_fitness.append(acc_score[num][1])
            num += 1
        
        MED_list= []
        
        #exp_fitness is a list of score
        for qq in range(0, ndif):
            fitness_0= 0.0
            fitness_1= 0.0
            MED= 0.0
            for pp in range(0, exp):
                if oaarray[pp][qq]== 0:
                    fitness_0+= exp_fitness[pp]
                elif oaarray[pp][qq]== 1:
                    fitness_1+= exp_fitness[pp]
                
            MED= fitness_0-fitness_1
            MED_list.append(MED)

        abs_MED_list= []
        for c in range(0, len(MED_list)):
            abs_MED_list.append(MED_list[c]*MED_list[c])
      
        for pp in range(0, ndif):
            if MED_list[pp]< 0.0:
                child1.chromosome[indif[pp]]= papa[indif[pp]]
                child2.chromosome[indif[pp]]= papa[indif[pp]]
            elif MED_list[pp]> 0.0:
                child1.chromosome[indif[pp]]= mama[indif[pp]]
                child2.chromosome[indif[pp]]= mama[indif[pp]]
            else:
                child1.chromosome[indif[pp]]= papa[indif[pp]]
                child2.chromosome[indif[pp]]= mama[indif[pp]]

            if abs_MED_list[pp]== min(abs_MED_list):
                if child2.chromosome[indif[pp]]== papa[indif[pp]]:
                    child2.chromosome[indif[pp]]= mama[indif[pp]]
                elif child2.chromosome[indif[pp]]== mama[indif[pp]]:
                    child2.chromosome[indif[pp]]= papa[indif[pp]]
                    
        child1.evaluate()
        child2.evaluate()
        chromosomesList.append(child1)
        chromosomesList.append(child2)

        chromosomesList.sort(key=lambda x :(x.score) ,reverse=True)
        new_child1,new_child2=chromosomesList[:2]
        
        return new_child1, new_child2
        
    def mutate(self, gene):

        self.chromosome[gene] = random.randint(self.boundMIN,self.boundMAX)

   
if __name__ == "__main__":
    pool=Pool(20) ###
    if time==0:
        mypop= []
        mypop.append(OneMax(f[0]))
        
        for i in range(59):
            #chromosome 是0到1000的數所組成的
            mypop.append(OneMax([round(random.randint(0, 1000)) for gene in range(400)]))
        
        
        env = Environment(OneMax, maxgenerations=ngen,size=60,optimum=None, population= mypop)
        env.run()


    elif time>0:
        print('the time is '+str(time))
        sosco_key,scoring,tmpscore=make_sc(scorecard)

        batch = (n for n in samplelist)
        p_sample=[]
        n_sample=[]
        for n in batch:
            if n[1]=='1':
                p_sample.append(n+[1])
            elif n[1]=='0':
                n.append(cuc_sc(n[0],sosco_key,scoring))
                n_sample.append(n)
                
        n_sample.sort(key=lambda x: (x[2]))
        
        new_sample=p_sample+n_sample[:int(len(p_sample)*time/3)]
        samplelist = [n for n in new_sample]
        
        mypop= []
        mypop.append(OneMax(tmpscore))
        mypop.append(OneMax(f[0]))
        
        for i in range(58):
            #chromosome 是0到1000的數所組成的
            mypop.append(OneMax([round(random.randint(0, 1000)) for gene in range(400)]))
    
    
        env = Environment(OneMax, maxgenerations=ngen,size=60,optimum=None, population= mypop)
        env.run()
    else:
        print('something wrong')

    
 

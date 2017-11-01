
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
cmdparser.add_option("-P", "--Population", action="store", dest="population", default=60, help="number of Population, default is 40")
cmdparser.add_option("-V", "--Weight1", action="store", dest="w1", default=0.9, help="Weight 1 AUC, default is 0.9")
cmdparser.add_option("-W", "--Weight2", action="store", dest="w2", default=0.1, help="Weight 2 Correlation, default is 0.1")
cmdparser.add_option("-s", "--scorecard", action="store", dest="scorecard", default='0', help="input scorecard name")
cmdparser.add_option("-p", "--pools", action="store", dest="pools", default=10, help="number of pools")
(options, args) = cmdparser.parse_args()
if(options.filename == 0):
    print ("  the input filename is not specified!! Please use -f or --file option...")
    exit(" For more information, use -h or --help")
trainname = options.filename
train_file = open(trainname)
gap = int(options.gap)
nfold = int(options.nfold)
ngen = int(options.ngen)
W1 = float(options.w1)
W2 = float(options.w2)
scorecard = options.scorecard
Population = int(options.population)
pools = int(options.pools)

#set score max and min
boundMAX = 1000
boundMIN = 0
#set some const value
aalist= ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
dipep = [x1+x2 for x1 in aalist for x2 in aalist]
samplelist= [n.strip('\n').split('\t') for n in train_file.readlines()]
#read training sample
train_file.close()

###small function we used
#all key to zero
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
#read and make a scoring card
def make_sc(scorecard):
    f3 = open(scorecard)
    count = 0
    tmpscore = []
    for line in f3.readlines():
        if count==3:
            tmpscore1 = line.split('[')
            tmpscore2 = tmpscore1[1].strip(']'),split(',')
            for tmpval in tmpscore2:
                tmpscore.append(float(tmpval))
        count = count + 1
    f3.close()
    return tmpscore
#calculate average
def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)
#calculate Pearson coefficient
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

#initialize dipeptide frequence dic
dipep_0= ini_dic(key_list=dipep)
dipep_1= ini_dic(key_list=dipep)

# counting the positive dipeptide and negative dipeptide
pos_count,neg_count = 0,0
for line in samplelist:       
    seq= line[0]
    clas = int(line[1])
    #divide positive data and negative data
    for aa in range(0, len(seq)-(gap+1)):
        tempaa=seq[aa]+seq[aa+(gap+1)]
        if clas == 0:
            dipep_0[tempaa] += 1
            neg_count += 1
        elif clas == 1:
            dipep_1[tempaa] += 1
            pos_count += 1
    
scoring = []
for x5 in dipep:
    # times 1000 to make score bigger
    eachscore = float(((float(dipep_1[x5])/pos_count)-(float(dipep_0[x5])/neg_count))*1000)
    scoring.append(eachscore)
#nomolize them
nol_scoring= []
for i in scoring:
    n= (i-min(scoring))/(max(scoring)-min(scoring))*1000
    nol_scoring.append(round(n))

#ini_scorecard is the first scoring card
ini_scorecard = nol_scoring
avg_aa_score = count_aa_score(ini_scorecard)

def p_evaluate(chromosome):
    
    sco= []
    x= 0.0
    ts_file= []
    index = 1
    indexl = []
    #use index the divide k-fold data,indexl store all index
    for line in samplelist:
        dipep_test= ini_dic(key_list=dipep)
        seq= line[0]
        clas = line[1]
        #count dipeptide frequence
        for aa in range(0, len(seq)-(gap+1)):  
            tempaa= seq[aa:aa+(gap+2)]
            dipep_test[tempaa] += 1
        #caculate score of each dipeptide
        gg=0.0
        j= 0
        for x6 in dipep:
            gg+= float((chromosome[j])*dipep_test[x6])
            j+=1
        #append [score,clas] and index
        ts_file.append([gg/(len(seq)-(gap+1)),clas])
        indexl.append(index % nfold)
        index = index + 1
    
    auc_score = 0
    kfoldacc = 0
    for i in range(nfold):
        test = []
        train = []
        # make test set and train set
        for count in range(len(ts_file)):
            if indexl[count] == i:
                test.append(ts_file[count])
            else:
                train.append(ts_file[count])
    
        # Train to find Best Score , train is a list of score [[gg/(len(seq)-(gap+1)),real]......]
        for sample in train:
            sco.append(sample[0])
        TPRl=[]
        FPRl=[]
        x= min(sco) #x is the min
        maxacc = -1
        
        #sco is a list of score [predict,predict,predict] sorted,from small to large
        while x<= max(sco):
            thre= x
            #initialize true positive,false positive,true negative,false negative
            TP,FP,TN,FN,TPR,FPR=[0.0]*6
            
            for everysample in test:
                ss= everysample[0] #predict score
                clas= everysample[1] #real clas
                assert type(clas) == str
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
        
        #calculate auc
        ARC,area,high,bottom=[0.0]*4
        
        for pp in range(0, len(TPRl)-2):
            high= float(FPRl[pp])-float(FPRl[pp+1])
            bottom= float(TPRl[pp])+float(TPRl[pp+1])
            area= float(bottom*high)/2.0
            ARC+= area
        auc_score += ARC
        kfoldacc += maxacc
    auc_score = (auc_score/nfold) #average
    kfoldacc = (kfoldacc/nfold) #average
    #caculate aa score for each aa
    cur_aa_score = count_aa_score(chromosome)
    corr_score = pearson_def(avg_aa_score, cur_aa_score)
    score = (W1*auc_score + W2*corr_score)*100 
    #conpute score w1=0.9 w2=0.1 ，bigger better
    return kfoldacc,score
    
class Environment(genetic.Environment):
    #evaluate all chromosome
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
        self.kfoldacc,self.score = p_evaluate(self.chromosome)
    def crossover(self, other):
        #chrom_list contain chromosome in this crossover
        chromosomesList = [];
        chromosomesList.append(self)
        chromosomesList.append(other)
        papa = self.chromosome[:]
        mama = other.chromosome[:]
        #copy the class 
        child1 = self.__class__(papa)
        child2 = self.__class__(papa)
        ###Find Different
        indif = [Temp for Temp in range(1,self.length) if papa[Temp] != mama[Temp]]
        ndif = len(indif)
        # if all same quit function
        if ndif == 0:
            return self, other
        ###OA
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
        #IGA : making OA array
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
        #oaarray is an array contain 0 and 1 , 0 : use papa ; 1 : use mama
        #OA-end
        exp_fitness= []
        #for every word
        for experiment in oaarray:
            childfit= papa[:]
            for k in range(0,ndif):
                if experiment[k]== 0:
                    childfit[indif[k]] = papa[indif[k]]
                elif experiment[k]== 1:
                    childfit[indif[k]] = mama[indif[k]]
                    
            oaChromosome = self.__class__(childfit)
            chromosomesList.append(oaChromosome)
        #use multiprocessing to accerate speed
        chrom_list=[n.chromosome for n in chromosomesList]
        acc_score = pool.map(p_evaluate,chrom_list)
        num=0
        for ind in chromosomesList:
            ind.kfoldacc = acc_score[num][0]
            ind.score = acc_score[num][1]
            exp_fitness.append(acc_score[num][1])
            num += 1
        
        #compare and find med
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
        #sorting the chromosome
        chromosomesList.sort(key=lambda x :(x.score) ,reverse=True)
        new_child1,new_child2=chromosomesList[:2]
        return new_child1, new_child2
    #change the mutate method
    def mutate(self, gene):
        self.chromosome[gene] = random.randint(self.boundMIN,self.boundMAX)

if __name__ == "__main__":
    pool=Pool(pools)
    t = 1
    mypop= []
    mypop.append(OneMax(ini_scorecard))
    if scorecard != '0':
        tmpscore=make_sc(scorecard)
        mypop.append(OneMax(tmpscore))
        t += 1
    
    for i in range(Population-t):
        #chromosome 是0到1000的數所組成的
        mypop.append(OneMax([round(random.randint(0, 1000)) for gene in range(400)]))
    
    env = Environment(OneMax, maxgenerations=ngen,size=Population,optimum=None, population= mypop)
    env.run()
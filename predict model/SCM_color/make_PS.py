from optparse import OptionParser #markliou
import numpy as np
aalist= ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

cmdparser = OptionParser()
cmdparser.add_option("-f", "--file", action="store", dest="filename", default='example/istr', help="input a scorecard filename")
cmdparser.add_option("-t", "--type", action="store", dest="score_type", default='DPS', help="input a scoring type")
cmdparser.add_option("-o", "--out", action="store", dest="outname", default='DPS.tab', help="input a output filename")
cmdparser.add_option("-n", "--normalize", action="store_true", dest="nol", default=False, help="using normalize")
(options, args) = cmdparser.parse_args()
filename1 = options.filename
score_type = options.score_type
outname = options.outname
nol = options.nol

f = open(filename1)
i = 0
def cuc_aa(c_list):
    c_list = [float(n) for n in c_list]
    each_aa_score = [0]*20
    for n in range(20):
        for i in range(20):
            each_aa_score[n]+=c_list[20*n+i]
            each_aa_score[i]+=c_list[20*n+i]
    each_aa_score = [n/40 for n in each_aa_score]
    return each_aa_score
def std(l):
    l = np.array([float(i) for i in l])
    mean = l.mean()
    std = l.std()
    l = l.tolist()
    out_list=[]
    uplimit=mean+2*std
    downlimit=mean-2*std
    for n in l:
        if n>uplimit:
            out_list.append(round(uplimit,1))
        elif n<downlimit:
            out_list.append(round(downlimit,1))
        else:
            out_list.append(n)
    return [str(n) for n in out_list]
#read score card
scores = []
for l in f.readlines():
    if i==3:
        #print(l)
        scores = l.strip('\n').split('\t')[1].strip('[').strip(']').split(',')
    i+=1
f.close()

# score_type
outfile = open(outname,'w')
if score_type.upper()=='DPS':
    if nol :
        scores = std(scores)
    out = ""
    for n in range(21):
        if n==0:
            out += "\t".join(aalist)+'\n'
        else:
            out += "\t".join(scores[20*(n-1):20*n])+'\n'
    outfile.write(out.strip('\n'))
    
elif score_type.upper()=='PS':
    c_list = cuc_aa(scores)
    if nol:
        c_list = std(c_list)
    out = ""
    for n in range(20):
        out += aalist[n]+'\t'+str(c_list[n])+'\n'
    outfile.write(out.strip('\n'))
else:
    print('unknown input')
outfile.close()


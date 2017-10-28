from optparse import OptionParser #markliou
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

aalist= ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

cmdparser = OptionParser()
cmdparser.add_option("-f", "--file", action="store", dest="filename", default='new_scorecard_1016', help="input a training data filename")
(options, args) = cmdparser.parse_args()
filename1 = options.filename
#read score card
f = open(filename1)
i = 0
for l in f.readlines():
    if i==3:
        print(l)
        scores = l.strip('\n').split('\t')[1].strip('[').strip(']').split(',')
    i+=1
f.close()

scores = np.array(scores,dtype=np.float32).reshape((20,20))
pt = pd.DataFrame(scores,index=aalist,columns=aalist)
#print(pt)

f,ax = plt.subplots(figsize=(12,8))
cmap = sns.cubehelix_palette(as_cmap=True)
sns.heatmap(pt, linewidths = 0.05, ax = ax, vmax=1000, vmin=0,center=350,fmt = '.1f'
        ,cmap='RdBu_r',annot=True,annot_kws={'size':8,'color':'black'}) 
ax.set_title('AFP scoring card',fontdict={'fontsize':24})
ax.set_xlabel('Amino Acid(second)',fontdict={'fontsize':16})
ax.set_ylabel('Amino Acid(first)',fontdict={'fontsize':16})

#f.show()
f.savefig('AFP.jpg', bbox_inches='tight')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

aalist= ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
filename = 'new_scorecard_1016'
f = open(filename)
for l in f:
    if l.startswith('best chromosome'):
        t = l.strip('\n').split('\t')
        c = t[1].strip('[').strip(']')
        c_list = [float(n) for n in c.split(',')]
        assert len(c_list)==400
each_aa_score = [0]*20
for n in range(20):
    for i in range(20):
        each_aa_score[n]+=c_list[20*n+i]
        each_aa_score[i]+=c_list[20*n+i]
        
each_aa_score = [n/40 for n in each_aa_score]
print(each_aa_score)
score_list=[aalist[n]+'\n'+str(each_aa_score[n]) for n in range(20)]
plt.figure(figsize=(12,6))
sns.barplot(score_list, each_aa_score, alpha=0.8)
#plt.xticks(rotation='vertical')
plt.xlabel('AA', fontsize=12)
plt.ylabel('average score', fontsize=12)
plt.show()
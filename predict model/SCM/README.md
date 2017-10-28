# Scoring Card Method Code

The following requirements are needed for using the scoring card predicting model.

`python>=3.6` with packages :`optparse`,`math`,`multiprocessing`

You can use `pip` to install these packages
```
pip install optparse
pip install math
pip install multiprocessing
```

>Scoring Card Data Format
>----------

ACCCTTTTYYYYMMMMMACAC	1
ACCAAMMMMTTTRRSSSSSSSS	0

1 = positive class
0 = negative class

Example file
1. crtr (Crystallization Training)
2. crts (Crystallization Testing)
3. istr (Solubility Training)
4. ists (Solubility Testing)


>Optimization
>---------
Use `optimize_max.py` to make and optimize the scoring card
```
python optimize_max.py -f [datafile]
```
there are some options to run the code:

`-g [--gap]` gap number ,default is 0
`-v [--cvfold]` the fold of cross validation , default is 10
`-G [--Generation]` number fo generation , default is 20
`-V [--Weight1]` the AUC fitness weight , default is 0.9
`-W [--Weight2]` the correlation weight , default is 0.1

##################
##  Prediction  ##
##################

Command line :
python prediction.py training test scorecard

See option :
python prediction.py -h

#########################
## Optimization Output ##
#########################

file name :
output_scorecard1

file organization :
gen_score:	(Generation Score)
best CV:	0
best scoring:	(Best Score)
best chromosome:	[400 propensity score of dipeptides (Check dipeptides order in dipep)]

#########################
##  Prediction Output  ##
#########################

file name :
[name of test]_result.csv
[name of test]_ori.csv (Original Score Card)

Result file organization :
[fitness score]	[fulltrain acc]	[crossvalidation acc]	[MCC]	[test acc]	[sensitivity]	[specificity]	[crossvalidation auc]	[R value]	[threshold]


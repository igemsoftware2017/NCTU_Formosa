# Scoring Card Method Code

The following requirements are needed for using the scoring card predicting model.

`python>=3.6` with packages :`optparse`,`math`,`multiprocessing`

These packages are all in python standard library.
If you do not have these packages you can use `pip` to install these packages.
```
pip install optparse
pip install math
pip install multiprocessing
```

Scoring Card Data Format
----------

ACCCTTTTYYYYMMMMMACAC	1

ACCAAMMMMTTTRRSSSSSSSS	0

1 = positive class

0 = negative class

### Example file

1. example_train : AFP_example(training_data)

2. example_test : AFP_example(testing)

Optimization
---------
Use `optimize_max.py` to make and optimize the scoring card
```
python optimize_max.py -f [datafile]
```
there are some options to run the code:

`-g [--gap]` gap number ,default is 0

`-v [--cvfold]` the fold of cross validation , default is 10

`-G [--Generation]` number of generation , default is 20

`-P [--Population]` number of population , default is 60

`-V [--Weight1]` the AUC fitness weight , default is 0.9

`-W [--Weight2]` the correlation weight , default is 0.1

`-s [--scorecard]` the scorecard for retrain

`-p [--pools]` the numbers of multiprocessing , default is 10

#### note : you can use -h , --help to find more options and description

### Optimization Output

file name :output_scorecard1

file organization :
gen_score:	(Generation Score)
best CV:	0
best scoring:	(Best Score)
best chromosome:	[400 propensity score of dipeptides (Check dipeptides order in dipep)]

Prediction
--------
Use `predict.py` to evaluate the scorecard

```
python predict.py -f [train data] -t [test data] -s [scorecard file]
```

#### note : you can use -h , --help to find more options and description

### Prediction output
```
---------- Result ----------
FullTrain_acc = (The best k-fold accuracy of training data)
CV acc(train) = (The accuracy of training data)
CV auc(train) = (The AUC of training data)
Theshold = (The best threshold)
Test_acc = (The testing accuracy with theshold)
Sensitivity = (The testing sensitivity with theshold)
Specitivity = (The testing specificity with theshold)
```

This code is from [Shinn-Ying Ho's Lab website](http://iclab.life.nctu.edu.tw/iclab_webtools/SCMBYK/download.php) with some modification.
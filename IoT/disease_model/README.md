Disease Predictin Model
========

This is a the CNN base model that can use for disease prediction

How to use ?
--------
The following requirement are needed for using this model.

`python >= 3.6` with packages : `optparse`,`numpy`,`tensorflow`>=1.2,`tensorlayer`

you can use `pip` to install these packages
```
pip intsall numpy
pip install tensorflow==1.2
pip install tensorlayer
```

Training model
--------
Run `CNN.py` to starting training

You need to input the training file , testing file ,and savename to run the code

Example :
```
python CNN.py -f train.csv -t test.csv -s example
```
they are some options to modify the network hyper parameters

`-l [--learning_rate]` the learning_rate , default is 0.001

`-b [--batch_size]` the batch size , default is 128

`-e [--epoch]` epochs you want to train , default is 200 

`-d [--days]` how long the time steps is , default is 14

`-m [--model]` key in a model name if you want to retrain our model 

`-g [--graph]` using tensorboard or not

After training , model output a `.npz` format file ,it can be easy analyze by `tl.files.load_npz` function
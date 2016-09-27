---
layout: post
title: kerasでgrid-search
date: 2016-06-12 00:00:00 +0900
comments: false
---

# はじめに

Kerasの`Sequential`ではScikit-learnのAPIが利用できるラッパーが提供されています．
これによってscikit-learnのK-Foldやgrid-searchをKerasのモデルに使うことができます．
その機能をMNISTを例にして紹介します．

# 本題

3層の多層パーセプトロンの中間層と中間層の活性化関数をgrid-searchします．

分類を行う場合は`KerasClassifier`にKerasのモデルを渡すことで，scikit-learnの分類器と同じように扱えます．
このとき，Kerasの`fit()`で使用するパラメータ`nb_epoch, batch_size, verbose`は`KerasClassifier`のコンストラクタに渡すことができます．ちなみにこれらの値もgrid-searchで探索可能です．
あとはsklearnと同様，探索するパラメータを辞書型のデータで渡すだけです．


以下のサンプルコードでは，中間層の次元数が`[10,100,1000]`の3つと活性化関数が7つの計21通りを探索対象としています．


```python
import numpy as np
np.random.seed(13)

from sklearn import grid_search

from keras.models import Sequential
from keras.datasets import mnist
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.utils.visualize_util import model_to_dot, plot
from keras.wrappers.scikit_learn import KerasClassifier

(X_train, y_train), (X_test, y_test) = mnist.load_data()

nb_classes = 10 # class size
input_unit_size = 28*28 # input vector size

# 前処理
X_train = X_train.reshape(X_train.shape[0], input_unit_size)
X_test  = X_test.reshape(X_test.shape[0], input_unit_size)
X_train = X_train.astype('float32')
X_test  = X_test.astype('float32')
X_train /= 255
X_test  /= 255

def create_model(activation="relu", nb_hidden=10):
    model = Sequential()
    model.add(Dense(nb_hidden, input_dim=784, init='glorot_uniform'))
    model.add(Activation(activation))
    model.add(Dense(10, init='glorot_uniform'))    
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer="adadelta", 
                  metrics=['accuracy'])
    return model

activations = ["softplus", "softsign", "relu", "tanh", "sigmoid", "hard_sigmoid", "linear"]
nb_hiddens = np.array([10,100,1000])

param_grid = dict(activation=activations, nb_hidden=nb_hiddens)
model = KerasClassifier(build_fn=create_model, nb_epoch=10, batch_size=256, verbose=0)

clf = grid_search.GridSearchCV(estimator=model, param_grid=param_grid, cv=4, scoring='accuracy')
res = clf.fit(X_train, y_train)

```


```python
0.971166666667 {'nb_hidden': 1000, 'activation': 'relu'} # best

# meanの高い順にsort
mean: 0.97117, std: 0.00098, params: {'nb_hidden': 1000, 'activation': 'relu'}
mean: 0.95432, std: 0.00113, params: {'nb_hidden': 1000, 'activation': 'softsign'}
mean: 0.95185, std: 0.00211, params: {'nb_hidden': 1000, 'activation': 'tanh'}
mean: 0.95170, std: 0.00134, params: {'nb_hidden': 100, 'activation': 'relu'}
mean: 0.94548, std: 0.00259, params: {'nb_hidden': 100, 'activation': 'tanh'}
mean: 0.93992, std: 0.00167, params: {'nb_hidden': 100, 'activation': 'softsign'}
mean: 0.93367, std: 0.00376, params: {'nb_hidden': 1000, 'activation': 'softplus'}
mean: 0.93197, std: 0.00290, params: {'nb_hidden': 100, 'activation': 'softplus'}
mean: 0.92327, std: 0.00321, params: {'nb_hidden': 100, 'activation': 'sigmoid'}
mean: 0.92133, std: 0.00373, params: {'nb_hidden': 100, 'activation': 'hard_sigmoid'}
mean: 0.91957, std: 0.00337, params: {'nb_hidden': 100, 'activation': 'linear'}
mean: 0.91725, std: 0.00248, params: {'nb_hidden': 1000, 'activation': 'sigmoid'}
mean: 0.91712, std: 0.00566, params: {'nb_hidden': 1000, 'activation': 'linear'}
mean: 0.91403, std: 0.00352, params: {'nb_hidden': 10, 'activation': 'relu'}
mean: 0.91322, std: 0.00450, params: {'nb_hidden': 1000, 'activation': 'hard_sigmoid'}
mean: 0.91000, std: 0.00306, params: {'nb_hidden': 10, 'activation': 'linear'}
mean: 0.90602, std: 0.00654, params: {'nb_hidden': 10, 'activation': 'softplus'}
mean: 0.90327, std: 0.00214, params: {'nb_hidden': 10, 'activation': 'tanh'}
mean: 0.89817, std: 0.00360, params: {'nb_hidden': 10, 'activation': 'softsign'}
mean: 0.87140, std: 0.00775, params: {'nb_hidden': 10, 'activation': 'hard_sigmoid'}
mean: 0.87007, std: 0.00366, params: {'nb_hidden': 10, 'activation': 'sigmoid'}
```

もっとも良かったのは，中間層が1000次元で活性化関数が`relu`のときでした．

コードは[こちら](https://github.com/nzw0301/keras-examples/blob/master/sklearn_MLP_MNIST.ipynb)を．

# 参考

- [Use Keras Deep Learning Models with Scikit-Learn in Python](http://machinelearningmastery.com/use-keras-deep-learning-models-scikit-learn-python/)
- [Wrappers for the Scikit-Learn API](http://keras.io/scikit-learn-api/)

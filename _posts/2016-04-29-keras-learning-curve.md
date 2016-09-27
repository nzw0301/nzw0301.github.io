---
layout: post
title: kerasで最適化アルゴリズム別の学習曲線を描く
date: 2016-04-29 00:00:00 +0900
comments: false
---

# はじめに

kerasは学習を終えると，モデルのパラメータや，epochごとの訓練誤差やaccuracyをもった`Histroy`オブジェクトを返します．
これを使うと簡単に学習曲線を描くことができます．
（いい加減飽き飽きしますが，）MNISTを使って出してみます．

# 本題
最適化アルゴリズム別にepochごとのaccuracyを出してみます．
使用したアルゴリズムは以下の7つです．パラメータはデフォルトのものを使います．

- SGD
- Adadelta
- Adagrad
- Adam
- Adamax
- RMSprop
- Nadam

```python
from keras.models import Sequential
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD, Adadelta, Adagrad, Adam, Adamax, RMSprop, Nadam
from keras.utils import np_utils
import numpy as np
from matplotlib import pyplot as plt
%matplotlib inline
plt.style.use("fivethirtyeight")

nb_classes = 10 # class size
input_unit_size = 28*28 # input vector size

(X_train, y_train), (X_test, y_test) = mnist.load_data()

# 前処理
X_train = X_train.reshape(X_train.shape[0], input_unit_size)
X_test  = X_test.reshape(X_test.shape[0], input_unit_size)
X_train = X_train.astype('float32')
X_test  = X_test.astype('float32')
X_train /= 255
X_test  /= 255

# one-hot representation
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

optimizers = [SGD, Adadelta, Adamax, Adam, Adagrad,  RMSprop, Nadam]
results = {}
for opitmizer in optimizers:
    
    model = Sequential()
    model.add(Dense(128, input_dim=input_unit_size, init='glorot_uniform'))
    model.add(Activation("relu"))
    model.add(Dense(nb_classes, init='glorot_uniform'))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer=opitmizer(), metrics=['accuracy'])

    # 学習
    results[opitmizer.__name__] = model.fit(X_train, Y_train, nb_epoch=10, batch_size=128, verbose=2,  validation_split=0.2)

x = range(10)
# plot accuracy of train data
for k, result in results.items():
    plt.plot(x, result.history['acc'], label=k)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# plot accuracy of validation data
for k, result in results.items():
    plt.plot(x, result.history['val_acc'], label=k)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

```

上記のコードをjupyterで実行すると2つグラフが描画されます．

こっちはtraining dataのaccuracy
![index.png](https://qiita-image-store.s3.amazonaws.com/0/72604/21cdb9d0-b3f0-ece4-b4df-50128469f427.png)


こっちはvalidation dataのaccuracy
![test_index.png](https://qiita-image-store.s3.amazonaws.com/0/72604/ea422f09-edfc-e846-59c5-bc316b913d9b.png)


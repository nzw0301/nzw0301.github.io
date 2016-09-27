---
layout: post
title: SVMとKFoldをmutiprocessingとParalellで扱う
date: 2016-02-18 00:00:00 +0900
comments: false
---

## はじめに

`Kfold`を並列処理したいときに，`multiprocessing`と`Parallel`のどっちを使ったらいいのかわからなかったので，簡単な比較．

個人的には`Parallel`だと引数を複数指定できるのでこっちを使うかなという感じ．（[mulitprocessingのmapは引数1つのようなので](http://docs.python.jp/3.3/library/multiprocessing.html#multiprocessing.pool.Pool.map)）


## 環境

- python 3.5.1 (anaconda 2.5.0)
- MBA (yosemite)
    - メモリ8GB
    - 1.4 GHz Intel Core i5

## 本題
題材として扱えるいいかんじのデータがなかったので，ガウス分布から2次元ベクトルのデータを40,000サンプル生成して2値分類のSVMで学習する．
このとき，K-分割交差検証 ( $$K=4$$ ) で評価したいためこれを並列化したい．


### 可視化
各クラスを200点ずつサンプルし，可視化してみる．

```python
import numpy as np

import matplotlib.pyplot as plt
%matplotlib inline
plt.style.use("fivethirtyeight")

# 適当な正規分布2つからサンプル
np.random.seed(13)
sample_size = 200
data0 = np.random.multivariate_normal([-1, -1], [[1,0],[0,1]], sample_size)
data1 = np.random.multivariate_normal([1,1], [[1,0],[0,1]], sample_size)

x0 = data0[:,0]
y0 = data0[:,1]
x1 = data1[:,0]
y1 = data1[:,1]

plt.plot(x0,y0,"o")
plt.plot(x1,y1,"x")
```

![index.png](https://qiita-image-store.s3.amazonaws.com/0/72604/fcc0b898-8da6-5f90-b179-b9aec0d92f73.png)

### 並列化なし

```python
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import KFold

np.random.seed(13)
sample_size = 20000
data0 = np.random.multivariate_normal([-1, -1], [[1,0],[0,1]], sample_size)
data1 = np.random.multivariate_normal([1,1], [[1,0],[0,1]], sample_size)
data = np.concatenate((data0,data1), axis=0)
label = np.concatenate((np.zeros(sample_size),np.ones(sample_size)), axis=0)
folds_size = 4

kf = KFold(len(label), n_folds=folds_size, shuffle=True,random_state=13)

for train_idxs, test_idxs in kf:
    x_train = data[train_idxs]
    y_train = label[train_idxs]
    x_test  = data[test_idxs]
    y_test  = label[test_idxs]
    clf = svm.SVC()
    clf.fit(x_train, y_train)

    predicted_test_y = clf.predict(x_test)
    print(accuracy_score(y_test, predicted_test_y))
```

### multiprocessing

`kFold`はタプルのリストのようなものを保持しているので，今回は`map`に渡す引数が1つで済む．

```python
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import KFold
from multiprocessing import Pool

np.random.seed(13)
sample_size = 20000
data0 = np.random.multivariate_normal([-1, -1], [[1,0],[0,1]], sample_size)
data1 = np.random.multivariate_normal([1,1], [[1,0],[0,1]], sample_size)

data = np.concatenate((data0,data1), axis=0)
label = np.concatenate((np.zeros(sample_size),np.ones(sample_size)), axis=0)

folds_size = 4
kf = KFold(len(label), n_folds=folds_size, shuffle=True,random_state=13)

def cal_accuracy_one_fold(one_kf):
    train_idxs, test_idxs = one_kf
    x_train = data[train_idxs]
    y_train = label[train_idxs]
    x_test  = data[test_idxs]
    y_test  = label[test_idxs]
    clf = svm.SVC()
    clf.fit(x_train, y_train)

    predicted_test_y = clf.predict(x_test)
    return accuracy_score(y_test, predicted_test_y)

pool = Pool(processes=folds_size)
results = pool.map(cal_accuracy_one_fold, kf)
print(results)
```

### Parallel

```python
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import KFold
from sklearn.externals.joblib import Parallel, delayed

np.random.seed(13)
sample_size = 20000
data0 = np.random.multivariate_normal([-1, -1], [[1,0],[0,1]], sample_size)
data1 = np.random.multivariate_normal([1,1], [[1,0],[0,1]], sample_size)

data = np.concatenate((data0,data1), axis=0)
label = np.concatenate((np.zeros(sample_size),np.ones(sample_size)), axis=0)

folds_size = 4
kf = KFold(len(label), n_folds=folds_size, shuffle=True,random_state=13)

def cal_accuracy_one_fold(train_idxs, test_idxs):
    x_train = data[train_idxs]
    y_train = label[train_idxs]
    x_test  = data[test_idxs]
    y_test  = label[test_idxs]
    clf = svm.SVC()
    clf.fit(x_train, y_train)
    predicted_test_y = clf.predict(x_test)
    return accuracy_score(y_test, predicted_test_y)

results = Parallel(n_jobs=4)(delayed(cal_accuracy_one_fold)(train_idxs, test_idxs) for train_idxs, test_idxs in kf)
print(results)
```


## 計測
楽をして`time`で計測した．
並列化なしと比較してそれ以外の2つは，だいたい倍速．

- 並列化なし
    - 49.55s user 1.36s system  98% cpu 51.952 total
- `multiprocessing`
    - 74.55s user 1.73s system 286% cpu 26.608 total
- `Parallel`
    - 74.32s user 1.79s system 284% cpu 26.791 total


`Parallel`の`backend`のデフォルトが `multiprocessing` （[githubより](https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/externals/joblib/parallel.py#L416)）なので同じような実行時間になってるのかなぁと思いました．

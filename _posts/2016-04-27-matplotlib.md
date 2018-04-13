---
layout: post
title: matplotlibで正方に画像を描画
date: 2016-04-27 00:00:00 +0900
comments: false
---

# 概要

matplotlibを使って，MNISTでニューラルネットワーク試してみました！でよくみる以下ようなplotのやり方．

![スクリーンショット 2016-04-27 21.56.54.png](https://qiita-image-store.s3.amazonaws.com/0/72604/23f5bd81-b565-21c1-352c-4a4434b2e33b.png)

# コード

```python
from keras.datasets import mnist
import numpy as np

from matplotlib import pyplot as plt
%matplotlib inline

# MNIST data(28x28 matrix)
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# visualization
def draw_digit(data, row, col, n):
    size = 28
    plt.subplot(row, col, n)
    plt.imshow(data)
    plt.gray()

show_size = 10
total = 0
plt.figure(figsize=(20,20))
for i in range(show_size):
    for j in range(show_size):
        draw_digit(X_train[total], show_size, show_size, total+1)
        total += 1
plt.show()
```

肝心なのは `plt.subplot(row, col, n)` ．
`row`と`col`はそれぞれ行数と列数で，固定値．
今回は10x10なので常に10．
`n`には1スタートでその行列の何番目に描画するかを指定．

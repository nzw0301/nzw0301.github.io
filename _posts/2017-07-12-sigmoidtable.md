---
layout: post
title: "sigmoid table for word2vec&fasttext"
comments: true
abstract: 計算テクニック
---

### はじめに

Skip-gram&NegativeSamplingでは（正例数 $$\times$$ (neg+1) $$\times$$ 反復回数）だけ出力層でsigmoid関数を呼ぶ。
これを避けるためにword2vecやfasttextではsigmoid関数の評価値をキャッシュすることで高速化している。
ざっくりとした解説を以下に書く。

### 本題

word2vecの拡張ライブラリである[fasttext](https://github.com/facebookresearch/fastText/blob/5282d91c9f116fe58b9bdbfd467fb1d24f5c4831/src/model.cc)の変数と実装に従って説明する。


まず、関係する定数として `SIGMOID_TABLE_SIZE` と `MAX_SIGMOID` がある。

`SIGMOID_TABLE_SIZE`は、事前に計算するsigmoid関数の回数。この値は小さいほど荒い計算値を使うことになる。
word2vecでは1000、[fasttextでは512](https://github.com/facebookresearch/fastText/blob/fbc42146893cbdfdc784c50956d9b09dda9d46de/src/model.h#L24)。

`MAX_SIGMOID`は、sigmoid関数の引数の最大値。
この値より大きければ1を返す（`-MAX_SIGMOID`より小さければ0）。
word2vecでは6、[fasttextでは8](https://github.com/facebookresearch/fastText/blob/fbc42146893cbdfdc784c50956d9b09dda9d46de/src/model.h#L25)。

Pythonで書くと以下のようになる。

``` python
import numpy as np

SIGMOID_TABLE_SIZE = 512
MAX_SIGMOID = 8

t_sigmoid = np.zeros(SIGMOID_TABLE_SIZE)

for i in range(SIGMOID_TABLE_SIZE):
    x = (i / SIGMOID_TABLE_SIZE * 2 - 1) * MAX_SIGMOID
    t_sigmoid[i] = 1 / (np.exp(-x)+1.)


def sigmoid(x):
    if x >= MAX_SIGMOID:
        return 1.
    elif x <= -MAX_SIGMOID:
        return 0.
    else:
        return t_sigmoid[(int)((x + MAX_SIGMOID) * (SIGMOID_TABLE_SIZE / MAX_SIGMOID / 2))]

sigmoid(x=0.)  # 0.5
sigmoid(x=0.7) # 0.66541055874681398
sigmoid(x=10.) # 1.0
```

`(i / SIGMOID_TABLE_SIZE * 2 - 1) * MAX_SIGMOID`は、index`i`を`-MAX_SIGMOID`から`MAX_SIGMOID`を`SIGMOID_TABLE_SIZE-1`に等分割したときの`i`番目の実数値に変換している。
当然だが、`sigmoid(x)`の最終行は、これの逆変換になっている。

### その他

$$exp(x)$$ の高速計算は[exp(x)の高速計算 ～理論編～](http://www.chokkan.org/blog/archives/320)を読んで理解したいと思いました。

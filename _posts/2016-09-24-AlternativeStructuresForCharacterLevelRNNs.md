---
layout: post
title: "Alternative structures for character-level RNNs"
date: 2016-09-24 18:00:00 +0900
comments: false
abstract: 文字単位のRNNの論文紹介
---

### メタデータとか

Piotr Bijanowski, Tomas Mikolov, Armand Joulinの[論文](https://research.facebook.com/publications/alternative-structures-for-character-level-rnns/)．
First authorがFAIRでインターンしてたときの成果をICLR2016に出したもの．

1行要約:
文字単位のRNNの学習がうまくいくような拡張

### 本題

##### 表記

- $$d$$ : ユニークな文字数
- $$k$$ : ユニークな単語数
- $$t, p$$ : 時刻
- $$c_t$$ : 時刻 $$t$$ における文字のone-hot表現
- $$w_p$$ : 時刻 $$p$$ における単語のone-hot表現
- $$\mathbf{A}$$ : $$ \mathbb{R}^{ m \times d} $$ の重み行列
- $$\mathbf{R}$$ : $$ \mathbb{R}^{ m \times m} $$ の重み行列
- $$h_t$$ : 時刻 $$t$$ の隠れ層
- $$y_t$$ : 時刻 $$t$$ の予測値 (: 時刻 $$t+1$$ の文字)
- $$z_t$$ : 現在予測している文字を含む単語の1時刻前のRNNの中間層$$g_{p-1}$$．実験では200次元．
- $$\mathbf{Q}$$ : $$ \mathbb{R}^{ m \times ?} $$ の重み行列．
- $$g_p$$ : 時刻 $$p$$ における中間層
- $$n_t$$ : n-gramのone-hot表現．ただし，$$N$$ 個未満十分な頻度のあるn-gramのみ．(nzw: 違うかもしれない)

----

##### ベースとなるモデル

次の文字を予測する際の中間層の計算は次のようになる．


$$h_t = \sigma(\mathbf{A} c_t + \mathbf{R} h_{t-1})$$


このモデルでは，文字が単位なので記憶する長さが単語単位と比較して長くなりやすい．
中間層を十分にとれば単語単位のモデルと同じくらいの学習ができるが，計算量が増えるため好ましくない．
というわけで2つのモデルを提案しているのがこの論文．

##### Conditioning on Words

提案モデルの1つ目．

中間層の式を次のようにして単語の情報も利用する．

$$h_t = \sigma(\mathbf{A} c_t + \mathbf{R} h_{t-1} + \mathbf{Q} z_{t})$$

ベースとなるモデルでは文字についてのRNNしかなかったが，ここでは単語についてのRNNも加えている．
$$z_{t}$$ は，$$c_{t}$$ を含んでいる単語 $$w_p$$ の一つ前の単語 $$w_{p-1}$$ における単語RNNの中間層である．

単語の情報をすべて使うとsoftmaxの計算が重いので，
階層softmaxを使い，かつ単語は頻度順に3000~5000単語くらいしか使わないものとする．

##### Conditioning Prediction on Recent History

Conditioning on Wordsでは単語のRNNを加えたが，それをしないのが提案モデルの2つ目．
ここでは，学習するパラメータの少ない文字だけのRNNを使いつつ文脈情報を加えるために，n-gramを使う．
中間層は，ベースとなるモデルのままで，出力層の計算にn-gramのone-hot表現 $$n_t$$ をかける．
ただし，$$n_t$$ として複数のn-gramが該当する場合は，長い方を優先．

$$y_t = f(n_t^{T} \mathbf{U} h_t)$$

ただし，$$\mathbf{U}$$ はテンソル．

##### 実験

特徴だけまとめると

- 同じ実行時間の文字RNNよりもentropyが小さい
- 2つ目のモデルは，文字RNNと比較して中間層が200-500で変えた時に落ち幅が少ない

### 雑感

テンソル $$U$$ がよくわかっていない．

### 余談

ICLR2015で今回紹介した1つ目のネットワークと類似した構造のネットワークが提案されている
([Learning Longer Memory in Recurrent Neural Networks](https://research.facebook.com/publications/learning-longer-memory-in-recurrent-neural-networks/))．

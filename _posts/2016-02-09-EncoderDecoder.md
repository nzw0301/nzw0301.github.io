---
layout: post
title: "Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation"
date: 2016-02-09 13:15:00 +0900
comments: false
---

#### はじめに
（このページは研究室の輪講のために作成されたページです．）

[青深層学習の7章](http://amzn.to/1T9JfPS) で系列データに対して使われるRNNを扱いました．
本ではCTCを使って，入出力で系列長の異なるデータへの対応をしました（読んでる限りは入力系列より短くはできるが長くはできないような）．

この [EMNLP2014](http://arxiv.org/pdf/1406.1078v3.pdf) の論文では，encoder–decoderの提案とLSTM likeなユニット，機械翻訳での実験しています．（word embeddingsも少し出てきます）

nzwは機械翻訳について全くの素人であるので，モデル自体の話しかしません．
また詳しいslideは [slideshare](http://www.slideshare.net/yutakikuchi927/learning-phrase-representations-using-rnn-encoderdecoder-for-statistical-machine-translation) で菊池さんのが非常にわかりやすいのでこちらをお勧めします．

論文で提案されているencoder–decoderの用途は，

1. 入力系列から出力系列の生成
2. 入出力の系列ペアのスコアリング

#### 本題

まずタイトルの用語の説明をしますと

- encoder：可変長の入力系列を固定長ベクトルに変換するRNN
- decoder：固定長ベクトルを可変長の系列データに変換するRNN

となります．


論文の図1の例で説明すると，



![nn]({{ site.url }}/images/model.png)

- \\(\mathbf{x}_{1}\\) ：1単語に対応するone–hotベクトル
- \\(\mathbf{c}\\) ：固定長ベクトル
- \\(\mathbf{y}_{1}\\) ：1単語に対応するone–hotベクトル


##### encoderの計算
\\(\mathbf{h}\_{\langle t \rangle}\\) は時刻\\(t\\) におけるencoderの白いユニット部分の値です．

計算式はRNNなので以下のようになります．

\begin{eqnarray}
\mathbf{h}\_{\langle t \rangle} = f( \mathbf{h}\_{\langle t-1 \rangle} , x\_t)
\end{eqnarray}

関数 \\(f\\) はロジスティックシグモイドとかLSTMなどをおけます．

encoderのRNNは，青い本のRNNとほぼ同じ形です．

##### decoderの計算
\begin{eqnarray}
\mathbf{h}\_{\langle t \rangle} = f( \mathbf{h}\_{\langle t-1 \rangle} , y\_{t-1}, c)
\end{eqnarray}

\\(\mathbf{h}\_{\langle t \rangle}\\) は時刻\\(t\\) におけるdecoderの白いユニット部分の値です．

出力層の計算は

\begin{eqnarray}
p(y\_{t}|y\_{t-1},y\_{t-2},...,y\_{1},\mathbf{c}) = g(\mathbf{h}\_{\langle t \rangle}, y\_{t-1}, \mathbf{c})
\end{eqnarray}

となります．


#### LSTM likeなRNNの隠れ層のユニット

LSTMよりもシンプルで似た働き（記憶と忘却）を持たせるために導入します．

これが1ユニット

![nn]({{ site.url }}/images/encoder-decoder-unit.png)

- \\(r\\)：reset gate，確率値で0に近いほど前の層の情報\\(h\\)を無視，頻繁に活発化すれば短期記憶
- \\(z\\)：update gate，確率値で前の層の情報をどれだけ今の層に伝えるか，ずっと活性化していれば長期記憶

###### encoderの計算再び

\begin{eqnarray}
h^{\langle t \rangle}\_{j} &=& z\_{j} h\_{j}^{\langle t \rangle} + (1-z\_{j}) \tilde{h}^{\langle t \rangle}\_{j} \\\
\tilde{h}^{\langle t \rangle}\_{j} &=& tanh( [ \mathbf{W} e(\mathbf{x}\_t) ]\_j + [\mathbf{U}(\mathbf{r} \odot \mathbf{h}\_{\langle t-1 \rangle})]\_j ) \\\
z\_j &=& \sigma( [\mathbf{W}\_z e(\mathbf{x}\_t)  ]\_j + [\mathbf{U}\_z \mathbf{h}\_{\langle t-1 \rangle})]\_j) \\\
r\_j &=& \sigma( [\mathbf{W}\_r e(\mathbf{x}\_t)  ]\_j + [\mathbf{U}\_r \mathbf{h}\_{\langle t-1 \rangle})]\_j), \\\
\mathbf{c} &=& tanh(\mathbf{V} \mathbf{h}^{\langle N \rangle})
\end{eqnarray}


###### decoderの計算再び

初期値は \\(\mathbf{h}'^{\langle 0 \rangle} tanh(\mathbf{V}' \mathbf{c})\\)


\begin{eqnarray}
h'^{\langle t \rangle}\_{j} &=& z'\_{j} h\_{j}'^{\langle t-1 \rangle} + (1-z'\_{j}) \tilde{h}'^{\langle t \rangle}\_{j} \\\
\tilde{h}'^{\langle t \rangle}\_{j} &=& tanh( [ \mathbf{W}' e(\mathbf{y}\_{t-1}) ]\_j + \mathbf{r}'[\mathbf{U}'\mathbf{h}'\_{\langle t-1 \rangle}) + \mathbf{Cc}] ) \\\
z'\_j &=& \sigma( [\mathbf{W}'\_z e(\mathbf{y}\_{t-1})  ]\_j + [\mathbf{U}'\_z \mathbf{h}'\_{\langle t-1 \rangle})]\_j + [\mathbf{C}\_z \mathbf{c}]\_j) \\\
r'\_j &=& \sigma( [\mathbf{W}'\_r e(\mathbf{y}\_{t-1})  ]\_j + [\mathbf{U}'\_r \mathbf{h}'\_{\langle t-1 \rangle})]\_j + [\mathbf{C}\_r \mathbf{c}]\_j), \\\
p(y\_{t,j} = 1 | \mathbf{y}\_{t-1}, ..., \mathbf{y}\_1 \mathbf{X}) &=& \frac{exp(\mathbf{g}\_j \mathbf{s}\_{\langle t \rangle})}{\sum\_{j'=1}^{K} exp(\mathbf{g}\_{j'} \mathbf{s}\_{\langle t \rangle})} \\\
s\_{\langle t \rangle} &=& max ( s'^{\langle t \rangle}\_{2i-1}, s'^{\langle t \rangle}\_{2i} ) \\\
s'^{\langle t \rangle} &=& \mathbf{O}\_h \mathbf{h}'^{\langle t \rangle} + \mathbf{O}\_y \mathbf{y}\_{t-1} + \mathbf{O}\_c \mathbf{c}
\end{eqnarray}
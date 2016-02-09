---
layout: post
title: "Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation"
date: 2016-02-09 13:15:00 +0900
comments: false
---

#### はじめに
このページは研究室の輪講のために作成されたページです．

[青深層学習の7章](http://amzn.to/1T9JfPS) でRNNを扱いました．
本ではCTCを使って，入出力で系列長の異なるデータへの対応をしました（読んでる限りは入力系列より短くはできるが長くはできないような）．

この [EMNLP2014](http://arxiv.org/pdf/1406.1078v3.pdf) の論文では，encoder–decoderの提案，LSTM likeなユニットの提案，それらを使った英仏のフレーズ翻訳のタスクでの評価実験しています．（word embeddingsも少し出てきます）

nzwは機械翻訳について全くの素人であるので，モデル自体の話しかしません．
また詳しい話は菊池さんの [slideshare](http://www.slideshare.net/yutakikuchi927/learning-phrase-representations-using-rnn-encoderdecoder-for-statistical-machine-translation) が非常にわかりやすいのでこちらをお勧めします．

#### 本題

まずタイトルにあるencoder–decoderを別々に説明すると，

- encoder：可変長の入力系列を固定長ベクトルに変換するRNN
- decoder：固定長ベクトルを可変長の系列データに変換するRNN

です．

構造自体はシンプルです．
まずencoderでは，入力系列（例えば，英語のフレーズ）を時刻ごとに受け取り，入力系列の最後まで入力したら固定長ベクトルの1つに変換します．
次にdecoderでは，encoderで求めた固定長ベクトルとdecoder部分のRNNを使って時刻ごとに単語を1つずつ出力していき，文末を表す記号を出力するまで繰り返します．


論文の図1では下がencoder，上がdecoderになります．

![nn]({{ site.url }}/images/model.png)

このとき，

- \\(\mathbf{x}\\) ：1単語に対応するone–hotベクトル
- \\(\mathbf{c}\\) ：固定長ベクトル
- \\(\mathbf{y}\\) ：1単語に対応するone–hotベクトル

です．

encoder–decoderの用途は，

1. 入力系列から出力系列の生成
2. 入出力の系列ペアのスコアリング

と言及されています．

##### encoderの計算
\\(\mathbf{h}\_{\langle t \rangle}\\) は時刻\\(t\\) におけるencoderの白いユニット部分の値です．

計算式はRNNなので以下のようになります．

\begin{eqnarray}
\mathbf{h}\_{\langle t \rangle} = f( \mathbf{h}\_{\langle t-1 \rangle} , x\_t)
\end{eqnarray}

関数 \\(f\\) はロジスティックシグモイドやLSTMなどをおけます．
この論文ではLSTM likeなユニットを導入しているので，それが\\(f\\)に対応します．

encoderのRNNは，青い本のRNNとほぼ同じ形です．

##### decoderの計算
\begin{eqnarray}
\mathbf{h}\_{\langle t \rangle} = f( \mathbf{h}\_{\langle t-1 \rangle} , y\_{t-1}, \mathbf{c})
\end{eqnarray}

\\(\mathbf{h}\_{\langle t \rangle}\\) は時刻\\(t\\) におけるdecoderの白いユニット部分の値です．
encoderと異なり，\\(\mathbf{c}\\)が隠れ層に常に関係してきます．


出力層の計算は

\begin{eqnarray}
p(y\_{t}|y\_{t-1},y\_{t-2},...,y\_{1},\mathbf{c}) = g(\mathbf{h}\_{\langle t \rangle}, y\_{t-1}, \mathbf{c})
\end{eqnarray}

となります．
確率値にしたいので，\\(g\\)には，例えばsoftmax関数が使われます．


#### LSTM likeなRNNの隠れ層のユニット

LSTMよりもシンプルで似た働き（記憶と忘却）を持たせるために導入しています．

これが1ユニットです（LSTMの1メモリユニットに相当）．

![nn]({{ site.url }}/images/encoder-decoder-unit.png)

- \\(r\\)：reset gate，確率値で0に近いほど前の層の情報\\(h\\)を無視，頻繁に活発化すれば短期記憶
- \\(z\\)：update gate，確率値で前の層の情報をどれだけ今の層に伝えるか，ずっと活性化していれば長期記憶
- \\(\mathbf{x}\\)：入力ベクトル
- \\(\mathbf{h}\\)：このユニットが出力する値
- \\(\mathbf{\tilde{h}}\\)：hの計算に使う値

#### appendixの詳しい式の紹介

###### encoderの計算再び
入力系列\\(\mathbf{x}\\)から
固定長ベクトル\\(\mathbf{c}\\)を求めるまでの計算式です．


\begin{eqnarray}
h^{\langle t \rangle}\_{j} &=& z\_{j} h\_{j}^{\langle t-1 \rangle} + (1-z\_{j}) \tilde{h}^{\langle t \rangle}\_{j} \\\
\tilde{h}^{\langle t \rangle}\_{j} &=& tanh( [ \mathbf{W} e(\mathbf{x}\_t) ]\_j + [\mathbf{U}(\mathbf{r} \odot \mathbf{h}\_{\langle t-1 \rangle})]\_j ) \\\
z\_j &=& \sigma( [\mathbf{W}\_z e(\mathbf{x}\_t)  ]\_j + [\mathbf{U}\_z \mathbf{h}\_{\langle t-1 \rangle})]\_j) \\\
r\_j &=& \sigma( [\mathbf{W}\_r e(\mathbf{x}\_t)  ]\_j + [\mathbf{U}\_r \mathbf{h}\_{\langle t-1 \rangle})]\_j), \\\
\mathbf{c} &=& tanh(\mathbf{V} \mathbf{h}^{\langle N \rangle})
\end{eqnarray}


- \\(z\_j\\)：隠れ層の\\(j\\)番目のユニットのupdate geteの確率値
- \\(r\_j\\)：reset geteの確率値
- \\(h^{\langle t \rangle}\_{j}\\)：時刻\\(t\\)の隠れ層の\\(j\\)番目のユニットの値
- \\(e\\)：word embeddingsの行列(このモデルで学習できる)
- \\(U\\)：前の層に対する重み
- \\(V\\)：入力系列を最後まで読みこんで計算した\\(h\\)にかかる重み
- \\(W\\)：入力系列の分散表現にかかる重み
- \\(\sigma\\)：ロジスティクスシグモイド関数

###### decoderの計算再び

初期値は \\(\mathbf{h}'^{\langle 0 \rangle} =  tanh(\mathbf{V}' \mathbf{c})\\)．


\begin{eqnarray}
h'^{\langle t \rangle}\_{j} &=& z'\_{j} h\_{j}'^{\langle t-1 \rangle} + (1-z'\_{j}) \tilde{h}'^{\langle t \rangle}\_{j} \\\
\tilde{h}'^{\langle t \rangle}\_{j} &=& tanh( [ \mathbf{W}' e(\mathbf{y}\_{t-1}) ]\_j + \mathbf{r}'[\mathbf{U}'\mathbf{h}'\_{\langle t-1 \rangle}) + \mathbf{Cc}] ) \\\
z'\_j &=& \sigma( [\mathbf{W}'\_z e(\mathbf{y}\_{t-1})  ]\_j + [\mathbf{U}'\_z \mathbf{h}'\_{\langle t-1 \rangle})]\_j + [\mathbf{C}\_z \mathbf{c}]\_j) \\\
r'\_j &=& \sigma( [\mathbf{W}'\_r e(\mathbf{y}\_{t-1})  ]\_j + [\mathbf{U}'\_r \mathbf{h}'\_{\langle t-1 \rangle})]\_j + [\mathbf{C}\_r \mathbf{c}]\_j), \\\
p(y\_{t,j} = 1 | \mathbf{y}\_{t-1}, ..., \mathbf{y}\_1 \mathbf{X}) &=& \frac{exp(\mathbf{g}\_j \mathbf{s}\_{\langle t \rangle})}{\sum\_{j'=1}^{K} exp(\mathbf{g}\_{j'} \mathbf{s}\_{\langle t \rangle})} \\\
s\_{\langle t \rangle} &=& max ( s'^{\langle t \rangle}\_{2i-1}, s'^{\langle t \rangle}\_{2i} ) \\\
s'^{\langle t \rangle} &=& \mathbf{O}\_h \mathbf{h}'^{\langle t \rangle} + \mathbf{O}\_y \mathbf{y}\_{t-1} + \mathbf{O}\_c \mathbf{c}
\end{eqnarray}

'がついているものはencoderと同様です．

- \\(s\\)：maxout関数で計算
- \\(O\\)：出力層への入力にかかる重み
- \\(C\\)：固定長ベクトル\\(\mathbf{c}\\)の重み
- \\(g\\)：重み行列\\(G\\)の要素


#### その他，nzw的に興味があった箇所

word embeddingsがこれでも学習できるらしく，上の式で出てきた\\(e\\)を可視化した図が出てきている．
NGやsubsampligがないのでw2vの両モデルほど良い結果は出ないと思うけど，お得感がある．


あと\\(\mathbf{c}
\\)を可視化するとフレーズが近くにまとまる．
（なので，ベクトル\\(\mathbf{c}
\\)を求めることは，入力系列のフレーズを埋め込んでるかPCAみたいなことをしていることに相当している？）
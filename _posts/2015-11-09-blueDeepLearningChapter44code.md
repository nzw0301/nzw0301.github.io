---
layout: post
title: "青深層学習 4章 実装"
date: 2015-11-09 21:00:00 +0900
comments: false
---

# はじめに
前回まで数式の展開をしていたので，それをもとにして実装を行いました．

Pythonを使いました．

# データとタスク

データは例によって夢野久作の作品([オンチ](http://www.aozora.gr.jp/cards/000096/files/2122_21847.html))を使います．

1文が登場人物の発言なのか，地の文なのかの2値分類を行います．
活性化関数はすべてロジスティック関数，損失関数は対数尤度です．
（なので出力層のユニット数は1つ）

> tag sentence

> 1 退け 退け ッ 

> 0 疎ら に なっ た 群衆 の 背後 から 、 今 出 た ばかり の 旭 が キラキラ と 映し 込ん で 来 た 。 

このように地の文であれば0，発言であれば1をつけます．

# コード
`hidden_layer` で指定する層を変えても問題ないように作ってあるので層の増減とユニット数の増減は好きに試すことができます．

<script src="https://gist.github.com/nzw0301/363b803268c2ece127f2.js"></script>


テストデータは作ってないので，パラメータによる誤差関数の変動のグラフをみて投稿を締めようかと思います．

上記のコード
1つ目がミニバッチを使った確率的勾配法
2つ目が全データで学習する勾配法

![nn]({{ site.url }}/images/nn_err_rate.svg) 


学習回数`400`，学習率`0.2`で固定し，隠れ層をいじってみます．
![nn]({{ site.url }}/images/nn_hidden.svg) 

学習率`0.2`と隠れ層を固定し，確率的勾配法を使います．
ミニバッチによる変化を見ています．
![nn]({{ site.url }}/images/nn_minibatch.svg) 


以上です．
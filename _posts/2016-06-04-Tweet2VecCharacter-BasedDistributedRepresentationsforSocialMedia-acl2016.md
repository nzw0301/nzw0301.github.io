---
layout: post
title: "Tweet2Vec: Character-Based Distributed Representations for Social Media"
date: 2016-06-03 02:00:00 +0900
comments: false
---

#### はじめに
Dhingra, B, et al. ACL2016のaccepted paper ([preprint](http://arxiv.org/abs/1605.03481))

Google ScholarのAlertで引っかかったので軽く目を通した論文．
[Lasagneの実装](https://github.com/bdhingra/tweet2vec)を公開している．

最近Kerasのモデル書いてなかったので，実装もした．

#### 本題

tweetからhashtagを分類するNNを学習している（ので Hashtag tweet to Vector では？）．

tweetは低頻度語や単語の表記が崩れていて素性として使いにくいので，文字単位でRNNにかける．
文字単位で扱ってもtweetの140文字の制限があるので，最長で140 time-step．
（単語と比べて前処理する手間が省けるのでこれは素晴らしいと思う．）


NNの構成は以下のとおり

- Character Lookup table
  - Embeddig
  - 仮に英語であればascii文字しかないので，word2vecのように大規模にならない
- Bi-GRU
  - tweetを前から処理するGRUと後ろから処理するGRUの2つ
  - その和をとり1つのベクトルに変換（これがtweetのEmbeddings）
- softmax
  - ユニークなhashtag数


[character2vec](http://arxiv.org/pdf/1508.02096v2.pdf)と似てると言及しているが，Lookup tableが1つなくなってBi-LSTMがGRUに置き換わった程度の違い．


評価は単語ベースのモデルに対してhashtagの予測を行っている．


#### 実装

著者実装の出力層をサッと眺めたが，softmaxだけでだったので，ラベルの分だけ学習データを冗長にしてみた．

テストとして自分のTweetを使ってみたところ，一応 `自然言語処理` といれたら `chainer` のhashtagを予測した（小規模だったので，うまくいってるのか微妙）．


<script src="https://gist.github.com/nzw0301/13dc8c51c513ab8738c01838af5bdddc.js"></script>


#### 余談

本筋には関係ないが，別のTweet2Vecをつい先日見つけた．

[Tweet2Vec: Learning Tweet Embeddings Using
Character-level CNN-LSTM Encoder-Decoder](http://socialmachines.media.mit.edu/wp-content/uploads/sites/27/2016/05/tweet2vec_vvr.pdf)

こっちはNNがより複雑な構成になっているし，hashtagが不要なので汎用性は高そう．
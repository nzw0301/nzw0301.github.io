---
layout: post
title: "Bag of Tricks for Efficient Text Classification"
date: 2016-07-19 03:20:00 +0900
comments: true
---

$# メタデータとか

FAIR所属のArmand Joulin, Edouard Grave, Piotr Bojanowski, Tomas Mikolovの[論文](https://arxiv.org/abs/1607.01759)．
Last authorはword2vecで有名なTomas Mikolov氏．

Mikolov氏が共著に入ってる論文は，高速化とか単純化をするモデルが多いと勝手に思っているが，これも高速化なモデルを提案している．

1行要約:
CNNでがんばるモデルと同じくらいの文書分類性能をモデルが3層のニューラルネットワークでも出せた．

## 本題

文書分類のタスクにおいて，CBoWをベースにしたモデル `fastText` の提案を行っている．
CBoWは，注目する1単語 (出力層) を前後 $$n$$ 単語 (入力層) の分散表現の平均ベクトル (中間層) で予測するモデルであった．

提案モデルは，CBoWの入力を文書中の単語のone-hotベクトル，出力を文書のラベルに変える (入力にn-gramも加えるとさらに性能が上がる) ．
出力層ではword2vecと同じく階層Softmaxを使うことで高速化を図っている．

実験では，CNNのモデルでは数日を要しているが， `fastText` では数分で学習が終わることが示されている．
あと，TF-IDF+SVMのモデルでもDLと近いような分類性能が報告されている．

## コード

気になったのでKeras実装してみた．
階層Softmaxを組みたくないため，出力層が `sigmoid` 関数で済む2値分類で比較する．
ちょうど[Kerasのサンプルコード](https://github.com/fchollet/keras/blob/master/examples/imdb_cnn.py) に映画レビューの2値分類があるので，これを使う．

<script src="https://gist.github.com/nzw0301/227c23fa5a7dc463a6bda44eee00d720.js"></script>

サンプルのCNNでは2epochでval accuracyが0.88であった (1epoch あたりTesla K40で 7sec CPUでは 70sec)．
単語だけを使った `fastText` では，1epochが1sec (CPUでは 9~10sec)でCNNと同じtest accuracyに達するまでに6epochを必要とした．
というわけで確かに高速．

## 雑感

CNNと比較すると指定するパラメータがEmbeddingsの次元数だけで，とりあえずで試せるので重宝しそう．

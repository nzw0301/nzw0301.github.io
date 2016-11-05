---
layout: post
title: "Neural Architecture Search with Reinforcement Learning"
date: 2016-11-05 00:00:00 +0900
comments: false
abstract: CNNとRNNのユニット構造をRNNで求める
---

### メタデータとか


Barret Zoph, Quoc Leの[論文](http://openreview.net/forum?id=r1Ue8Hcxg)．
ICLR2017のレビュー中の論文．
Twitterでみかけたので読んだ．

論文の図がわかりやすい．

### 本題

深層学習ではネットワークの構造をどうやって決めるかという課題がある．
この論文では，RNNと強化学習を使ってCNNとRNNのユニット構造を自動的に求める．

この学習法は，2つのネットワークから構成される．

- Controller: RNN（2層のLSTM）．学習するNNのパラメータを求める
- Child network: Controllerのパラメータを使うNN．分類などのタスクはこっちで学習．

Contollerは，child networkのパラメータを単語に見立てて強化学習する．
Child networkは，contollerで得られたパラメータを使って学習する（CIFAR10とか）．
Contollerの強化学習の報酬は，child networkのaccuracy．
Contorllerで学習と予測，予測したパラメータでchild networkを学習してaccuracyを求める，ということを繰り返す．

##### CNNの構造

例えば，CNNの1層目のフィルタの高さがcontrollerの$$t_0$$の単語で，1層目のフィルタの幅が$$t_1$$の単語とみたてて学習する．
つまりCNNの1パラメータの1単語とし，ネットワーク全体のパラメータをシーケンスとして扱っている．

フィルタだけではなく，poolingをどこにいれるかやresidual blockでどこをつなぐかというのも学習できる．

##### RNNのユニット

CNNとほぼ同じで，入力の活性化関数の種類を$$t_0$$の単語，1時刻前の隠れ層と入力層の値を加算するか積算するかという操作を$$t_1$$の単語に見立てて，contorllerを学習する．
LSTMのようにメモリセルに対する操作も学習．

### その他

GPU800個使っている．

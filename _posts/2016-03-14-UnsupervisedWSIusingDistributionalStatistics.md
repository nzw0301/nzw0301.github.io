---
layout: post
title: "Unsupervised Word Sense Induction using Distributional Statistics"
date: 2016-03-14 13:15:04 +0900
comments: false
---

#### メタデータ
Kartik Goyal, Eduard Hovy. COLING2014の[論文](http://www.aclweb.org/anthology/C14-1123)．

nzwは，LDAの部分が気になったので，その部分をかいつまんで説明します．

#### 本題

WSIのタスクに2つの手法を提案していて，その1つにLDAを使用．
モデルの拡張はせずに[Blei+ 2003]のままで，データを工夫．

SemEVal2010のデータセットのnoun,verb50単語づつを対象．
学習データは，google 5-gram．

##### 学習データの作り方

- 5-gramを使って共起行列を作る
- 対象語が5-gramで共起する語（共起行列の対象語の列で非0要素）をfirst order とする
- first orderと5-gramで共起する語をsecond order とする
- first orderを文書，first orderの単語をsecod orderとみなしてLDA
- first orderについたトピック分布にk-meansかけてクラスタを語義とする
- 品詞はいくつか限定

#### 気になったこと

- トピック数とk-meansのクラスタ数をどう決めるか
  - 追ってる範囲のsotaは階層型かつnonparametricなLDA
- LDA全体にいえるが，大規模になったときにこの手法だと動かない
  - 大規模なcorpusだとsecond orderがでかくなるので死ぬ
  - nzwが青空文庫で全品詞で試したら助詞とか"する"がハブになって文書長が長くなりやすい

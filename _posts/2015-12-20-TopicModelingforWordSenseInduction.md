---
layout: post
title: "Topic Modeling for Word Sense Induction"
date: 2015-12-20 13:18:00 +0900
comments: false
---

#### 概要

`Word Sense Induction`（WSI）のタスクに`LDA`を使ってみましたという[2013年のGSCLの会議論文](http://publications.wim.uni-mannheim.de/informatik/lski/Knopp13TopicModelingforWSI.pdf)． 

WSIでは，出現した単語ごとの文脈などを単位としてベクトルを作り，それを`k-means`でクラスタリングすることで，出現した位置における語義を分けられるかというやり方がある．
トピックが語義に対応しているという仮定して，そのベクトルを作る際に`LDA`で得られるトピックごとの単語の確率分布\\(\phi\\)を使ってやろうというもの．
なので`LDA`を拡張したわけではないのでわりと直感的である．（`gensim`+`scikit-learn`+`NLTK`さえあればできそう）


#### 気になったこと

- トピック数が`3~10`と比較的とかなり小さい(この分野ではそうなんだろうか)
- 評価には`WordNet`と`SeｍEval2010`を使ってる（名詞と動詞だけで評価，評価指標は`F-score`と`V-measure`）
- クラスタリングの手法は複数試したほうが良さそう（WSIのsurveyでいくつ言及あり）

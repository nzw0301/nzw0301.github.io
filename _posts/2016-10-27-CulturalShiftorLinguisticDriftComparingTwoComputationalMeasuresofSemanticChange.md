---
layout: post
title: "Cultural Shift or Linguistic Drift? Comparing Two Computational Measures of Semantic Change"
date: 2016-10-27 00:00:00 +0900
comments: false
abstract: 分散表現を使って意味の変化について考える
---

### メタデータとか

[William L. Hamilton](http://stanford.edu/~wleif/), [Jure Leskovec](https://cs.stanford.edu/people/jure/), [Dan Jurafsky](http://web.stanford.edu/~jurafsky/)の[論文](https://arxiv.org/abs/1606.02821)．
EMNLP2016に通っている．
first authorがACL2016に関連した論文を出しており，その応用という印象．


### 本題
Word embeddingsを使って単語の時間的な意味変化を扱う研究はあるが，意味変化にもいろいろな種類があるのでそれについてword embeddingsを使って考える．
ここでは以下の2種類の意味変化の原因を考える．

1. cultual
  - 科学技術の発展とかで意味が変化
  - 名詞に多い
  - ex. *cell*

1. linguistic
  - 言語学のgrammaticalization(文法化), subjectificationなどがこれに該当
  - 動詞に多い
  - ex. *I promise* -> *It promised to be*

論文では，

1. 上の2つに対応するような尺度を考える
2. 時間ごとにつくったword embeddingsを作る
3. 品詞を説明変数に入れた線形回帰を行う

という流れ．
2と3は先行研究でやっていることなので，提案しているのは1の部分．

##### 時間ごとに作ったword embeddings

著者の[histwords](http://nlp.stanford.edu/projects/histwords/)を使う．
これは，SGNGを使って時間$$t$$ごとに学習したEmbeddings $$\mathbf{w}_{i}^{t}$$ を得る手法．

##### 尺度
2単語間がどれくらい離れているかを表す．
2種類の計算方法があり，1つ目はglobal shifts（これは前から提案されているもの）．
分散表現が似ているほど右辺は小さくなることから，意味的な距離は小さくなる．

時刻$$t$$と時刻$$t+1$$での単語$$w_i$$の距離は以下で定義される．

$$d^G(w_i^{t}, w_i^{t+1}) = 1-cos(\mathbf{w}_i^{t}, \mathbf{w}_i^{t+1})$$


2つ目が提案手法で，local shifts．

$$d^L(w_i^{t}, w_i^{t+1}) = 1-cos(\mathbf{s}_i^{t}, \mathbf{s}_i^{t+1})$$

$$\mathbf{s}^{t}(j) = cos(\mathbf{w}_i^{t}, \mathbf{w}_i^{t+1}),  \forall w_i \in {\cal N}_k (w_i^{(t)})  \cup  {\cal N}_k (w_i^{(t+1)})  $$

$$\mathbf{s}^{t}(j)$$は，要素値に類似度もつ最小で$$k$$次元のベクトルになる．
$${\cal N}_k (w_i^{(t)})$$は，$$cos$$類似度の上位$$k$$単語の集合．
今回は，$$k=25$$．

##### 線形回帰

以下の3つの説明変数を用いて，上記の2つの尺度を従属変数として線形回帰を行う．

- 頻度
- 品詞
- 時間

実験結果では，2つの尺度に対して品詞の係数について比較している．
比較の結果として，「名詞はlocal，動詞はglobalな尺度に対して高い係数を持っている」ということ．


以下，個人的な解釈．

ある動詞の意味変化は2時刻間のembeddingsの$$cos$$が小さいほど，意味変化している．
ある動詞が新しい意味をもったり，文法化するといろんな単語と共起するようになるので，embeddingsが全体として変化する．
例えば， *It promised to be* とかはいろんな単語と出てきたり，これまであった言い回しに影響を与えるため．

対して名詞は，周囲の単語との$$cos$$のずれが大きいほど意味変化しているという結果であった．
例えば *人工知能* という単語について考えてみる．

現代の *人工知能* の意味が10年前の *人工知能* の意味としては，違うとしても *人工知能* によって我々の文法などは大きく変化することはなく，あくまで *人工知能* という単語の周囲の共起情報が変わっただけに過ぎない．
なので，局所的な類似度と名詞との関係が強いような結果なのではないだろうか．

### 所感

Embeddingsは頻度情報をけっこうもっているので，高頻度語も変化するため，globalがいいのかもしれない．

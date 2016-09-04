---
layout: post
title: "Enriching Word Vectors with Subword Information"
date: 2016-09-03 22:20:00 +0900
comments: false
abstract: 分散表現の論文紹介
---

### メタデータとか

FAIR所属のPiotr Bojanowski, Edouard Grave, Armand Joulin, Tomas Mikolovの[論文](https://arxiv.org/pdf/1607.04606v1.pdf)．


1行要約:
skip-gramの単語ベクトルの作り方を変えたら低頻度語とOOVに対応できるようになった．

実装はfasttextに入ってる．


### 本題

単語自体にmorphologicalな (語形?) 情報 ([^ex]) が含まれる．
それをskip-gramに組み込むのがこのモデル．

skip-gramは注目する単語からその周囲に出現する単語を予測するようなNNを学習することで単語ベクトルを得る．
このモデルでは，入力側の単語の作り方をskip-gramから少し変える．

どうするかというと，
skip-gramにおける入力ベクトルを単語に含まれる文字 $$n$$ -gramの和ベクトルとする．

論文にはないが，例をあげるならば，
たとえば $$n=3$$ とする場合， $$word$$ のベクトルは以下の3-gramのベクトルの和として扱う．

\begin{eqnarray}
word  = \<s\>wo  + wor  + ord  + rd\<e\>
\end{eqnarray}

ここで $$<s>$$ と $$<e>$$ はそれぞれ単語の開始記号と終了記号を表す文字である．

これによって $$n$$ -gramさえあれば単語ベクトルが構築できるようになるので，未知語（OOV）や低頻度語の問題に対処できる．
欠点としては，和ベクトルを作る処理が増えるので学習に時間がかかる（論文ではskip-gramの約1.5倍かかるとのこと）


### 雑感

skip-gramの課題というか欠点に低頻度語に弱いという話があったので，それをカバーしたskip-gramとしてみれるかもしれない．

[^ex]: 例えば[~tion: 名詞, ~ed: 過去形, sub~: 部分的] といったものだと思う．

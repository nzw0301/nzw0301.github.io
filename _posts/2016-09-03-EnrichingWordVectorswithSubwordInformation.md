---
layout: post
title: "Enriching Word Vectors with Subword Information"
date: 2016-09-03 22:20:00 +0900
comments: true
abstract: 分散表現の論文紹介
---

### メタデータとか

FAIR の Piotr Bojanowski, Edouard Grave, Armand Joulin, and Tomas Mikolovの[論文](https://arxiv.org/pdf/1607.04606.pdf)．TACLに通ってる．

1行要約:
skip-gramの単語ベクトルの作り方を変えたら低頻度語とOOVに対応できるようになった．

実装は[fasttext](https://fasttext.cc/)に入ってる．

### 本題

単語自体にmorphologicalな (語形?) 情報 ([^ex]) が含まれる．それをskip-gramに組み込むのがこのモデル．

skip-gramは注目する単語からその周囲に出現する単語を予測するようなNNを学習することで単語ベクトルを得る．このモデルでは，入力側の単語の作り方をskip-gramから少し変える．

どうするかというと，skip-gram における入力ベクトルの計算に、単語に含まれる文字 $$n_{min} – n_{max}$$ gram のベクトルを加える．

例えば $$n_{min}=3, n_{max}=6$$ とする場合， $$word$$ の単語ベクトルは以下で定義される [^code]．

$$
\begin{aligned}
    word =& (\mathbf{h}_{word} + <wo  + wor  + ord  + rd> + <wor + word + ord> + <word + word> + <word>) / 11
\end{aligned}
$$

ここで $$<$$ と $$>$$ はそれぞれ単語の開始記号と終了記号を表す文字．

これによって $$n$$-gram さえあれば単語ベクトルが構築できるようになるので，未知語（OOV）や低頻度語の問題に対処できる．欠点としては，学習に時間がかかる（論文では skip-gram の約 1.5 倍かかるとのこと）

この論文のあとに同チームが学習したモデルを157言語くらい配布したり，embeddings の圧縮した論文があったりでいろいろありがたい.

[^ex]: 例えば[~tion: 名詞, ~ed: 過去形, sub~: 部分的] といったものだと思う．
[^code]: [ここ](https://github.com/facebookresearch/fastText/blob/b5b7d307274ce00ef52198fbc692ed3bd11d9856/src/model.cc#L50) で `input.size()` で割ってて、[ここ](https://github.com/facebookresearch/fastText/blob/b5b7d307274ce00ef52198fbc692ed3bd11d9856/src/dictionary.cc#L201)で subwords 変換前の単語が `inputs` に追加されている．

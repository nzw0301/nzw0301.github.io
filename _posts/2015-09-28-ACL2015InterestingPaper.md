---
layout: post
title: "ACL 2015で気になったもの一覧"
date: 2015-09-28 16:30:00 +0900
comments: false
---

タイトルの通りである．

論文の一覧は [ここ](http://www.aclweb.org/anthology/P/P15/ "ACL paper list")

#  [SENSEMBED:Learning Sense Embeddingsfor Word and Relational Similarity](http://www.aclweb.org/anthology/P/P15/P15-1010.pdf "pdf link")
単語の意味のレベルで分散表現の獲得．意味のついたでかいコーパスがないので，WSDのstate-of-artsな手法を使う


# [Learning Continuous Word Embedding with Metadata for Question Retrieval in Community Question Answering](http://www.aclweb.org/anthology/P/P15/P15-1025.pdf "pdf link")

コミュニティQAサイトで過去に出た質問を探すために，分散表現をQAのタグやカテゴリと一緒に学習する．Skim-gram（word2vecに実装されてるやつ）の拡張．レシピでも同じことできそうだなぁと思った．（類似レシピを探して嬉しいかどうかはよくわからないけど）

# その他アブスト読んだけどぱっと説明できなかったもの
[Gaussian LDA for Topic Models with Word Embeddings](http://www.aclweb.org/anthology/P/P15/P15-1077.pdf "link")

LDAの多項分布をガウス分布を使う手法．word embeddingsとの関係がいまいちつかめなかったので後で読む気がする

knowledge Graph系2つ，もう一個はあったけどクラウドソーシング使ってて多分違うのでリストから外した．

- [Knowledge Graph Embedding via Dynamic Mapping Matrix](http://www.aclweb.org/anthology/P/P15/P15-1067.pdf)
- [Semantically Smooth Knowledge Graph Embedding](http://www.aclweb.org/anthology/P/P15/P15-1009.pdf)

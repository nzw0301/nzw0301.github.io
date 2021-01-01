---
layout: post
title: Attention
comments: True
abstract: 論文メモ？
lang: ja
---


Attentionがよくわからんので、とりあえずfastTextに当ててみて感じを知りたくなるわけです。

前世で、重複コミュニティ抽出をやってたのでとこのあたりは少し既視感がでてきます。
soft attention はsoftmaxかけてるので、重み付き平均、あるいは、その重みに多項分布（あるいはカテゴリカル分布）をおいてるわけなので、そのシーケンスの中で、相対的な重要度を出してるわけです。
それよりは各単語に対してBernoulli 分布をおいてみたくなるわけです。softmaxは性質業、argmaxを取った形になりやすいので、
まぁ、もちろんこれはこれであるわけです（Yoon Kim!）が、実装して比べてみましょうという気持ちです。

ちなみに、とりあえずAttentionが解釈できるものかというとそうでもないというので[]()、解釈できる！といわれるいうブログをみると、cherry pickingっぽいなという気持ちと、ついでにattentionをあくまで当てさせつつ騙すadversarial attack なりfakeモデルもありそうだなとか思いました。

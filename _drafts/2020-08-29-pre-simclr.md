---
layout: post
title: "SimCLRの細かいところについて"
---

## はじめに

SimCLRという CPC のロスベースのシンプルかついい感じに動く self-supervised represention learning のアルゴリズムがあります。再実装していて、可視化等したくなった部分があるので、少し書きたいと思います。



## 学習率

linear vs squared

念の為に用語を明確にしておくと、`epoch` は、1通り全バッチを見たらインクリメントされる値で、`iteration`は、ミニバッチを1単位としてインクリメントする値とします。
なので、学習データが $$50\,000$$ でミニバッチサイズが $$100$$ とすれば、1 epochあたり 500 iterations になります。

学習率ですが、まず最初の10エポックはlinear-warmup をします。
どうするとかというと

です。10エポックが終わったら、その点を初期値として、cosine annelying をします。このとき、restartはしないので、単調減少します。

初期値の $$lr$$ epoch ごと学習率の変化を描くとこんな感じになります。


## Data-augmentation

ImageNet-1K は大変なので、ここでは論文でも言及されている CIFAR-10 を例にします。
まず元画像をclipしてresizeします。
次に確率50%で左右反転をします。
その後確率0.8でcolor dissortをして、その結果に対して確率0.2でグレイスケールに変換します。

どういう画像ができるかというとこういう画像が生成されます。

## feed-forwardingをどうするか

SimCLRでは、$K$の画像をサンプルしてきてから、それぞれに対してdata-augmentationを2回適用、2つの変換結果を作ります。
このため、iterationごとに$$2K$$ のデータを扱います。
lossを見ても分母には、$$2K-1$$ sumをとります。

では、この$$2K$$ のミニバッチをどう扱うかですが、これらのconcatしてひとまとめにしたデータを特徴量変換すればfeed-forwardが一回で済むので少し速そうですし、逆に$K$ ごとに2回feed-forwardに流すことも考えられます。
特にSimCLRのresnetでは、BatchNormalizationが入っているので、この処理は2回通す方が自然です。（$$2K$$ の場合がもともと同じ画像から2通りのdata augmentationを適用していて、ミニバッチ内のサンプルが独立でなくなるためで、BatchNormalizationの使い方としてはよくありません。2Kでやるとしたらlayer normalization、Batch re-normalizationとかnon-iidの場合を考慮した手法に置き換えることも考えれますし、事実SimCLRではそのように言及されています。類似手法では、別のnormalisation が使われています。）

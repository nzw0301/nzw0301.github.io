---
layout: post
title: "Learning Features by Contrasting Natural Images with Noise"
abstract: NCEの最初の論文
---

### メタデータとか

- 著者: M. Gutmann and A. Hyvärinen
- 投稿先: International Conference on Artificial Neural Networks
- 出版年: 2009
- 論文: [pdf](https://www.cs.helsinki.fi/u/ahyvarin/papers/Gutmann09ICANN.pdf)

NCE という negative sampling の上位クラス的なアルゴリズムがあり，それの一番最初の論文．
この論文の段階では， Noise Contrastive Estimation ではなく， Contrastive feature learning として提案されている．

余談で，2nd authorはICA関係で有名．

I. Goodfellow et al. の GAN か T. Mikolov et al. の Negative sampling を知ってると理解しやすい．

### 本題

文脈としては，画像データに ICA をかけたいという状況を考える:

$$\mathbf{x} = \sum_{i=1}^N \mathbf{a}_i s_i $$

このとき，
- $$\mathbf{x}$$: natural image
- $$\mathbf{a}$$: basic feature
- $$s$$: latent variable

これを学習するときに，計算コストが高いケースがあるので，それを避けるというのがこの研究のモチベーション．

Contrastive feature learning では， neural network の重みベクトルが上記の $$\mathbf{a}$$ に対応するような2値分類問題に置き換える．
正例に natural images を与える場合，負例としては natural images の特徴をある程度含んだ画像を与える．
これらに対する2値分類器は，正例と負例に共通しない特徴で natural images を当てようとするので，そのときの重みがよい $$\mathbf{a}$$ になるだろうと仮定．

---

前述したとおり，入力画像 $$\mathbf{x}$$ が natural images か reference data かの2値分類器 $$r$$ を考える [^1]．

$$r(\mathbf{x}) = \frac{1}{1 + \exp(-y(\mathbf{x}))}$$

これは，入力画像に関数 $$y$$ を適用したものに logistic sigmoid function をかけているだけ．
このとき，ロス関数は binary cross entoropy を選ばれる．
また，関数 $$y$$ は非線形変換とする．

$$y(\mathbf{x}) = \sum_{m=1}^{M} g(\mathbf{w}_m^{T} \mathbf{x} + b_m) + \gamma $$

このとき $$g$$ は非線形関数 ($$tanh$$ とか $$sigmoid$$) ．関数 $$y$$ は入力層を含めるなら1層の neural network として見ることもできる．

さて，natural images としては MNIST や CIFAR10 ， ImageNet など既にあるが，reference data をどうやって用意するかを考える必要がある [^2]．
ここでは，ICA の文脈なので natural image の特徴をとらえた $$w$$ を学習できるような reference data を用意する．
ここでは，入力データと同じ共分散をもつ同数のデータを使う．
共分散が同じなので，オリジナルの入力とある程度似た表現をもつ負例になる．

論文では，非線形関数 $$g$$ にいくつかバリエーションを持たせて学習している．
対称の sigmoid function か パラメータを学習した非線形関数が分類性能と $$\mathbf{w}$$ をみると良かったらしい．
一方で sigmoid と tanh でははっきりとした表現 $$w$$ は得られなかったとのこと．

[^1]: GANでいえばDiscriminator．
[^2]: GANでいえばGenerator，word2vec tool の negative sampling でいえば noise 分布 (unigram 分布を $$3/4$$ 乗した分布)

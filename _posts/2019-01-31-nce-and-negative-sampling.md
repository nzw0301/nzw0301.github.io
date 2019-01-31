---
layout: post
title: Noise Contrastive Estimation と Negative Sampling
comments: True
abstract: 論文メモ
lang: ja
---

単語の分散表現を学習するときに softmax を使ったモデリングをすると分母の計算が遅いので NCE や Negative sampling といった高速な手法が使われます。この2つは、式が似ており [Notes on Noise Contrastive Estimation and Negative Sampling](https://arxiv.org/abs/1410.8251) で

> This objective can be understood in several ways. First, it is equivalent to NCE when $$k = \mid V \mid$$ and $$q$$ is uniform.

と言っています。ここでの `This objective` は negative sampling を指します。微妙に違う別の解釈が個人的にあったので書きます。ちなみに上記の引用のあとに別の解釈もありますが、この記事はまた別です。

## 前準備

#### Continuous Skip-gram model [[^1]]

単語 $$w_t$$ が与えられたとき、その周囲の単語 $$w_c$$ を予測するように単語ベクトルを学習するモデルです。予測は softmax を使って

$$
p(w_c \mid w_t) = \frac{\exp(\mathbf{u}_{w_t}^{\top} \mathbf{v}_{w_c})}{\sum_{v \in \mathcal{V}} \exp(\mathbf{u}_{w_t}^{\top} \mathbf{v}_{v})},
$$

とされます。ただし、$$\mathbf{u}$$ と $$\mathbf{v}$$ は学習する単語ベクトルです。これを使って負の対数尤度

$$
\begin{align}
    \mathcal{L}_{SG} = - \sum_{t=1}^T \sum_{w_c \in \mathcal{C}_t} \ln p(w_c \mid w_t),
\end{align}
$$

を最小化するように単語ベクトルを学習します。ただし、$$T$$ は学習する系列長で $$\mathcal{C}_{t}$$ は単語 $$w_{t}$$ の文脈語を含んだ bag-of-words です。

#### Negative sampling [[^2]]

Skip-gram の softmaxの計算が重いので、negative sampling loss を考えます。
Skip-gram の negative sampling loss は以下のように定義されます：

$$
\begin{align}
    \mathcal{L}_{SGNS} = 
    - \sum_{t=1}^T \sum_{w_c \in \mathcal{C}_t} \left[
        \ln \sigma \left( \mathbf{u}_{t}^\top \mathbf{v}_{w_c} \right)
        + \sum_{w_n \in \mathcal{NS}}  \ln \sigma \left( - \mathbf{u}_{t}^\top \mathbf{v}_{w_n} \right)
    \right],
\end{align}
$$

ただし、

- $$\sigma$$ : logistic sigmoid function
- $$\mathcal{NS}$$: $$k$$ 個の負例単語の bag-of-words で ノイズ分布 $$p_n$$ から i.i.d. にサンプルされます
    - この実装である `word2vec` では $$w_c$$ が正例のときは $$w_c$$ は $$\mathcal{NS}$$ に含みません。
- 第2項目はサンプル近似

#### Noise Contrastive Estimation (NCE) [[^3]]

NCE 自体はいろんな分布の近似に使えるものですが、ここでは単語ベクトルの学習時に出てくる softmax の近似のために使います。
この辺りは [[^4]] と [[^5]] が最初の論文だと思います。

NCE では正規化項（今回は softmax の分母）をパラメータだと思って推定します。あとで対数をとって評価するので、まず対数をとって

$$
\ln p(w_c \mid w_t) = \mathbf{u}_{w_t}^{\top} \mathbf{v}_{w_c} - \ln \sum_{v \in \mathcal{V}} \exp(\mathbf{u}_{w_t}^{\top} \mathbf{v}_{w_v}),
$$

これの第2項目を $$c_{w_t}$$ とした式を $$s(w_c, w_t)$$ とします：

$$s(w_c, w_t) = \mathbf{u}_{w_t}^{\top} \mathbf{v}_{w_c} - c_{w_t}.$$

単語ベクトルに加えてこの $$c_{*}$$ も学習します。これを使って NCE を使った損失関数は以下のように定義されます：

$$
\begin{align}
    \mathcal{L}_{NCE} &= 
    - \sum_{t=1}^T \sum_{w_c \in \mathcal{C}_t} \left\{
        \ln \sigma [\Delta s(w_c, w_t)]
        + k \mathbb{E}_{w_n \sim p_n} \ln \sigma \left[ - \Delta s(w_n, w_t) \right]
    \right\}, \\
    \Delta s(w_c, w_t) &= s(w_c, w_t) - \ln [k p_n(w_c)], \\
\end{align}
$$

2項目を $$k$$ 個の負例を使ったサンプリング近似を考えると、最終的には以下のような損失関数を最小化します：

$$
\begin{align}
    \mathcal{L}_{NCE} &= 
    - \sum_{t=1}^T \sum_{w_c \in \mathcal{C}_t} \left\{
        \ln \sigma [\Delta s(w_c, w_t)]
        + \sum_{w_n \in \mathcal{NS}} \ln \sigma \left[ - \Delta s(w_n, w_t) \right]
    \right\}.
\end{align}
$$

### 本題

引用に戻ると

> This objective can be understood in several ways. First, it is equivalent to NCE when $$k = \mid V \mid$$ and $$q$$ is uniform.

とありますが、$$k = \mid V \mid$$ がひっかかります（それなら計算量が softmax と同じだし…）。ここにいたるために、NCE が経験的に $$c_{w_t}$$ を $$1$$ としてもちゃんと学習してくれることを使っています。それをしないで考えてみます。

定義に従って代入すると、

$$
\begin{align}
\Delta s(w_c, w_t) &= s(w_c, w_t) - \ln [k p_n(w_c)],\\
                   &= \mathbf{u}_{w_t}^{\top} \mathbf{v}_{w_c} - c_{w_t} - \ln [k p_n(w_c)],
\end{align}
$$

なので $$ c_{w_t} = \ln [k p_n(w_c)]$$ のとき、negative sampling と等しくなります。このときノイズ分布 $$p_n$$ が uniform でなくても成立します。

### その他

NCE や negative sampling のような softmax の近似方法は `深層学習による自然言語処理` で触れられています。

<center>
<a href="https://www.amazon.co.jp/dp/4061529242/ref=as_li_ss_il?ie=UTF8&linkCode=li3&tag=algebrae-22&linkId=50f99a975d15751085eb23c1e0719a5c&language=ja_JP" target="_blank"><img border="0" src="//ws-fe.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=4061529242&Format=_SL250_&ID=AsinImage&MarketPlace=JP&ServiceVersion=20070822&WS=1&tag=algebrae-22&language=ja_JP" ></a><img src="https://ir-jp.amazon-adsystem.com/e/ir?t=algebrae-22&language=ja_JP&l=li3&o=9&a=4061529242" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</center>


$$c=1$$ としても学習することを `self-normalization` とか言います。ちなみにこれだと安定しないらしく $$c=9$$ にしたりとか色々なヒューリスティックが提案されています。


間違えてたらおしえてください [@twitter](https://twitter.com/nozawa_kento)。


---

### References

[^1]: Tomas Mikolov, Greg Corrado, Kai Chen, and Jeffrey Dean. **Efficient Estimation of Word Representations in Vector Space**. In _ICLR Workshop_, 2013.
[^2]: Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. **Distributed Representations of Words and Phrases and their Compositionality**. In _NeurIPS_, 2013.
[^3]: Michael U. Gutmann and Aapo Hyvärinen. **Noise-Contrastive Estimation of Unnormalized Statistical Models, with Applications to Natural Image Statistics**. _JMLR_, 2012.
[^4]: Andriy Mnih and Koray Kavukcuoglu. **Learning Word Embeddings Efficiently with Noise-contrastive Estimation**. In _NeurIPS_, 2013.
[^5]: Andriy Mnih and Yee Whye Teh. **A Fast and Simple Algorithm for Training Neural Probabilistic Language Models**. In _ICML_, 2012.

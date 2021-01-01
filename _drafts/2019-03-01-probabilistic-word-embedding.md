---
layout: post
title: 単語の確率的分散表現
comments: True
abstract: 論文メモ
lang: ja
---

久しぶりに論文のメモを書きます。
別にナウいやつではないのですが、まぁやっていく感じで。

### はじめに

[T. Mikolov et al., 2013] で有名になった分散表現ですが、単語は1つのベクトルで表現されます。この記事で紹介する論文は、そうではなく、分布でそれを表現しようというものです。
単語を分布で表現する理由としては、単語の意味的なものは文脈などに応じて曖昧さがあり、
例として、1単語をガウス分布で表現する場合、多義的な単語は分散が大きく、一方で意味が限定的な単語の分散は小さくしたほうが表現としては自然な感じがします。
[revise]


| Paper   |  Model   |   Distribution   |
|:-------:|:--------:|:----------------:|
|         | word2vec | Gaussian         |
|         | word2vec | Gaussian Mixture |
|         | fastText | Gaussian Mixture |

ICLRの論文が一番最初で、わりとこれが一番ベースとなります。2つ目の論文は、[徐さんが最先端NLP勉強会で使われた発表スライド](https://www.slideshare.net/liyuanxu1/multimodal-word-distribution)があります。


### おわりに

各単語のprotetype数をいくつにするかという話があって、
紹介した論文では $$K = 2, 3$$ とされていました。ノンパラベイズで単語ごとに割り当てるベクトルをいくつにするかとい話はもちろんあるんですが、
stochastic variational inferenceとかで近似計算入れる必要があったりします。自然な拡張な気がしますしそのうち、誰かが公開しそうな気がします。
AISTATSとかであるので、これとmixtureモデルを組み合わせれば単語ごとに推定はできそうな気がします。



## 前準備
#
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



間違えてたらおしえてください [@twitter](https://twitter.com/nzw0301)。

---

### References

[^1]: Tomas Mikolov, Greg Corrado, Kai Chen, and Jeffrey Dean. **Efficient Estimation of Word Representations in Vector Space**. In _ICLR Workshop_, 2013.
[^2]: Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. **Distributed Representations of Words and Phrases and their Compositionality**. In _NeurIPS_, 2013.
[^3]: Michael U. Gutmann and Aapo Hyvärinen. **Noise-Contrastive Estimation of Unnormalized Statistical Models, with Applications to Natural Image Statistics**. _JMLR_, 2012.
[^4]: Andriy Mnih and Koray Kavukcuoglu. **Learning Word Embeddings Efficiently with Noise-contrastive Estimation**. In _NeurIPS_, 2013.
[^5]: Andriy Mnih and Yee Whye Teh. **A Fast and Simple Algorithm for Training Neural Probabilistic Language Models**. In _ICML_, 2012.

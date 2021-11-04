---
layout: post
title: skip-gram と何かが等価な話
comments: True
abstract: skip-gram as なにか
lang: ja
---

## 前置き

Tomas Mikolov et al. の Skip-gram with negative sampling (word2vecの一部) がなんなのかを理解したい研究がいくつかあります。

一番有名なものは、Omer Levy and Yoav Goldberg の [Neural Word Embedding
as Implicit Matrix Factorization](https://papers.nips.cc/paper/5477-neural-word-embedding-as-implicit-matrix-factorization.pdf) です。
仮定のもと skip-gram with negative sampling で得られるベクトルの内積が、 Shifted PMI の要素の近似する、という趣旨です。

さて、これにはいくつか問題があり、Prof. Arora が言及していたり、論文を見てわかるとおり、行列をどう分解したらこの表現が得られるかはこれだけではわかりません。また、単語ベクトルが高次元のケースを考えており、現実で使われる300次元のようなケースについては成立しません。事実、Shifted PPMI を SVD で分解していますが、analogy task (king - man + woman +~ queen のタスク) になるとけっこう差がついて負けます。ただし、similarity task では結果が近いです。

さて、このあとに Le et al. が行列分解と似てるという話をしています。（証明読みましたが、式9を具体的に計算すると間違ってるように思えるのと、ついでに実験が `min_count = 3000` とかになっていて、等価なのか？という感じで、個人的にはこれは違いそうな印象です。
この行列分解は頻度行列を二つのベクトルの内積で推定するような形をしています。replicated softmax っぽい形だそうです。

さて EACL では、without negative sampling が PCA と等価とした上でテンソル分解の拡張しています。これでは計算が重いので少し微妙です。
ちなみに、窓幅の位置ごとに独立させた文脈ベクトル（ $w$ を予測するとしたら $t-1 t-2$ は別の表現）を学習する話はMinh and がしていますが、彼らの結果を見るとしなくてもよいかもしれません。

最後が Andrew J. Landgraf and Jeremy Bellay の [word2vec Skip-Gram with Negative Sampling is a Weighted Logistic PCA](https://arxiv.org/abs/1705.09755) で、これは証明があってそうです。何を示したのかというと skip-gram with negative sampling で最小化している損失関数は weighted logistic PCA と等価であるという話です。式しかないので、実験的に動くかは不明です。

というわけで今回の記事は、これの実装です。

Hasimoto et al. TACL
では、同様にskip-gram with softmaxについての解析を行っています。
こちらも残念ながら、文脈窓幅が長い、という仮定が付きます（要確認）。現実問題としては2--10 くらいの値しかとらないので、これも等価といっていいのかちょっとわかりません。また、最適解がw=cのとき、という結果になっています。ちなみに、skip-gram with negative samplingに関しては、w=cの制約をつけると性能が悪くなるのでSGNSに関しては違いそうです。(See https://www.aclweb.org/anthology/E17-2025/)

最後にAroraですが[...]

## 本題
### Notation

- $$w, c$$: target word, context word
- $$\#(w, c)$$: the number of co-occurrence in the same window
- $$\#(w) = \sum_{c \in V} \#(w, c)$$
- $$\#(c) = \sum_{w \in V} \#(w, c)$$
- $$D = \sum_{w \in V} \sum_{c \in V} \#(w, c)$$ :

### Preliminaries

Some tutorials...
http://alexhwilliams.info/itsneuronalblog/2016/03/27/pca/

#### Principal Component Analysis (PCA)
Decompose co-variance matrix ... right?

$$ \left\|X - W C^{T}\right\|_{F}^{2}=\sum_{i=1}^{n} \sum_{j=1}^{p}\left(x_{i j}-\sum_{k=1}^{K} W_{i k} C_{j k}\right)^{2}$$

from http://alexhwilliams.info/itsneuronalblog/2016/03/27/pca/

### logistic PCA

???

[8] J. De Leeuw, “Principal component analysis of binary data by iterated singular value decomposition,” Computational Statistics and Data Analysis, vol. 50, no. 1, pp. 21–39, 2006.

See [9]  A. I. Schein, L. K. Saul, and L. H. Ungar, “A generalized linear model for principal component
analysis of binary data.,” in AISTATS, vol. 3, p. 10, 2003

$$\mathrm{maximize}_{\Theta} L$$

$$L = \sum_{i, j} \left[ X_{i, j} \log \sigma (\Theta_{i, j}) + (1 - X_{i, j}) \log (- \Theta_{i, j}) \right]$$

where $$\Theta_{i, j} = \log \left( \frac{p}{1-p} \right)$$

### Weighted logistic PCA

$$\ell() = \sum_w \sum_c \left[ n_{w, c} + k n_w P_D(c) \right] \left[ \frac{n_{w, c}}{n_{w, c} + k n_w P_D(c)} (\mathbf{v}_w^{\top} \mathbf{u}_c) - \log \left[1 + \exp(\mathbf{v}_w^{\top} \mathbf{u}_c) \right] \right]$$

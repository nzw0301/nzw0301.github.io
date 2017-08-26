---
layout: post
title: "joint topic modelのサンプリング式導出"
date: 2016-02-17 21:00:00 +0900
comments: false
---

#### はじめに
間違っていたら[nzw](https://twitter.com/nzw0301)までお願いします．


[トピックモデルによる統計的潜在意味解析](http://amzn.to/1Nbzlq3)の3章の周辺化ギブスサンプリングの式を参考にjoint topic modelのサンプリング式を導出します．
Joint topic modelよりもpolylingual topic modelの名前のほうが有名かもしれないです．

まずグラフィカルモデルを[Blei+, 2003](https://www.cs.princeton.edu/~blei/papers/BleiNgJordan2003.pdf)のものと合わせて示します．


Topic model
![gmodel]({{ site.url }}/images/topic_model.svg)

Joint topic model
![gmodel]({{ site.url }}/images/joint_topic_model.svg)

[Blei+, 2003](https://www.cs.princeton.edu/~blei/papers/BleiNgJordan2003.pdf)とほぼ同じ形をしていますが， 観測できる変数が1つ増え，それに合わせて潜在変数も増えています．

通常のLDAでは1つの文書集合が与えられますが，このモデルでは，さらにそれぞれの文書ごとに補助情報が与えられます．
補助情報ごとに $$N_{*}$$のプレートと$$\beta$$と$$\phi$$が増えます．

このようなデータの例としては，

- レシピの手順をひとまとめにしたもとを1文書とし，そのレシピについているつくれぽ
- 日本語のwikipediaの1記事と対応する英語のwikipedia1記事

などが挙げられます．
（WSIにこのモデルを使った論文では，context–windowとPOSを使っていました）

示したグラフィカルモデルでは$$N_{*}$$のプレートは2つですが，いくつでも増やせます．（wikipediaの例を使うと，`[英語, 日本語, ロシア語]` など）


#### 本題

『トピックモデルによる〜』のp55を踏襲します．

$$z_{d,i}^{1}$$ は1番目の文書集合の$$d$$番目の文書の$$i$$番目の単語のトピックです．
このとき$$w_{d,i}^{1}$$ は1番目の文書集合の$$d$$番目の文書の$$i$$番目の単語です．

同様に，$$z_{d,i}^{2}$$は2番目の文書集合の$$d$$番目の文書の$$i$$番目の単語のトピックで，$$w_{d,i}^{2}$$は2番目の文書集合の$$d$$番目の文書の$$i$$番目の単語です．
文書集合の要素に対応関係が取れていれば，対応する文書長は一致しなくても構いません．

$${\boldsymbol \beta}^1$$ は，1番目の文書集合の語彙数次元あるディリクレ分布のパラメータベクトル，$${\boldsymbol \beta}^2$$ は，2番目の文書集合の語彙数次元あるディリクレ分布のパラメータベクトルです．
$${\boldsymbol \beta}$$ の次元数は一致しなくても構いません．

このとき，周辺化ギブスサンプリングにおける$$z_{d,i}^{1}$$のサンプリング式を考えます．

\begin{eqnarray}
  p(z_{d,i}^{1}=k|
    w_{d,i}^{1}=v,
    \mathbf{W}^{1}\_{\backslash d,i},
    \mathbf{W}^{2},
    \mathbf{Z}^{1}\_{\backslash d,i},
    \mathbf{Z}^{2},
    {\boldsymbol \alpha},
    {\boldsymbol \beta}^{1},
    {\boldsymbol \beta}^{2})
  &=& \frac{p(z_{d,i}^{1}=k, w_{d,i}^{1}=v,
      \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2},
      | {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2})}
    {p(w_{d,i}^{1}=v,
      \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2},
      | {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2})} \tag{1}\\\
  & \propto & p(z_{d,i}^{1}=k, w_{d,i}^{1}=v,
      \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2},
      | {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2}) \tag{2} \\\
  &=& p(w_{d,i}^{1}=v |
      z_{d,i}^{1}=k,
      \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2},
      {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2}) \\\
    & &\times
      p(z_{d,i}^{1}=k,
      \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2}
      | {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2}) \tag{3} \\\
    &=& p(w_{d,i}^{1}=v |
      z_{d,i}^{1}=k,
      \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2},
      {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2}) \\\
    & &\times
      p(z_{d,i}^{1}=k|
      \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2}
      {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2}) \\\
    && \times
      p(\mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2}
      | {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2}) \tag{4} \\\
    & \propto & p(w_{d,i}^{1}=v |
      z_{d,i}^{1}=k,
      \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2},
      {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2}) \\\
    & &\times
      p(z_{d,i}^{1}=k|
      \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{W}^{2},
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2}
      {\boldsymbol \alpha},
      {\boldsymbol \beta}^{1},
      {\boldsymbol \beta}^{2}) \tag{5} \\\
    &=& \int p(w\_{d,i}^{1}=v|{\boldsymbol \phi}^1\_{k}) p({\boldsymbol \phi}^1\_{k}| \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{Z}^{1}\_{\backslash d,i},
      {\boldsymbol \beta}^{1})  d {\boldsymbol \phi}^1\_{k} \\\
    && \times  \int p(z_{d,i}^{1}=k|{\boldsymbol \theta}\_{d})
     p({\boldsymbol \theta}\_{d}|
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2},
      {\boldsymbol \alpha}) d {\boldsymbol \theta}\_{d} \tag{6} \\\
    &=& \int \phi\_{k,v}^{1} \times p({\boldsymbol \phi}^1\_{k}| \mathbf{W}^{1}\_{\backslash d,i},
      \mathbf{Z}^{1}\_{\backslash d,i},
      {\boldsymbol \beta}^{1})  d {\boldsymbol \phi}^1\_{k} \\\
    && \times  \int \theta\_{d,k} \times
     p({\boldsymbol \theta}\_{d}|
      \mathbf{Z}^{1}\_{\backslash d,i},
      \mathbf{Z}^{2},
      {\boldsymbol \alpha}) d {\boldsymbol \theta}\_{d} \tag{6} \\\
    &=& \mathbb{E}\_{p({\boldsymbol \phi}^1\_{k}| \mathbf{W}^{1}\_  {\backslash d,i},\mathbf{Z}^{1}\_{\backslash d,i},      {\boldsymbol \beta}^{1})}[\phi\_{k,v}^{1}]
    \mathbb{E}\_{p({\boldsymbol \theta}\_{d}|
      \mathbf{Z}^{1}\_{\backslash d,i}, \mathbf{Z}^{2},{\boldsymbol \alpha}) d {\boldsymbol \theta}\_{d}}[\theta\_{d,k}] \tag{7} \\\
    &=& \frac{n\_{k,v, \backslash d,i}^{1}+\beta^{1}\_{v}}{\sum\_{v'} (n\_{k,v', \backslash d,i}^{1}+\beta^{1}\_{v'})}
        \frac{n\_{d,k, \backslash d,i}^{1} + n\_{d,k}^{2} + \alpha\_k}{\sum\_{k'} (n\_{d, k', \backslash d,i}^{1} + n\_{d,k'}^{2} + \alpha\_{k'})} \tag{8}
\end{eqnarray}

$$z_{d,i}^{2}$$の場合も同様に求まります．

単語の分布($$\phi$$)は，文書集合ごとに別なので，トピックモデルと同じ式に帰着します．
$$\theta$$は，各文書集合の潜在変数$$z$$で繋がっていますが，ディリクレ分布の期待値計算から上記の式のように求まります．

#### 実行例
以下のような2つの文書集合を使ってみました．
それぞれ1行が1文書とみなし，行ごとに対応関係（この例では対訳のページ）であるとします．

- - -

> lisp lisp lisp scala scala scala clojure clojure

> java java java scala scala scala

> book book library library lisp lisp clojure clojure

> writing writing book book library library

> scala book lisp book java book clojure

> movie movie article article book book mars mars

> movie movie article article mars mars mars

- - -

> リスプ リスプ リスプ スカラ スカラ スカラ

> ジャバ ジャバ ジャバ スカラ スカラ スカラ

> 本 本 図書館 図書館 リスプ リスプ

> 書く 書く 本 本 図書館 図書館

> スカラ ジャバ リスプ 本 本 本

> 映画 映画 論文 論文 本 本 火星 火星

> 映画 映画 論文 論文 火星 火星 火星

- - -

トピック数3で実行したときの， $$\phi_{k,v}$$の確率値の高い単語の一覧を示します．

```
- 英語
  - topic=0
    - mars 0.382442748092
    - article 0.306106870229
    - movie 0.306106870229
  - topic=1
    - book 0.596688741722
    - library 0.265562913907
    - writing 0.133112582781
  - topic=2
    - scala 0.317194570136
    - lisp 0.271945701357
    - clojure 0.226696832579
    - java 0.181447963801

- 日本語
  - topic=0
    - 火星 0.382734912147
    - 論文 0.306340718105
    - 映画 0.306340718105
  - topic=1
    - 本 0.597084161696
    - 図書館 0.265738899934
    - 書く 0.133200795229
  - topic=2
    - スカラ 0.410181392627
    - リスプ 0.351667641896
    - ジャバ 0.234640140433
```

このときトピックは共通しているため（同じ$$\theta$$から$$z$$が生成されるため），言語が違っていても共通したトピックから生成される単語分布を求めることができます．

せっかくなので[Juliaでのコード](https://github.com/nzw0301/TopicModels.jl)を公開しました．

#### 参考資料
- [青いトピックモデル本で言及されているjoint topic modelの論文](http://dirichlet.net/pdf/mimno09polylingual.pdf)

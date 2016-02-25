---
layout: post
title: "SparseLDAの導出"
date: 2016-02-25 13:00:00 +0900
comments: false
---

#### はじめに
間違っていたら[nzw](https://twitter.com/nzw0301)までお願いします．



pythonでLDAの実装をしましたが，ちょっと遅すぎるので，周辺化ギブスサンプリングの高速化するSparse LDAの論文を読んで実装したと思いました．

モデル自体は
[Blei+, 2003](https://www.cs.princeton.edu/~blei/papers/BleiNgJordan2003.pdf)と等価で，サンプリング式の計算を工夫して早くするというものです．

![topicModel]({{ site.url }}/images/topic_model.svg) 



#### 本題

単語$$w$$にトピック$$z$$が割り当てられる確率は以下の式に比例する．

\begin{eqnarray}
p(z=t|w) \propto (\alpha\_{t} + n\_{t|d})  \frac{\beta + n\_{w|t}}{\beta V + n\_{\cdot|t}} \tag{5}
\end{eqnarray}

上の値を$$q(z)$$と表記し，以下の分布から実数値$$U$$をサンプルする．

\begin{eqnarray}
U \sim {\cal u}(0, \sum\_{z} q(z))
\end{eqnarray}

（日本語で書くと実数値$$U$$を一様分布$${\cal u}(0, \sum_{z} q(z))$$からサンプル．）

一様分布からサンプルした$$U$$を使って，以下の式を満たすような$$t$$をトピック$$z$$に割り当てる．

\begin{eqnarray}
\sum\_{z=1}^{t-1} q(z) < U < \sum\_{z=1}^{t} q(z)
\end{eqnarray}

ただし，これを順番に計算していく過程で$$\sum_{z} q(z))$$を計算する必要がありこれを軽くしたい．
後述するが，これを3つの場合わけにして計算しないように工夫する．


まず，式(5)を変形して依存関係をわかりやすくする．

\begin{eqnarray}
p(z=t|w) \propto
    \frac{\alpha\_{t}\beta}{\beta V + n\_{\cdot|t}}
 +  \frac{n\_{t|d}\beta}{\beta V + n\_{\cdot|t}} 
 +  \frac{(\alpha\_{t}+ n\_{t|d})n\_{w|t}}{\beta V + n\_{\cdot|t}} \tag{6}
\end{eqnarray}

- 第1項：全文書に対して固定
- 第2項：現在の単語タイプに対して独立


変形した結果から $$\sum_z p(z) = s+r+q$$ と表せる．

ただし，
\begin{eqnarray}
s &=& \sum\_{t} \frac{\alpha\_{t} \beta}{\beta V + n\_{\cdot|t}} \tag{7} \\\
r &=& \sum\_{t} \frac{n\_{t|d}\beta}{\beta V + n\_{\cdot|t}} \tag{8} \\\
q &=& \sum\_{t} \frac{(\alpha\_{t}+ n\_{t|d})n\_{w|t}}{\beta V + n\_{\cdot|t}} \tag{9} \\\ 
\end{eqnarray}

これによって3つに分解できる．

\begin{eqnarray}
U \sim {\cal u}(0, s+r+q)
\end{eqnarray}

##### if $$U < s$$ , "smoothing only" bucket

このときは式(7)の総和の中身 $$\frac{\alpha_{t} \beta}{\beta V + n_{\cdot|t}}$$ 
だけを順番に加算していく．

つまり以下を満たすような$$t$$を見つけることになる．

\begin{eqnarray}
\sum\_{z=1}^{t-1} \frac{\alpha\_{z} \beta}{\beta V + n\_{\cdot|z}} < U < \sum\_{z=1}^{t} \frac{\alpha\_{z} \beta}{\beta V + n\_{\cdot|z}}
\end{eqnarray}

たしかに$$r$$と$$q$$の部分を使わないので，計算量が減っている．

##### if $$s < U < (s+r)$$, "document topic" bucket

この場合は$$r$$に注目する．
$$r$$は，現在の単語が含まれる文書依存なので，文書に現れるトピック$$z$$だけを考慮すればよい．
$$n_{t|d} \neq 0$$ だけを走査はすればよい．

\begin{eqnarray}
\sum\_{z=1}^{t-1} \frac{n\_{t|d}\beta}{\beta V + n\_{\cdot|z}} < U-s < \sum\_{z=1}^{t} \frac{n\_{t|d}\beta}{\beta V + n\_{\cdot|z}}
\end{eqnarray}

トピック数$$T$$だけ走査する必要がなくなるので計算コストが下がる．

このあたりは参考文献[2]を見るとわかりやすい．

##### if $$(s+r) < U$$, "topic word" bucket

この項は，現在の単語依存する．
"document topic" bucketと似ていて，
$$n_{w|t} \neq 0$$だけを走査はすればよい．
これもトピック数$$T$$だけ走査する必要がなくなるので計算コストが下がる．

\begin{eqnarray}
\sum\_{z=1}^{t-1}
\frac{(\alpha\_{z}+ n\_{z|d})n\_{w|z}}{\beta V + n\_{\cdot|z}}
< U-(s+r) < 
\sum\_{z=1}^{t} 
\frac{(\alpha\_{z}+ n\_{z|d})n\_{w|z}}{\beta V + n\_{\cdot|z}}
\end{eqnarray}


#### $$s,r,q$$の計算
$$s,r,q$$の値を計算する必要がある．（一様分布のパラメータに出てくるため）

$$s$$はDicichlet分布のパラメータ$${\boldsymbol \alpha}$$が更新したときだけ更新．

$$r$$は，1つの文書をgibbs samplingで更新したら$$r$$を更新．

$$q$$はちょっと複雑になる．
まず，$$q$$を以下のように2つの項に分解する．

\begin{eqnarray}
\sum\_{t} \Bigl[\frac{\alpha\_{t}+ n\_{t|d}}{\beta V + n\_{\cdot|t}} \times n\_{w|t} \Bigr] \tag{10}
\end{eqnarray}


$$\frac{\alpha_{t} + n_{t \\| d}}{\beta V + n_{\cdot \\| t}}$$は，各トピックごとにキャッシュしておく．

キャッシュした項と$$n_{w\\|t} \neq 0$$の積で$$q$$を求めることができる．

また，ほとんどの文書$$d$$において$$t$$は，$$n_{t\\|d}=0$$であるのでキャッシュしておく項は，
$$\frac{\alpha\_{t}}{\beta V + n\_{\cdot|t}}$$
となる．
なので，更新する必要があるキャッシュは，その文書に割り当てられているトピック数が非零なトピックの部分だけなので更新が早い．


論文では，$$\alpha$$や$$\beta$$の値が小さいと約90%くらいは"topic word" bucketに落ちると言及している．
（例えば，ディリクレ分布のパラメータが全体的に小さいとのっぺりとした分布になるので，単語が特定のトピックが偏らないで配分されるので，"topic word" bucketに落ちるという認識をしました，また実際問題$$\beta$$と$$\alpha$$は小さい値になるのでこの特徴は重要）

このことから"word topic" bucketにかかる時間をより高速化したい．
ここで式(10)の中身は，$$n_{w\\|t}$$の比のように見えるので，
できるだけ，$$n_{w\\|t} \neq 0$$を満たすものを降順に求めることで
"topic word" bucketで示した大小関係を満たすトピックを見つけることができる．

そこで，($$t$$, $$n_{w\\|t}$$)のタプルを32bitsの整数で表現する．
1つの整数は，$$n_{w\\|t}$$とトピック番号の2つに分割する．
トピックに必要なビット数$$m$$は $$2^m \geq T$$で残りを頻度が使う．
（完全に余談だけど，ノンパラメトリックベイズのような場合はどうなるんだろうか）

- $$n_{w\\|t}$$を更新などするときは，$$n_{w\\|t}$$を$$m$$だけ左シフトしてトピックの番号だけ加算．
- $$n_{w\\|t}$$を読み出すときは，$$n_{w\\|t}$$を$$m$$だけ右シフトしてトピックの番号だけ減算．

単語ごとに上記のタプルの整数表記を要素に持つ配列に格納する．
ただし，$$n_{w\\|t} = 0$$は格納しない．

この構造のメリットは以下の2つ

1. 単語に対して，トピック数次元の配列を用意する必要がない
2. $$n_{w\\|t}$$は上位ビットなので，トピックを意識せずに頻度順にソートできる．


このデータ構造について具体的にみると，
トピック数$$T=64$$として，単語"book"がトピック1に3回，トピック16に10回配分されたとします．

- $$n_{book\\|t=1 } = 3$$.
- $$n_{book\\|t=16} = 10$$.

トピックの番号に使うビット数は，$m=6$

値の設定は

トピック番号1：bin((3<<6)+1) ==> 0b11000001 == 193
トピック番号2：bin((10<<6)+16) ==> 0b1010010000



#### 参考文献など

1. [Efficient methods for topic model inference on streaming document collections](http://dl.acm.org/citation.cfm?id=1557121)
1. [Efficient Inference for Multinomial Mixed Membership Models](http://mimno.infosci.cornell.edu/slides/fast-sparse-sampling.pdf)
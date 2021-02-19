---
layout: post
title: "SparseLDAの導出"
date: 2016-02-25 23:25:00 +0900
comments: false
---

### はじめに

間違っていたら[nzw](https://twitter.com/nzw0301)までお願いします．

pythonでLDAの実装をしましたが，遅くて使い物になりません．
そこで高速化するSparse LDAの論文を読んで実装したいと思いました．

モデル自体は[Blei+, 2003](https://www.cs.princeton.edu/~blei/papers/BleiNgJordan2003.pdf)と等価で，サンプリング式の計算を工夫して高速化します．![topicModel]({{ site.url }}/assets/img/topic_model.svg)

この論文の3.4を読んでまとめました．

### 本題

単語$$w$$にトピック$$z$$を割り当てる確率は以下の式に比例する．

$$
\begin{aligned}
p(z=t|w) \propto (\alpha_{t} + n_{t|d})  \frac{\beta + n_{w|t}}{\beta V + n_{\cdot|t}}
\end{aligned}
$$

上の値を$$q(z)$$と表記し，以下の連続一様分布から実数値$$U$$を1つサンプルする．

$$
\begin{aligned}
U \sim \mathcal{U}(0, \sum_{z} q(z))
\end{aligned}
$$

先の一様分布からサンプルした$$U$$を使って，以下の式を満たすような$$t$$をトピックとして単語$$w$$に割り当てる．

$$
\begin{aligned}
\sum_{z=1}^{t-1} q(z) < U < \sum_{z=1}^{t} q(z)
\end{aligned}
$$

ただし，これを順番に計算する必要があり，計算を軽くしたい．

まず，式(5)を展開して依存関係をわかりやすくする．

$$
\begin{aligned}
p(z=t \mid w) \propto \frac{\alpha_t\beta}{\beta V + n_{\cdot \mid t}} + \frac{n_{t \mid d}\beta}{\beta V + n_{\cdot \mid t}} + \frac{(\alpha_t+ n_{t \mid d})n_{w \mid t}}{\beta V + n_{\cdot \mid t}}
\end{aligned}
$$

- 第1項：全文書に対して固定
- 第2項：現在の単語タイプに対して独立

変形した結果から $$\sum_z q(z) = s+r+q$$ と表せる．

ただし，

$$
\begin{aligned}
s &= \sum_{t} \frac{\alpha_{t} \beta}{\beta V + n_{\cdot \mid t}} \\
r &= \sum_{t} \frac{n_{t \mid d}\beta}{\beta V + n_{\cdot \mid t}} \\
q &= \sum_{t} \frac{(\alpha_{t}+ n_{t \mid d})n_{w \mid t}}{\beta V + n_{\cdot \mid t}} \\
\end{aligned}
$$

以上より，$$U$$のサンプル式は以下のように書き換えることができる．

$$
\begin{aligned}
U \sim {\cal u}(0, s+r+q)
\end{aligned}
$$

---

以下ではこれらの項ごとに条件分岐を行う．

#### "smoothing only" bucket

$$U < s$$ のときは，式(7)の総和の中身 $$\frac{\alpha_{t} \beta}{\beta V + n_{\cdot \mid t}}$$
だけを順番に加算していく．

つまり以下を満たすような$$t$$を見つけることになる．

$$
\begin{aligned}
\sum_{z=1}^{t-1} \frac{\alpha_z \beta}{\beta V + n_{\cdot \mid z}} < U < \sum_{z=1}^{t}
\frac{\alpha_z \beta}{\beta V + n_{\cdot \mid z}}
\end{aligned}
$$

$$r$$と$$q$$の部分を使わないので，計算量が減っている．

#### "document topic" bucket

$$s < U < (s+r)$$のとき，$$r$$に注目する．
$$r$$は，現在の単語が含まれる文書依存なので，文書に現れるトピック$$z$$だけを考慮すればよい．
つまり，$$n_{t|d} \neq 0$$ だけを走査する．

$$
\begin{aligned}
\sum_{z=1}^{t-1} \frac{n_{t \mid d}\beta}{\beta V + n_{\cdot \mid z}} < U-s < \sum_{z=1}^{t} \frac{n_{t \mid d}\beta}{\beta V + n_{\cdot \mid z}}
\end{aligned}
$$

このあたりは参考文献[2]を見るとわかりやすい．

#### "topic word" bucket

if $$(s+r) < U$$のときは$$q$$の項に注目する．
この項は，現在の単語$$w$$に依存する．
"document topic" bucketと似ていて，
$$n_{w|t} \neq 0$$だけを走査はすればよい．

$$
\begin{aligned}
\sum_{z=1}^{t-1}
\frac{(\alpha_{z}+ n_{z \mid d})n_{w \mid z}}{\beta V + n_{\cdot \mid z}}
< U-(s+r) <
\sum_{z=1}^{t}
\frac{(\alpha_{z}+ n_{z \mid d})n_{w \mid z}}{\beta V + n_{\cdot \mid z}}
\end{aligned}
$$

条件分岐ここまで．

---

#### $$s,r,q$$の計算
一様分布のパラメータに出てくるため，
$$s,r,q$$の値を計算する必要がある．

- $$s$$はDicichlet分布のパラメータ$${\boldsymbol \alpha}$$が更新したら更新
- $$r$$は，1つの文書をgibbs samplingする前に一旦$$r$$を計算し，gibbs samplingで更新したら$$r$$を更新


$$q$$だけやや複雑になる．
まず，$$q$$を以下のように2つの項に分解する．

$$
\sum_{t} \Bigl[\frac{\alpha_{t}+ n_{t \mid d}}{\beta V + n_{\cdot \mid t}} \times n_{w \mid t} \Bigr]
$$

ここで，単語に依存しない$$\frac{\alpha_{t} + n_{t \mid d}}{\beta V + n_{\cdot \mid t}}$$は，各トピックごとにキャッシュしておく．キャッシュした項と$$n_{w \mid t} \neq 0$$の積から$$q$$を求められる．また，ほとんど$$n_{t \mid d}=0$$であるのでこのとき，キャッシュしておく項は，$$\frac{\alpha_{t}}{\beta V + n_{\cdot \mid t}}$$となる．なので，更新する必要があるキャッシュは，その文書に割り当てられているトピック数が非零なトピックの部分だけで済む．

---

論文では，$$\alpha$$と$$\beta$$の値が小さいと約90%くらいは"topic word" bucketに落ちると言及している．（例えば，ディリクレ分布のパラメータが全体的に小さいとのっぺりとした分布になるので，単語が特定のトピックが偏らないで配分されるので，"topic word" bucketに落ちるという認識をしました，また実際問題$$\beta$$と$$\alpha$$は小さい値なのでこの特徴は重要）

このことから"word topic" bucketにかかる時間を高速化する．ここで式(10)の中身は，$$n_{w \mid t}$$の比に見えるので，（できるだけ大きい方から計算したほうが見つかりやすいために）$$n_{w \mid t} \neq 0$$を降順に求めることで"topic word" bucketで示した大小関係を満たすトピックを速く見つける．

これについては，計算式ではなくて，データ構造を工夫する．($$t$$, $$n_{w \mid t}$$)のタプルを32ビットの整数で1つで表現する．この整数のビットを，$$n_{w \mid t}$$を割り当てる部分とトピック番号を割り当てる部分の2つに分割する．トピックに必要なビット数は，$$2^m \geq T$$をみたすようなで末尾$$m$$ビットで残りを$$n_{w \mid t}$$を表現するのに使用する．（完全に余談だけど，ノンパラメトリックベイズのような場合はどうなるんだろうか）

このデータ構造への操作は以下通りビット演算を使用する

- $$n_{w \mid t}$$を加える場合，$$n_{w \mid t}$$を$$m$$だけ左シフトしてトピックの番号だけ加算
- $$n_{w \mid t}$$とトピック$$t$$を読み出す場合
  - タプルの整数表記を$$m$$だけ右シフトして$$n_{w \mid t}$$を読み出す（右シフトすると$$t$$の情報が落ちる）
  - タプルの整数表記から下$$m$$桁を取り出すビットマスクをかけて，トピック番号を読み出す

単語ごとに上記のタプルの整数表記を要素に持つ配列に格納する．ただし，$$n_{w \mid t} = 0$$は格納しない．

この構造のメリットは以下の2つ

1. 単語に対して，トピック数次元の配列が不要
2. $$n_{w \mid t}$$は上位ビットなので，トピックを意識せずに頻度順にソート可能

これによってHashMapで同じ構造ことを行った場合と比べて2倍高速化したらしい．

このデータ構造について具体的にみてみる．トピック数$$T=60$$として，単語"book"がトピック1に3回，トピック16に10回配分されたとする．このとき，トピックの番号に使うビット数は，$$m=6$$である．

- $$n_{book \mid t=1 } = 3$$ .
- $$n_{book \mid t=16} = 10$$ .
- $$m=6$$ .

以下 `Jupyter` で計算する．

<script src="https://gist.github.com/nzw0301/660fd011197e9c0a3443.js"></script>

確かにトピック番号と$$n_{w \mid t}$$が取り出せている．

### 終わりに

これらを実装すればLDAが速くなります．

実装はそのうち上げると思います．

---

### 参考文献など

1. [Efficient methods for topic model inference on streaming document collections （論文）](http://dl.acm.org/citation.cfm?id=1557121)
1. [Efficient Inference for Multinomial Mixed Membership Models（スライド）](http://mimno.infosci.cornell.edu/slides/fast-sparse-sampling.pdf)

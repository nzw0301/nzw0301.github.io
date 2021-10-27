---
layout: post
title: "Understanding Negative Samples in Instance Discriminative Self-supervised Representation Learning の概要"
---


Self-supervised contrastive representation learningというのが2018年から流行っている表現学習の手法です。
有名な方法としては

- [CPC](https://arxiv.org/abs/1807.03748) / [CPC v2](https://arxiv.org/abs/1905.09272)
- [AMDIM](https://arxiv.org/abs/1906.00910)
- [MoCo](https://arxiv.org/abs/1911.05722) / [MoCo v2](https://arxiv.org/abs/2003.04297)
- [SimCLR](https://arxiv.org/abs/2002.05709)
- [SWaV](https://arxiv.org/abs/2006.09882) # Clustering ベースの方法ということもできますが、損失関数は上記の手法とほぼ同じ

というようにたくさんあります。negative samplingを使わないので、contrastive ではありませんが、発展系として[BYOL](https://arxiv.org/abs/2006.07733)/[SimSiam](https://arxiv.org/abs/2011.10566)/[Barlow Twins](https://arxiv.org/abs/2103.03230)/[VICReg](https://arxiv.org/abs/2105.04906)が2020年末からのself-supervised representation learningのトレンドです。


ものすごく大雑把にSelf-supervised contrastive representation learningで使われている損失関数を説明します。

- $$\mathbf{z}$$: 入力 $$\mathbf{x}$$にデータ拡張を施してから、何かしらの変換 $$\mathbf{f}$$ （ニューラルネットを使った特徴量抽出）をして得られる $$d$$ 次元の表現ベクトル
- $$\mathbf{z}^+$$: 入力 $$\mathbf{x}$$にデータ拡張を施してから、$$\mathbf{f}$$で得られる $$d$$ 次元の表現ベクトル（positive sampleといいます）
- $$\mathbf{z}^-$$: 別の入力にデータ拡張を施してから、$$\mathbf{f}$$で得られる $$d$$ 次元の表現ベクトル（negative sampleといいます）
- $$\mathbf{Z} = \{\mathbf{z}^+, \mathbf{z}^-_1, \ldots, \mathbf{z}^-_K \}$$: positive/negative samples をまとめたもの

とすると、$$\mathbf{z}$$に対するSelf-supervised contrastive representation learningの損失関数は、

$$
\ell(\mathbf{z}, \mathbf{Z}) = - \ln \frac{ \exp(\mathbf{z} \cdot \mathbf{z}^+ / t)}{
    \sum_{\mathbf{z}_k \in \mathbf{Z} }\exp(\mathbf{z} \cdot \mathbf{z}_k / t)
},
$$

で定義される[InfoNCE](https://arxiv.org/abs/1807.03748)です。論文間で多少の違いはありますが大まかにはだいたいこの損失関数を最小化します。MoCoやSimCLR論文を見るとnegative sample数（以下 $$K$$ ）を数千から数万を使って学習して得られる特徴量表現は、線形分類器の入力として使った時に、高い識別性能が報告されています。似たような設定の[contrastive unsupervised representation learningに対する理論解析](https://arxiv.org/abs/1902.09229)（以下CURL）では、$$K$$は小さい必要があるという解析結果があり、上記の現象とは反することを主張しています。

というわけで、この不一致を改善する論文, [Understanding Negative Samples in Instance Discriminative Self-supervised Representation Learning](https://arxiv.org/abs/2102.06866), を書きました。

---

なぜCURLが機能しないかを簡単に説明します。CURLを単純に上記の設定に適用すると、以下のようなlower boundが得られます（厳密な定義は論文の式8）。

$$
L_{\mathrm{Info}}(\mathbf{f}) = (1-\tau_K) L_{\mathrm{sub}}(\mathbf{f})
+ \tau_K \text{Collision} + d(\mathbf{f}),
$$

ただし、

- $$L_{\mathrm{Info}}(\mathbf{f})$$: InfoNCE $$\ell$$ のサンプル平均
- $$\tau_K$$: $$\mathbf{z}$$ のラベルが$$K$$ negative samplesのラベルと一致する確率（例えると、最初にガチャガチャを引いてから、追加で$$K$$ 回引いた時に最初に引いたものとダブる確率）
- $$L_{\mathrm{sub}}(\mathbf{f})$$: $$K$$ negative samplesの中でダブっているラベルを取り除いてから、残ったラベルを使って計算できる教師あり損失。$$K$$ によっては、解きたい教師ありタスクのクラス数よりも数が小さいので、教師ありクラスの部分集合に対する損失
- $$\text{Collision}$$: $$\mathbf{z}$$ のラベルが$$K$$ negative samplesのラベルと一致した数（ダブった数）
- $$d(\mathbf{f})$$: $$\mathbf{f}$$に依存する項。ここでの議論と関係がないので無視してください

このlower boundでは、例えば、$$L_{\mathrm{sub}}$$ で解きたいタスクのラベルを全て含むように$$K$$ を増やすと、$$\tau_K$$も増えるので、$$L_{\mathrm{sub}}(\mathbf{f})$$の係数が$$0$$に近づき、$$\text{Collision}$$が支配的になります。
しかし、教師あり損失と$$\text{Collision}$$は関係がないので、$$K$$が増えると教師ありの分類性能が落ちることが期待されます。冒頭で言及したように$$K$$は実験的には増やしても問題ないことが知られているので一貫していません。

---

### 貢献

上記の議論では$$\tau$$が厳しすぎるので、$$\tau$$を使わないlower boundを提案しました。具体的には、[Coupon collector's problem](https://en.wikipedia.org/wiki/Coupon_collector%27s_problem)の確率を使います。日本では、食玩問題やTeao分布でも検索すると出てきます。食玩問題を使うと上記の$$\tau$$に相当する確率が、$$K+1$$のサンプルの中で解きたいタスクのクラスを全て含まない確率になります。これにより、$$K$$を増やすことで意味のない項がlower boundで支配的にならなくなります。

$$K$$が小さい時の議論や、$$K$$が増えた時の影響についても議論していますが、ここでは省略します。camera-readyではNLPの実験も増える予定です。


## 余談

2019年12月くらいに、[CPC+InfoNCE](https://arxiv.org/abs/1807.03748)に対してCURLの解析ができないかどうかを考えはじめたのがはじまりでした。当時は別の論文の査読を待っていたり、UCL行く前にやっていてどこにも通っていない内容をどうしようか考えていると2020年の夏の終わりくらいになり、本格的にはじめました。2020年の夏の終わりというとすでにSimCLRとかMoCoとかBYOLとかSWaVが出てきて、手法が単純かつ性能がよいSimCLRに寄せたような記憶があります。CURL論文はUCL滞在時に[PAC-Bayesを使った拡張](https://arxiv.org/abs/1910.04464)をやっていて、CURLは普通の教師あり学習に対して理論解析が機能しないことがわかっていたので、self-supervised representation learningで観測されている事象とストーリーを合わせました。

## その他

<iframe width="560" height="315" src="https://www.youtube.com/embed/nK46OGjoosQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

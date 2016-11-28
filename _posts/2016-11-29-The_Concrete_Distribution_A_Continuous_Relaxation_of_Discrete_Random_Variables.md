---
layout: post
title: "The Concrete Distribution: A Continuous Relaxation of Discrete Random Variables"
date: 2016-11-29 00:00:00 +0900
comments: false
abstract: reparametarization trickの潜在変数を離散値にする
---

### メタデータとか


Chris J. Maddison, Andriy Mnih, Yee Whye Tehの
[論文](https://arxiv.org/abs/1611.00712)．
ICLR2017のレビュー中の論文．
最終著者のアラートで流れてきたので読んだ．

同じくICLR2017に投稿中の[Gumbel-Softmax](https://arxiv.org/abs/1611.01144)とほぼコンフリクトしてる．


### 本題

[VAE](https://arxiv.org/abs/1312.6114)で出てきたreparametarization trickは，ガウス分布とベルヌーイ分布に対して行われていた．
今回は，潜在変数 $$\mathbf{z}$$ を $$K$$ 次元のone-hotベクトル (深層学習では離散値はone-hotベクトルで表現されることが多いため) とする．
実際にはこれが複数あるが単純なケースとして1つの例で紹介する．
VAEで多変量ガウス分布の平均ベクトルと共分散行列の対角成分をencoderで求めたように，
カテゴリカル分布のパラメータをencoderで推定する．
推定するまではいいが，そのパラメータをもつカテゴリカル分布に従って離散値をサンプルし，one-hotベクトルを構成しなければならない．
とりあえず離散値をサンプルすることを考えると，
reparametarization trickと同様に単純な分布からサンプル値を構成する．
これには[第1著者らが過去にNIPSに通した論文](https://papers.nips.cc/paper/5449-a-sampling.pdf)の中でGumbel-Max trickと呼ぶ方法を使うことができる．
サンプルする離散値は， $$K$$ 次元ベクトルの正の実数
$$\boldsymbol{\alpha}$$
に対して
\begin{aligned}
argmax_{i} \big(G_i + \log \alpha_i  \big) \sim \frac{\alpha_i}{\sum_k \alpha_k }
\end{aligned}
によって構成できる．
Gumbel分布自体は
$$G_i \sim -log(-log(u))$$ , $$where$$ $$u \sim (U(0, 1)$$
という単純な分布のサンプルから計算できる．

Google 翻訳させてもnzwがよくわからなかったのだが，
$$argmax$$ だと $$\alpha_i$$ 対応する次元以外は0になってしまうので，
$$K-1$$ 次元については勾配が消えてしまうためGumbel-Max trickは今回の用途には不適切らしい．
そこで離散値をサンプルせずに直接one-hotベクトルを構成する _Concrete distribution_ を導入する．
\begin{aligned}
z_i =\frac{exp(\Big(\log(\alpha_i) + G_i) / \lambda \Big)}{ \sum_k \Big( exp(\log(\alpha_k) + G_i)/\lambda \Big)}
\end{aligned}
これが $$\mathbf{z}$$ の $$i$$ 要素となる．
$$\lambda$$ は _temperature_ で0に近いほどone-hotベクトルになり，
大きいほど離散一様分布のパラメータを要素に持つようなベクトルに近くなる．
よってone-hotベクトルの近似を求めている．

実験で使ってるネットワークは馴染みがないので読み飛ばした．


### その他

- 付録に証明やreparametarization trickのチートシートがあるので，参考になる
- VAEに限らず中間層で離散値がとれるはず
- VAEを離散値にしてKerasで試したところ，adam/nadamだとlossが `NaN` になってしまって厳しい気持ちになった

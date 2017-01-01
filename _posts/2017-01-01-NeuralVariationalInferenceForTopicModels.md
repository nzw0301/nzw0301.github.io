---
layout: post
title: "Neural Variational Inference For Topic Models"
comments: false
abstract: VAEでトピックモデル
---

### メタデータとか

Akash Srivastava, Charles Suttonの[論文](https://openreview.net/forum?id=BybtVK9lg)でICLR2017のレビュー中．ICLRの投稿論文の一覧を眺めていて面白そうだったので読んだ．[著者実装](https://github.com/akashgit/Neural-Variational-Inference-for-Topic-Models)も公開している．

数式はおってません．

### 本題

LDAの学習方法として有名なものはVariational BayesとCollapsed Gibbs samplingである．[VAE](https://arxiv.org/abs/1312.6114)は前者に対応するアルゴリズムなので．VAEを使ってLDAをやるのがこの論文．

encoderでは，LDAのパラメータ$$\theta$$を生成するDirichlet分布のパラメータを推定する．うまく$$\theta$$をreparametarization trickで構成できないので，Dirichlet分布をラプラス近似し，そのサンプルにSoftmax関数を適用することで$$\theta$$のサンプルとして代用する．これが貢献．ラプラス近似の詳細はここでは詳しく説明しないが，ある分布を正規分布で近似する方法．よって，多変量正規分布の平均ベクトルと共分散行列を推定する．事前分布を対称なDirichlet分布としているので，共分散行列は対角成分のみのベクトルとして推定する．VAE論文と違って，標準正規分布を事前分布としないので，encoderのロス関数が少しだけ複雑になる．

decoderはencoderで構成した$$\theta$$を入力としてと$$\phi$$ (論文では $$\beta$$) をパラメータとしてもち，周辺化尤度をロス関数とするようなニューラルネットワークである．

上記のモデルを少しだけ変更してprodLDAというのも合わせて提案しており，そっちのほうが性能はよいらしい．

### その他

- 論文の$$\beta$$はLDAでいうDirichlet分布のハイパーパラメータではなく，$$\phi$$のことだと思われるので注意
- 貢献の2つ目としては実行速度を謳っているが，比較手法はsklearnのonline LDAなどを使っており，提案手法はTF使っててGPU使いそうな雰囲気があるので疑問が残る

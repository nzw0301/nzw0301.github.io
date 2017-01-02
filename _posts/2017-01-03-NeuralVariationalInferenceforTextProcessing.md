---
layout: post
title: "Neural Variational Inference for Text Processing"
comments: false
abstract: NVIで文書の生成モデル
---

### メタデータとか


Yishu Miao, Lei Yu, Phil Blunsomの[論文](http://www.jmlr.org/proceedings/papers/v48/miao16.html)でICML2016に通っている．
[最近読んだ論文中](http://nzw0301.github.io/2017/01/NeuralVariationalInferenceForTopicModels)で比較手法として挙げられていたので読んだ．

教師なしとして文書の生成モデル，教師ありとしてQAをやっているが，後者については触れない．

### 本題

VAEの枠組みの中で文書の生成モデルを提案している．
論文では言及されていないが，LSIと対応付けるとわかりやすい．

encoderは，文書のBag-of-words表現（頻度ベクトル）を入力として，連続値のベクトルに変換する．
ここでは1文書 $$\mathbf{X}$$ で表す．
中間表現は，VAEと同様に事前分布を多変量標準正規分布とする多変量正規分布のパラメータからreparametarization trickで構成する．
サンプルで得られる中間表現を $$\mathbf{h} \in R^K$$ とすれば，
LSIにおける1文書の潜在表現に対応する．

decoderは，$$\mathbf{h}$$ の他に $$\mathbf{X}$$ に含まれる各単語のone-hot表現も入力として受け取る．
$$\mathbf{X}$$ の $$i$$ 番目の単語を $$\mathbf{x}_i$$ としたとき， $$\mathbf{h}^T \mathbf{R} \mathbf{x}_i + \mathbf{b}_i$$ を $$\mathbf{X}$$に含まれる全単語について計算する．
各単語で計算した結果をsoftmax関数に適用し， $$\mathbf{x}_i$$ を予測する．
$$\mathbf{R}$$ は，単語の潜在表現になっているため，LSIと同様に $$\mathbf{h}$$ と掛けあわせる（softmax関数も使うが）ことで元の文書 $$\mathbf{X}$$ の復元をしていると解釈できる．

### その他

- [実装](https://github.com/carpedm20/variational-text-tensorflow)が公開されている
- perplexityでLDAがボロ負けしていて切ない

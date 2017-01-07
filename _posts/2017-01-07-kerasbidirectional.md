---
layout: post
title: "BidirectionalRNNはKerasだと1行でかける"
comments: false
abstract: KerasのBidirectionalの使い方
---

2016年8月くらいのkerasのコミットで `Bidirectional` というRNNのラッパーのレイヤーが追加されています（[該当ページ](https://keras.io/layers/wrappers/#bidirectional)）．


RNNは長さ $$T$$ の系列データ（自然言語とか）を $$0$$ 番目から順に $$T-1$$ 番目までを再帰的に計算するレイヤーです（Kerasの[RNN](https://keras.io/layers/recurrent/) にある`SimpleRNN`, `GRU`, `LSTM` の3種類が該当）．
いくつかの深層学習のモデル（有名な例を挙げると[GNMT](https://arxiv.org/abs/1609.08144)）では，系列の先頭からRNNにいれるだけではなくて，逆順にも入れています．
このようなRNNは，BidirectionalRNN (双方向RNN）と呼ばれています．

Kerasでは，RNNのラッパーレイヤーとして`Bidirectional`というレイヤーが提供されており，他のレイヤーと同様に1行で記述可能です．
以下の最終行が`Bidirectional`レイヤーの使用例です．


``` python
from keras.layer import LSTM, Bidirectional
from keras.model import Sequential

model = Sequential()
model.add(Bidirectional(LSTM(10, return_sequences=True), input_shape=(5, 10)))
```

`Bidirectional`の引数に双方向に処理するRNNのレイヤーを渡します．
注意点として，Bidirectionalにしたあとの2つテンソルに対する操作は，
`Bidirectional`の引数`merge_mode`に以下のどれか1つから選択する必要があります．デフォルトは`concat`です．

- `'sum'`: 要素和
- `'mul'`: 要素積
- `'concat'`: 結合
- `'ave'`: 平均
- `None`: 結合せずに`list`を返す

ここにない操作，例えばcosine similarityやdot，
などは行数が増えてしまいますが，`None`を指定してから，[`merge`](https://github.com/fchollet/keras/blob/f573a86b42e49754386e536358e08e861d40d24c/keras/engine/topology.py#L1617) を使うことで可能になります．

より具体的な使用例は[imdbのデータに対してBidirectionalなLSTMを使った公式サンプルコード](https://github.com/fchollet/keras/blob/master/examples/imdb_bidirectional_lstm.py)があるので，そちらを見ていただければと思います．

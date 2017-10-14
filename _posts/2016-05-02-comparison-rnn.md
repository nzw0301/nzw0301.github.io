---
layout: post
title: KerasでRNNを使った2値分類とユニットの比較
date: 2016-05-02 00:00:00 +0900
comments: false
---

この記事はKeras v1の内容です．
Keras v2 での動作は確認していません．

## はじめに

KerasのRNNには3種類のユニットが用意されています．

- `SimpleRNN`
  - 全結合の中間層が再帰
- `GRU`
  - LSTMを簡略化したようなもの
  
 ![スクリーンショット 2016-05-01 23.28.20.png](https://qiita-image-store.s3.amazonaws.com/0/72604/a1e379fb-3f15-0537-8768-ce8dba1501b0.png)

- `LSTM`
  - いくつかバリエーションがあるが，kerasのは1997年のLSTM
  - MLPシリーズのLSTMとは違うので要注意

  ![スクリーンショット 2016-05-01 23.38.43.png](https://qiita-image-store.s3.amazonaws.com/0/72604/69af0462-de13-8a3e-6bce-a1da117a82bb.png)

これらのWrapperの`Bidirectional`というのもあります．

## 本題

使用するデータは，Kerasに用意されているIMDBの映画の25,000レビューです．
各レビューにpositive/negativeのタグが付与されているため2値分類を行います．

コードは[こちら](https://gist.github.com/nzw0301/e1aee5296e1c7874af9743442d0f8573)．

今回は，系列を最大で180まで使用し，以下の様なニューラルネットにおけるRNNのユニット3種類を比較します．

1. `Embeddings`，100次元
2. `RNN`，20次元
3. 線形結合層，1次元
4. 出力層の活性化関数，`sigmoid`

![スクリーンショット 2016-05-02 7.34.35.png](https://qiita-image-store.s3.amazonaws.com/0/72604/4ec47bcf-3289-1dbe-0ba7-1f6c792b069f.png)

また，`SimpleRNN`についてはRNNの中間層をもう1層増やしたものを用意し，全4種類で性能比較を行います．
![スクリーンショット 2016-05-02 7.38.38.png](https://qiita-image-store.s3.amazonaws.com/0/72604/c60db384-478b-8c8a-bd7d-763935b65f12.png)

学習のepoch数は10としました．

### コードの説明

#### データの読み込み
`(X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)`


データを読み込む段階でいくつかパラメータがあり，前処理的なことをやってくれます．
例えばこの場合は，頻度順にみて上位`max_features`単語だけ使用します．

#### データ整形

`X_train = sequence.pad_sequences(X_train, maxlen=maxlen)`

各レビューの長さはバラバラになっているので，`sequence.pad_sequences`関数では，長さを揃えた行列に変換します．最大の系列長を`maxlen`とし，足りない分は0で埋め，超えた分は削除します．

#### RNNについて

`model.add(SimpleRNN(20, return_sequences=False))`

kerasのRNNでは，次の層に全時系列のベクトルを渡すか，最後の系列データを受けた結果を渡すか設定可能です．
次の層もRNNであれば前者を，線形結合層や出力層であれば後者になるかと思います．


### 結果

#### accuracy

training dataでは`SimpleRNN`を2層積んだものが最高ですが，test dataでみると最も低いので，過学習しています．
test dataで最も良かったのはLSTMでepochが7回目の時でした．

![スクリーンショット 2016-05-02 7.40.27.png](https://qiita-image-store.s3.amazonaws.com/0/72604/2051c51c-3caa-c57d-9876-e66610054809.png)

#### loss
accuracyと同じ傾向で，

- training dataでは`SimpleRNN`2層がloss最小
- test dataでは，epochが7回目のLSTMが最小で`SimpleRNN`が最大

![スクリーンショット 2016-05-02 7.40.32.png](https://qiita-image-store.s3.amazonaws.com/0/72604/56f17752-8ab4-bee9-e9e5-ebe090c2dba8.png)

## 参考文献

- GRUの転載元
  - [_Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation_](http://arxiv.org/abs/1406.1078)

- LSTMの転載元
  - [_LONG SHORT–TERM MEMORY_](http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf)

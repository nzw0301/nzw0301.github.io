---
layout: post
title: 混合ユニグラムモデル+周辺化ギブスサンプリング
date: 2015-12-08 00:00:00 +0900
comments: false
---

青いトピックモデル本の混合ユニグラムモデルのベイズ推定（周辺化ギブスサンプ）のPython実装です．
本p53のアルゴリズムです．
概要は[こちら](http://nzw0301.github.io/2015/12/mixgibbs)


```python
import sys
import math
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing
import scipy.special

fname = sys.argv[1]
cv = CountVectorizer(token_pattern='(?u)\\b\\w')
docs = []

# データの読み込み
with open(fname) as f:
  for l in f:
    docs.append(l.strip())

Docs = cv.fit_transform(docs)
del docs

z = [-1]*Docs.shape[0] # topic idを管理，indexは文書のidと一致
K = 2 # トピック数
D_k = [0] * K # 要素：トピックkが割り当てらてた文書数
N_k = [0] * K # 要素：トピックkが割り当てらてた文書の総単語数
V = Docs.shape[1] # 語彙数
N_kv = [] # 各トピックにおける単語頻度
for k in range(K):
  N_kv.append([0] * V)
alpha = 1
beta = 1
# end init

for i in range(100):
  print("------------\n")
  print("ite:", i, " α= ", alpha, " β= ", beta)
  print("トピックの割り当て", z)

  for doc_id, doc in enumerate(Docs):
    z_d = z[doc_id] # 文書にあてられたトピックid
    not_zero_indices = doc.indices # 非ゼロ要素の単語index
    N_d = sum(doc.toarray()[0]) # 文書dの総単語数

    # 現在の文書の分を抜く
    if z_d >= 0:
      D_k[z_d] -= 1
      for index in not_zero_indices:
        N_kv[z_d][index] -= doc[0, index]
      N_k[z_d] -= N_d

    pro = [] # サンプリング式の値を格納
    for k in range(K):
      first = (D_k[k] + alpha) * math.gamma(N_k[k]+(beta*V)) / math.gamma(N_k[k] + N_d + (beta*V))
      second = 1.0
      for index in not_zero_indices:
        second *= math.gamma(N_kv[k][index] + doc[0, index] + beta) / math.gamma(N_kv[k][index] + beta)
      pro.append(first*second)

    pro = preprocessing.normalize(pro, norm="l1")[0] # 正規化
    z_d = np.nonzero(np.random.multinomial(1, pro))[0][0] # トピックの割り当て
    z[doc_id] = z_d # 文書のトピックを更新
    print("\ndoc id = ", doc_id)
    for k in range(K):
      print("topic",k,"'s pro =", pro[k])

    D_k[z_d] += 1
    N_k[z_d] += N_d
    for index in not_zero_indices:
      N_kv[z_d][index] += doc[0, index]

  # update α
  numerator = 0.0 
  for k in range(K):
    numerator += scipy.special.psi(D_k[k] + alpha)
  numerator -= K * scipy.special.psi(alpha)
  alpha = alpha * numerator / (K * scipy.special.psi(Docs.shape[0] + alpha * K) - K * scipy.special.psi(alpha * K))
  # end update α

  # update β
  numerator = 0.0
  denominator = 0.0
  for k in range(K):
    for v in range(V):
      numerator += scipy.special.psi(N_kv[k][v] + beta)
    denominator += scipy.special.psi(N_k[k]+beta*V)
  numerator -= K*V*scipy.special.psi(beta)
  denominator = V * denominator - K*V*scipy.special.psi(beta*V)
  beta = beta*numerator/denominator
  # end update β
```

例えばこんなデータがあるとします．

```data.txt
城ヶ崎美嘉 城ヶ崎美嘉 デレマス デレマス 城ヶ崎莉嘉 城ヶ崎莉嘉 カブトムシ
城ヶ崎美嘉 城ヶ崎美嘉 佳村はるか デレマス デレマス 城ヶ崎莉嘉 城ヶ崎莉嘉 カブトムシ 城ヶ崎美嘉
城ヶ崎美嘉 佳村はるか デレマス デレマス 城ヶ崎莉嘉 城ヶ崎莉嘉 カブトムシ カブトムシ
安原絵麻 安原絵麻 佳村はるか SHIROBAKO SHIROBAKO ドーナツ 万策尽きた 安原絵麻
安原絵麻 安原絵麻 佳村はるか SHIROBAKO SHIROBAKO 武蔵野 万策尽きた 安原絵麻 武蔵野
安原絵麻 安原絵麻 佳村はるか 佳村はるか 佳村はるか 城ヶ崎美嘉 城ヶ崎美嘉 城ヶ崎美嘉 SHIROBAKO デレマス 
```

1行が1文書に相当します．
1-3行目と4-5行目はそれぞれ同じ作品のキーワードからなるものだと思ってください．
6行目はそれぞれから一部をもってきたデータになります．
混合ユニグラムモデルにおいてトピック数を2にしたとき，おそらく

- 1-3行目は1つのトピックに偏った分布
- 4-5行目は別の1つのトピックに偏った分布
- 6行目は↑の2つが混じった分布

になるはずです．


上記のコードを実行した結果(イテレーション100回)

```
doc id =  0
topic 0 's pro = 1.71676927372e-05
topic 1 's pro = 0.999982832307

doc id =  1
topic 0 's pro = 4.56379334863e-06
topic 1 's pro = 0.999995436207

doc id =  2
topic 0 's pro = 2.0764393002e-05
topic 1 's pro = 0.999979235607

doc id =  3
topic 0 's pro = 0.999658093279
topic 1 's pro = 0.000341906721229

doc id =  4
topic 0 's pro = 0.999900794632
topic 1 's pro = 9.92053680337e-05

doc id =  5
topic 0 's pro = 0.258726973919
topic 1 's pro = 0.741273026081

ite: 99  α=  14.5969394228  β=  0.651078742861
トピックの割り当て [1, 1, 1, 0, 0, 1]
```

`doc id`はデータの行数-1に相当します．
`doc id=5`のときにトピックが混じっていることがわかります．
一方それ以外のデータについては片方のトピックに偏っています（一方だけ約99%になっている）

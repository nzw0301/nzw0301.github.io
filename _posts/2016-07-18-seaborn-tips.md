---
layout: post
title: Seaborn tips
date: 2016-07-18 00:00:00 +0900
comments: false
---

# はじめに

Pythonの可視化ライブラリといえばmatplotlibがあるが，そのラッパーライブラリに[seaborn](https://stanford.edu/~mwaskom/software/seaborn/)がある．

pandasのデータフレーム読み込んで，それの可視化などが楽にできる．


# フォントが回転・拡大時にグラフから見きれる

matplotlibの問題らしいです．

`barplot`でフォントを回転・拡大したい場合がある．
このとき，jupyterでは，グラフがちゃんと表示されていても，保存したグラフではラベルが見切れることがある．

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

d = {'epoch' : range(1,11),
     'train' : np.random.random(10),
     'test'  : np.random.random(10),
     'model' : ["MLP"] *10,}
df = pd.DataFrame(d)

d = {'epoch' : range(1,11),
     'train' : np.random.random(10),
     'test'  : np.random.random(10),
     'model' : ["LSTM"] *10,}
df = df.append(pd.DataFrame(d))

sns.set(context='notebook', font_scale=2.5)
fig = sns.barplot(x="epoch", y="train", hue="model", data=df)
plt.title("awesome titme")

fig.figure.savefig("file.png")
```

このコードから生成される画像は見切れる．（グラフ自体はデタラメ）

![file.png](https://qiita-image-store.s3.amazonaws.com/0/72604/7d8a622b-786a-c133-f36f-32fb8cd9e66a.png)

x軸の下にある"epoch"が見切れている．

# 解決策


`fig.figure.savefig("file.png")`を`fig.figure.savefig("file.png",  bbox_inches="tight")` とすると見切れなくなる．

![file.png](https://qiita-image-store.s3.amazonaws.com/0/72604/67f018c2-dae6-3bc5-9e29-74893613ff14.png)

# 読み込み時にエラーになる

```
RuntimeError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework. See the Python documentation for more information on installing Python as a framework on Mac OS X. Please either reinstall Python as a framework, or try one of the other backends. If you are Working with Matplotlib in a virtual enviroment see 'Working with Matplotlib in Virtual environments' in the Matplotlib FAQ
```

が出た場合は設定ファイルでバックエンドを指定すれば良いらしい．
自分の環境ではなかったので，作成してから設定を書きこんだ．

```sh
echo "backend : TkAgg" >> .matplotlib/matplotlibrc
```

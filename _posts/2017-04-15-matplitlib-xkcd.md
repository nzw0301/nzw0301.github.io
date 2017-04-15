---
layout: post
title: matplotlib
date: 2017-04-15 00:00:00 +0900
comments: false
---

[matplotlib]([http://matplotlib.org/) に [xkcd](https://xkcd.com/) 風にグラフを書く関数があります．
例えば[こんな図](http://matplotlib.org/examples/showcase/xkcd.html)です．

触ってみたくなったので，触ってみました．
あんまり情報量はないです．

## 通常時

任意のグラフで適用できる気がします．
まずは，`matplotlib.pyplot.plot` を使います．
matplotlib 2.0.0なので，これでもきれいです．

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(100, 200, 10)
plt.plot(x, x, label=r'$\phi$')
plt.plot(x, x+np.random.RandomState(1).randint(20, 100, 10), label=r'$\eta$')
plt.ylabel('#sizes')
plt.xlabel('Time')
plt.legend()
plt.title('awesome figure')
```

![fig]({{ site.url }}/images/normal_matplotlib.svg)

## xkcd

`plt.xkcd()`を実行すると，それ移行すべての図がxkcd風になります．
一部で使いたい場合は `with` で囲みます．

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(100, 200, 10)

with plt.xkcd():
    plt.plot(x, x, label=r'$\phi$')
    plt.plot(x, x+np.random.RandomState(1).randint(20, 100, 10), label=r'$\eta$')
    plt.ylabel('#sizes')
    plt.xlabel('Time')
    plt.legend()
    plt.title('awesome figure')

```

![fig]({{ site.url }}/images/xkcd_matplotlib.svg)

## NOTE

- `import seaborn` すると背景が変化します
- `seaborn` の図も `plt.xkcd()` でそれ風になります

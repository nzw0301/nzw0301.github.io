---
layout: post
title: "Sigmoid関数の速度比較"
comments: true
---

### 背景

sigmoid関数は，2値分類やVAEの，出力層の活性化関数として使われる．

$$\mathrm{sigmoid}(x) = \frac{1}{1 + \exp(-x)}$$

定義に従って実装してもいいのだが，そうするとけっこう遅いらしいので，高速化するテクニックがある．例えば[word2vecだと前に記事をかいたこんなの](http://nzw0301.github.io/2017/07/sigmoidtable)．
どのくらい変わるか比較してみた．

---

### 本題

python 3.6.4 (anaconda3-latest) で計測．

まず，愚直に計算する場合の関数定義．

```python
def sigmoid(x):
    return 1. / (1. + np.exp(-x))
```

次にword2vecやfastTextの実装にある方法．
`-8`から`8`までを`512`分割してキャッシュしておく．

``` python
SIGMOID_TABLE_SIZE = 512
MAX_SIGMOID = 8

t_sigmoid = np.zeros(SIGMOID_TABLE_SIZE)

for i in range(SIGMOID_TABLE_SIZE):
    x = (i / SIGMOID_TABLE_SIZE * 2 - 1) * MAX_SIGMOID
    t_sigmoid[i] = 1. / (1. + np.exp(-x))

def sigmoid_cache(x):
    if x >= MAX_SIGMOID:
        return 1.
    elif x <= -MAX_SIGMOID:
        return 0.
    else:
        return t_sigmoid[(int)((x + MAX_SIGMOID) * (SIGMOID_TABLE_SIZE / MAX_SIGMOID / 2))]
```

`-10`から`10`までを生成する一様乱数で`10000`個のデータを生成する．
`%timeit` で計測したいので，関数化．

``` python
rnd = np.random.RandomState(7)
data = rnd.uniform(low=-10, high=10, size=10000)


def cal_sigmoid(data):
    for x in data:
        sigmoid(x)


def cal_sigmoid_cache(data):
    for x in data:
        sigmoid_cache(x)
```

まず，愚直に計算する方を計測．

``` jupyter-notebook
%timeit cal_sigmoid(data)

24.4 ms ± 905 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

次に，cacheしておく方を計測．

``` jupyter-notebook
%timeit cal_sigmoid_cache(data)

16.4 ms ± 441 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

後者がやっぱり速い．

cacheの生成は，実際にsigmoid呼ぶ回数の総数と比べれば，とても小さいため，今回は無視している．
~~問題としては，`numpy.array` に対しては使えないかもしれないこと．~~

`np.vectorize` 関数に渡すと `numpy.array` に対しても使えるようになる ([助言いただいたツイート](https://twitter.com/MtJuney/status/954681191868743681))．


```python
vectorzed_sigmoid_cache =  np.vectorize(sigmoid_cache)
```

``` jupyter-notebook
%timeit sigmoid(data)

161 µs ± 6.56 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

``` jupyter-notebook
%timeit vectorzed_sigmoid_cache(data)

8.13 ms ± 173 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

負けた．
ちなみに，キャッシュしないほうを`math.exp`にしても負けた．

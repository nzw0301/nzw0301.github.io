---
layout: post
title: jupyter notebookをCUIで実行
date: 2016-05-08 00:00:00 +0900
comments: false
---

# 背景

ノートPCで重い計算を含んだ　jupyter notebook　を実行することはしんどいので，サーバーで実行したくなる．ただ実行するだけなら `nbconvert` で　python　に変換すればいいのですが，実行した結果の出力が書き込まれた notebook もほしい．

# 本題

`nbconvert` を使う．

以下，実行ファイルが `hoge.ipynb` とする．

## Case 1. notebook を実行し，別名で保存

`jupyter nbconvert --to notebook --execute hoge.ipynb`
実行結果が，`hoge.nbconvert.ipynb`というnotebookに保存される．

しかしデフォルトでは，`nbconvert` に実行時間に制約があり，セルを実行してから30秒間出力がないと終了する．その場合は以下の様に引数を追加する．

`jupyter nbconvert --to notebook --ExecutePreprocessor.timeout=-1  --execute hoge.ipynb`

## Case 2. 新しいファイルを作らずに上書き

`--inplace`を使う．

なので `jupyter nbconvert --to notebook --inplace --execute hoge.ipynb`
とすると新しい notebook は作られずに上書きが行われる．

## 3. CLIで実行するとエラーに

`conda` を使って複数の環境がある状態で，notebook を作成すると Kernel 名がその名前になった．
今回は，ローカル環境では pyenv でいれた anaconda (このとき，`conda create`で別環境も作ってあるがそっちではなく) で jupyter notebook を作り，サーバ上で上記の1.のようにCLI 上で実行すると

`jupyter_client.kernelspec.NoSuchKernel: No such kernel named Python [Root]`

となり実行できない．解決策としてはこの [issue](https://github.com/ContinuumIO/anaconda-issues/issues/877#issuecomment-230520226) にある通り

`--ExecutePreprocessor.kernel_name=python`

をつけるだけ．

# まとめ
2のやり方を使って、まとめてかくと次のようになる．

`jupyter nbconvert --to notebook --ExecutePreprocessor.timeout=-1 --execute --inplace --ExecutePreprocessor.kernel_name=python hoge.ipynb`

# 参考

- [http://nbconvert.readthedocs.io/en/latest/config_options.html](http://nbconvert.readthedocs.io/en/latest/config_options.html)

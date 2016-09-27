---
layout: post
title: jupyter notebookをCUIで実行
date: 2016-05-08 00:00:00 +0900
comments: false
---

# はじめに

ノートPCで重い計算を含んだjupyter notebookを実行することはしんどいので，サーバーで実行したくなる．
ただ実行するだけなら`nbconvert`でpythonに変換すればいいのですが，実行した結果の出力が書き込まれたnotebookもほしい．

# 本題

`nbconvert`を使う．

以下，実行ファイルが`hoge.ipynb`とする．

## 1. notebookを実行し，別名で保存

`jupyter nbconvert --to notebook --execute hoge.ipynb`
実行結果が，`hoge.nbconvert.ipynb`というnotebookに保存される．

しかしデフォルトでは，nbconvertに実行時間に制約があり，セルを実行してから30秒間出力がないと終了する．
その場合は以下の様に引数を追加してやる．


`jupyter nbconvert --to notebook --ExecutePreprocessor.timeout=-1  --execute hoge.ipynb`


## 2. 新しいファイルを作らずに上書き

`--inplace`を使う．

なので
`jupyter nbconvert --to notebook  --inplace --execute hoge.ipynb`
とすると新しいnotebookは作られずに上書きが行われる．

## 3. CLIで実行するとエラーに

condaを使って複数の環境がある状態で，notebookを作成するとKernel名がその名前になった．
今回は，ローカル環境ではpyenvでいれたanaconda (このとき，`conda create`で別環境も作ってあるがそっちではなく) でjupyter notebookを作り，サーバ上で上記の1.のようにCLI上で実行すると

`jupyter_client.kernelspec.NoSuchKernel: No such kernel named Python [Root]`

となり実行できない．


解決策としては[issue](https://github.com/ContinuumIO/anaconda-issues/issues/877#issuecomment-230520226)にある通り

`--ExecutePreprocessor.kernel_name=python`

をつけるだけ．

# まとめ

以上をまとめてかくと次のようになる．

`jupyter nbconvert --to notebook --ExecutePreprocessor.timeout=-1 --execute --inplace --ExecutePreprocessor.kernel_name=python hoge.ipynb`

# 参考

- [http://nbconvert.readthedocs.io/en/latest/config_options.html](http://nbconvert.readthedocs.io/en/latest/config_options.html)

---
layout: post
title: "Python勉強メモ"
date: 2015-07-16 02:25:00 +0900
comments: false
---

# はじめに

講義の関係で少しだけNLTKとかgensimとかflaskを触りましたが，
全然Pythonわからないので，いい加減勉強します．

図書館にあったこれをひと通り読むつもりです．


<a href="http://www.amazon.co.jp/gp/product/4873116880/ref=as_li_ss_il?ie=UTF8&camp=247&creative=7399&creativeASIN=4873116880&linkCode=as2&tag=algebrae-22"><img border="0" src="http://ws-fe.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=4873116880&Format=_SL110_&ID=AsinImage&MarketPlace=JP&ServiceVersion=20070822&WS=1&tag=algebrae-22" ></a><img src="http://ir-jp.amazon-adsystem.com/e/ir?t=algebrae-22&l=as2&o=9&a=4873116880" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

# 環境

- pyenv
- anaconda3-2.1.0
- Jupyter

Javaをよく書くのでJythonも検討しましたが，Javaとの連携がめんどうそうで手間でやめました．

速い速いと聞くpypyもやろうとしましたが，パッケージ周りがめんどうだったのでやめました．

scikit-learnなどをやりたい方はanacondaを入れると必要なパッケージがだいたい入ってて簡単です．

# 本題

まずを環境つくります．
グローバルでパッケージを管理したくないので，virtualenvを使います．

~~~
pip install virtualenv
virtualenv no-site-packages anaconda3
cd anaconda3
. bin/activate #この環境を使う
deactivate #この環境から抜ける
~~~

REPLでも十分ですが，jupyterでよりインタラクティブにpython使ってみます．
ちなみにJuliaもつかえます．

jupyterからhtmlのslideも作れちゃうので，tutorialには便利そうです．

~~~
pip install ipython
ipython notebook #ブラウザが起動
~~~


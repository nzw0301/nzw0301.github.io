---
layout: post
title: "青深層学習 4.4.2 行列表記"
date: 2015-11-09 01:22:00 +0900
comments: false
---

# はじめに
前回の続きです．

順伝播，誤差逆伝播，重みとバイアスの更新を行列の表記で行います．

# 表記

- \\(N\\) ：ミニバッチのデータ数
- \\(\boldsymbol{x}_n\\)：1件のデータ(例えば1つ文書，行は単語の頻度とか)
- \\(\boldsymbol{X} = \left[ \begin{array}{c} \boldsymbol{x}_1 ... \boldsymbol{x}_N \end{array} \right]\\)：ミニバッチの行列
- \\(\boldsymbol{W} = w_{ji}^{(l)} \\)：\\(l\\)層のおける重みの行列 要素はユニット\\(i\\)からユニット\\(j\\)のリンクの重み
- \\(\boldsymbol{b}^{(l)}\\)：\\(l\\)層のバイアスのベクトル
- \\(\boldsymbol{u}^{(l)}_n\\)：データ\\(\boldsymbol{x}_n\\)のときの，\\(l\\)層の入力ベクトル 1行目はユニットの1つ目の入力に対応
- \\(\boldsymbol{U}^{(l)} = \left[ \begin{array}{c} \boldsymbol{u}_1^{(l)} ... \boldsymbol{u}_N^{(l)} \end{array} \right]\\)：\\(l\\)層の入力の行列，列がデータ1件，行がユニットに対応
- \\(\boldsymbol{Z}^{(l)} = \left[ \begin{array}{c} \boldsymbol{z}_1^{(l)} ... \boldsymbol{z}_N^{(l)} \end{array} \right]\\)：\\(l\\)層の出力の行列，列がデータ1件，行がユニットに対応，\\(\boldsymbol{U}^{(l)}\\)の各要素に活性化を適用しただけ
- \\(\boldsymbol{Y} = \left[ \begin{array}{c} \boldsymbol{y}_1 ... \boldsymbol{y}_N \end{array} \right]\\)：各データに対する最終的な出力を列にもつ行列
- \\(\boldsymbol{\Delta^{(l)}}\\)：列がミニバッチのデータ，行がユニットのデルタ\\(\delta^{(l)}_j\\)の行列

# 順伝播

入力は恒等写像なので， \\(\boldsymbol{Z}^{(1)}=\boldsymbol{X}\\) ．


\begin{eqnarray}
\boldsymbol{U}^{(l)} &=&\boldsymbol{W^{(l)}} \boldsymbol{Z^{(l-1)}} + \boldsymbol{b}^{(l)} \boldsymbol{1}_N^{T} \tag{1} \\\
\boldsymbol{Z}^{(l)} &=& f^{(l)}(\boldsymbol{U}^{(l)}) \tag{2}
\end{eqnarray}

- \\(j\\)：\\((l)\\)層のユニット数（バイアス除く）
- \\(i\\)：\\((l-1)\\)層のユニット数（バイアス除く）
- \\(\boldsymbol{W}^{(l)}\\)：\\(j \times i\\)
- \\(\boldsymbol{U}^{(l)}\\)：\\(j \times N\\)
- \\(\boldsymbol{Z}^{(l)}\\)：\\(j \times N\\)
- \\(\boldsymbol{b}^{(l)}\\)：\\(j \times 1\\)
- \\(\boldsymbol{1}_N\\)：\\(1 \times N\\)




\\(y=\left[ \begin{array}{c} x x x \end{array} \right]\\)
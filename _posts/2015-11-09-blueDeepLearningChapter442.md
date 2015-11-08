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
- \\(\boldsymbol{W^{(l)}} = w_{ji}^{(l)} \\)：\\(l\\)層のおける重みの行列 要素はユニット\\(i\\)からユニット\\(j\\)のリンクの重み
- \\(\boldsymbol{b}^{(l)}\\)：\\(l\\)層のバイアスのベクトル
- \\(\boldsymbol{u}^{(l)}_n\\)：データ\\(\boldsymbol{x}_n\\)のときの，\\(l\\)層の入力ベクトル 1行目はユニットの1つ目の入力に対応
- \\(\boldsymbol{U}^{(l)} = \left[ \begin{array}{c} \boldsymbol{u}_1^{(l)} ... \boldsymbol{u}_N^{(l)} \end{array} \right]\\)：\\(l\\)層の入力の行列，列がデータ1件，行がユニットに対応
- \\(\boldsymbol{Z}^{(l)} = \left[ \begin{array}{c} \boldsymbol{z}_1^{(l)} ... \boldsymbol{z}_N^{(l)} \end{array} \right]\\)：\\(l\\)層の出力の行列，列がデータ1件，行がユニットに対応，\\(\boldsymbol{U}^{(l)}\\)の各要素に活性化を適用しただけ
- \\(\boldsymbol{Y} = \left[ \begin{array}{c} \boldsymbol{y}_1 ... \boldsymbol{y}_N \end{array} \right]\\)：各データに対する最終的な出力を列にもつ行列
- \\(\boldsymbol{\Delta^{(l)}}\\)：列がミニバッチのデータ，行がユニットのデルタ\\(\delta^{(l)}_j\\)の行列
- k：出力層のユニット数

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

# 逆伝播

出力層のデルタ\\(\boldsymbol{\Delta^{(L)}} = \boldsymbol{D} - \boldsymbol{Y}\\)
を\\((L-1)\\)~\\(2\\)まで逆伝播させる．

\begin{eqnarray}
\boldsymbol{\Delta}^{(l)} = f'^{(l)}(\boldsymbol{U}^{(l)}) \odot (\boldsymbol{W}^{(l+1)T} \boldsymbol{\Delta}^{(l+1)}) \tag{3}
\end{eqnarray}


- \\(\boldsymbol{\Delta^{(L)}} , \boldsymbol{D} , \boldsymbol{Y}\\)：\\(k \times N\\)
- \\(\boldsymbol{\Delta^{(l)}} \\)：\\(j \times N\\)
- \\(\odot\\)：[アダマール積](https://ja.wikipedia.org/wiki/%E3%82%A2%E3%83%80%E3%83%9E%E3%83%BC%E3%83%AB%E7%A9%8D "アダマール積")

# 重み更新
逆伝播で計算したデルタを使って微分し，重み\\(\boldsymbol{W}\\)を更新．
誤差逆伝播が漸化式で求めたので，重みの更新は並列して計算ができる．

- \\(\partial \boldsymbol{W}^{(l)} \\)：\\((l)\\)層の重み\\(w_{ji}^{(l)}\\)で誤差関数\\(E=\sum_{n=1}^N E_n(\boldsymbol{W})\\)を微分した値を\\((j,i)\\)成分にもつ行列
- \\(\partial \boldsymbol{b}^{(l)} \\)：\\((l)\\)層の重み\\(b_{j}^{(l)}\\)で誤差関数\\(E=\sum_{n=1}^N E_n(\boldsymbol{W})\\)を微分した値を\\((j)\\)成分にもつ列ベクトル
- \\(\epsilon\\)：学習率

\begin{eqnarray}
\partial \boldsymbol{W}^{(l)} = \frac{1}{N} \boldsymbol{\Delta^{(l)}} \boldsymbol{Z^{(l-1)T}} \tag{4}\\\
\partial \boldsymbol{b}^{(l)} = \frac{1}{N} \boldsymbol{\Delta^{(l)}} \boldsymbol{1}_N \tag{5}
\end{eqnarray}

- \\(\partial \boldsymbol{W}^{(l)}\\)：\\(j \times i\\)
- \\(\partial \boldsymbol{b}^{(l)}\\)：\\(j \times 1\\)
- \\(\boldsymbol{Z^{(l-1)}} \\)：\\(i \times N\\)
- \\(\boldsymbol{\Delta^{(l)}} \\)：\\(j \times N\\)
- \\(j\\)：\\((l)\\)層のユニット数（バイアス除く）
- \\(i\\)：\\((l-1)\\)層のユニット数（バイアス除く）
- \\(N\\)：ミニバッチのデータ数


更新式は，

\begin{eqnarray}
\boldsymbol{W}^{(l)} \leftarrow
\boldsymbol{W}^{(l)}
- \epsilon \partial \boldsymbol{W}^{(l)} \tag{6} \\\ 
\boldsymbol{b}^{(l)} \leftarrow
\boldsymbol{b}^{(l)}
- \epsilon \partial \boldsymbol{b}^{(l)} \tag{7} \\\ 
\end{eqnarray}


以上です．
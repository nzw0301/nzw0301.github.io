---
layout: post
title: "青深層学習 4.4.1 出力層でのデルタ"
date: 2015-11-09 01:22:00 +0900
comments: false
---

#### はじめに
前回の続きです．

高校生で培った微分を駆使してがんばります．

#### 出力層のデルタ
出力層のデルタを求めます．
出力層のデルタは，誤差関数\\(E_n\\)を，出力層の入力 \\(u_{j}^{(L)}\\) で微分(式1)である．

なので，出力層の活性化関数と誤差関数によって計算が異なる（本書の例の場合結果は全て同じになる）

\begin{eqnarray}
\delta_j^{(L)} =
  \frac{\partial E_n }{\partial u_{j}^{(L)}} \tag1
\end{eqnarray}

#### 回帰

- 活性化関数：恒等写像
- 誤差関数：2乗誤差

2乗誤差は以下の式2であり，出力層が恒等写像なので，\\(\boldsymbol{y}=\boldsymbol{z}=\boldsymbol{u}\\)
より式4に変形できる．

\begin{eqnarray}
E_n &=& \frac{1}{2} ||\boldsymbol{y} - \boldsymbol{d} ||^2 \tag{2}\\\
&=& \frac{1}{2}\sum_j (y_j-d_j)^2 \tag{3} \\\
&=& \frac{1}{2}\sum_j (u_j^{(L)} - d_j)^2 \tag{4} \\\
\end{eqnarray}

式4を\\(u_j^{(L)}\\)で微分すればいいので\\(L\\)層のデルタは，
\begin{eqnarray}
\delta_j^{(L)} &=& u_j^{(L)} - d_j \tag{5} \\\
&=& y_j - d_j \tag{6}
\end{eqnarray}

#### 2値分類

- 活性化関数：ロジスティック関数
- 誤差関数：対数尤度

2値分類なので出力層のユニットは1つだけ．

対数尤度の総和の内側のデルタ（データ1つに対するデルタ）を求める．

式7で分子を対数尤度で展開し，式8はchain ruleを適用してyで展開する．

\begin{eqnarray}
\delta^{(L)} &=& \frac
{\partial(d \log(y) + (1-d)\log(1-y))}
{\partial u} \tag{7} \\\
&=& \frac
{\partial (d \log(y) + (1-d)\log(1-y))}
{\partial y}
\frac{\partial y}
{\partial u} \tag{8} \\\
\end{eqnarray}

式8の第1項目は，対数の微分，2項目は，出力層がロジスティック関数なので， \\(y=\frac{1}{1+\exp(-u)}\\) を\\(u\\)で微分する必要がある（高校でいうところの商の微分）．

\begin{eqnarray}
\delta^{(L)} &=& (\frac{d}{y} - \frac{1-d}{1-y}) y(1-y) \tag{9}  \\\
&=& d(1-y)-(1-d)y \tag{10} \\\
&=& d-y \tag{11} \\\
\end{eqnarray}

ロジスティック関数をちゃんと微分すると以下のようになる．

\begin{eqnarray}
\frac{\partial y} {\partial u} &=& \frac{\partial}{\partial u} \frac{1}{1+\exp(-u)} \\\
&=& \frac{(-1)(\exp(-u))(-1)}{(1+\exp(-u))^2}\\\
&=& \frac{\exp(-u)}{(1+\exp(-u))^2}\\\
&=&(\frac{1}{1+\exp(-u)})(1-\frac{1}{1+\exp(-u)})\\\
&=&y(1-y)
\end{eqnarray}

- 合成関数の微分
- 商の微分

って名前がついてたきがする．


#### 多値分類
（これが一番時間がかかった）

- 活性化関数：ソフトマックス関数
- 誤差関数：交差エントロピー

誤差関数をソフトマックス関数で展開すると式13になる．

\begin{eqnarray}
E_n &=& - \sum_k d_k \log(y_k) \tag{12} \\\
&=& - \sum_k d_k \log (\frac{\exp(u_k^{(L)})}{\sum_i \exp(u_i^{(L)})}) \tag{13}
\end{eqnarray}

\\(\delta^{(L)}\\)を求めるには，chain ruleを使って\\(y\\)で展開する．

---


$$ \begin{align}
\delta^{(L)} &=& \sum_k \frac{\partial E_n}{\partial y_k} \frac{\partial y_k}{u_j^{(L)}} \tag{14} \\
&=& \sum_k (-1) \frac{d_k}{y_k} \frac{\partial }{u_j^{(L)}} \frac{\exp(u_k^{(L)})}{\sum_i \exp(u_i^{(L)})} \tag{15} \\
&=& - \frac{d_j}{y_j} \frac{\exp(u_j^{(L)}) \{ \sum_i \exp(u_i^{(L)})\} - \{\exp(u_j^{(L)})\}^2 }{\{ \sum_i \exp(u_i^{(L)})\}^2} - \sum_{k \neq j} \frac{d_k}{y_k} \frac{-\{\exp(u_k^{(L)})\}\{\exp(u_j^{(L)})\}}{\{\sum_i \exp(u_i^{(L)})\}^2} \tag{16} \\
&=& - d_j \frac{\sum_i \exp(u_i^{(L)}) - \exp(u_j^{(L)})  }{\sum_i \exp(u_i^{(L)})} + \sum_{k \neq j} \frac{d_k}{y_k} y_k y_j \tag{17} \\
&=& - d_j + d_j y_j + \sum_{k \neq j} d_k y_j  \tag{18} \\
&=& - d_j + \sum_{k} d_k y_j \tag{19} \\
&=& - d_j + y_j \tag{20} \\
\end{align} $$


- 式15：第1項目はそのまま誤差関数を \\(y_k\\)で微分し，2項目はソフトマックスに展開する．
- 式16：\\(k=j\\)と\\(k \neq j\\)の2つで変わるので，2つに分解して商の微分をする．
- 式17,式18：ソフトマックス関数で約分して整理．
- 式19：第3項に第2項を合わせる．
- 式20：\\(\sum_k d_k = 1\\)


#### まとめ

全部出力と正解の差になる．

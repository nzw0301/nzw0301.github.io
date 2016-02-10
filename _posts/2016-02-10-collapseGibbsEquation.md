---
layout: post
title: "トピックモデルによる統計的潜在意味解析のp56の最初の式"
date: 2016-02-10 18:36:00 +0900
comments: false
---

#### はじめに


[トピックモデルによる統計的潜在意味解析](http://amzn.to/1Tc0ost) を頭から読んでいて3.2.4の周辺化ギブスサンプリングの式が気になったのでその部分の式展開だけをちょっと詳しめに書きます．



#### 本題
p55の最後の式からp56の最初の式変形をやります．
2016年2月10日にアクセスした正誤表には記述がないのですが，
p56の最後の項は同時確率ではなく，条件付き確率であると思われます．


\begin{eqnarray}
p(z\_{d,i} = k, w\_{d,i}=v, \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} | {\boldsymbol \alpha}, {\boldsymbol \beta})
\end{eqnarray}

がp55の最後の式です．
これを順番に分解していきます．

\begin{eqnarray}
p(z\_{d,i} = k, w\_{d,i}=v, \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} | {\boldsymbol \alpha}, {\boldsymbol \beta}) &=&
p( w\_{d,i} = v |z\_{d,i} = k, \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i},  {\boldsymbol \alpha}, {\boldsymbol \beta})  \\\
& & \times
p(z\_{d,i} = k, \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} | {\boldsymbol \alpha}, {\boldsymbol \beta}) \tag{1} \\\
&=&
p( w\_{d,i} = v |z\_{d,i} = k, \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i},  {\boldsymbol \alpha}, {\boldsymbol \beta}) \\\
& & \times
p(z\_{d,i} = k| \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} , {\boldsymbol \alpha}, {\boldsymbol \beta}) \\\
& &  \times
p(\mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} | {\boldsymbol \alpha}, {\boldsymbol \beta}) \tag{2}
\end{eqnarray}

式1の左辺から右辺の変形は以下の関係式を使います．

\begin{eqnarray}
p(w\_{d,i}=v | z\_{d,i} = k, \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} ,  {\boldsymbol \alpha}, {\boldsymbol \beta}) = \frac{
  p(z\_{d,i} = k, w\_{d,i}=v, \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} | {\boldsymbol \alpha}, {\boldsymbol \beta})}
{p(z\_{d,i} = k, \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} | {\boldsymbol \alpha}, {\boldsymbol \beta})}
\end{eqnarray}

式2では式1右辺の第2項目を以下の等式を用いて2つの項（式2の第2項，第3項）に分解しています．


\begin{eqnarray}
p(z\_{d,i} = k | \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} , {\boldsymbol \alpha}, {\boldsymbol \beta}) = \frac{
p(z\_{d,i} = k, \mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} | {\boldsymbol \alpha}, {\boldsymbol \beta})}
{p(\mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} | {\boldsymbol \alpha}, {\boldsymbol \beta})}
\end{eqnarray}


以上から本のように同時確率\\(p(\mathbf{w}^{\backslash d,i}, \mathbf{z}^{\backslash d,i} , {\boldsymbol \alpha}, {\boldsymbol \beta})\\)ではなく条件付き確率になるような気がしています．
ただ，条件付き確率であろうとなかろうとこの項は\\(z\_{d,i}\\)を含んでいないので消去されることから期待値計算には関係してきません．

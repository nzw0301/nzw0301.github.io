---
layout: post
title: "青深層学習，誤差逆伝播法の計算"
date: 2015-11-03 06:30:00 +0900
comments: false
---

# はじめに
青いほうの深層学習を読んでいたら誤差逆伝播法の式変形が意味不明だったので，自分なりのやり方で書いてみます．

（個人的には中間層の重みを計算するやり方のほうがしっくりきて出力層の重みで転置がでてくるのがちょっと天下りっぽくて理解しにくかった，ベクトル解析をやってないせいだろうか）

# 本題
2つあるので片方ずつやっていきます．


このような3層のネットワークを考えます．(p42)

![nn]({{ site.url }}/images/nn.svg)

そもそもなんで微分を求めるかというと誤差関数を最小とするような重みを2章の勾配法によって求めるために，必要なためです．

# 出力層の重み
数学がよくわからないので微分したらなんで転置になるのかわからなくてこれが手間取った．

愚直に総和を展開した．

微分するほうもされるほうもスカラなので結果もスカラになる


\begin{eqnarray}
\frac{\partial E_n }{\partial w_{ji}^{(3)}} &=&
\sum_{k=1}^3 \frac{\partial E_n }{\partial y_{k}} \frac{\partial y_k }{\partial w_{ji}^{(3)}} \\\
&=&　\sum_{k=1}^3 \frac{\partial ( \frac{1}{2} \sum^3_{l=1} (y_l(\boldsymbol{x}) - d_l)^2) }{\partial y_{k}}\frac{\partial y_k}{\partial w_{ji}^{(3)}} \\\
&=&　\sum_{k=1}^3 \frac{\partial ( \frac{1}{2} \sum^3_{l=1} (y_l(\boldsymbol{x}) - d_l)^2) }{\partial y_{k}}
\frac{\sum_i w_{ki}^{(3)}z_i^{(2)}  }{\partial w_{ji}^{(3)}}\\\
&=& (y_j(\boldsymbol{x})-d_j) z_i^{(2)}
\end{eqnarray}

まずchain ruleで展開して \\(y_k\\) を間に挟む

次の式で誤差関数の自乗誤差を展開する，展開してもその中身を \\(y_k\\) で微分するだけ．

3段目でchain ruleで展開したもう一方も総和で展開する．出力層なので，式(4.3)に対応．

最終的には \\(k=l=j\\)でない項はすべて0になるので4段目の式が得られる．


# 中間層の重みの微分
（中間層は詳しめに載っている気がする．）



中間層（最初の図のInput layerからhidden layerをつなぐエッジ）の重みの微分は
\\( \frac{\partial E_n }{\partial w_{ji}^{(2)}} \\)
で表される．

\\(w_{ij}^{(2)}\\) はhidden layerのユニットが受け取るので，chain ruleを適用すれば

\begin{eqnarray}
\frac{\partial E_n }{\partial w_{ji}^{(2)}} = \frac{\partial E_n }{\partial u_j^{(2)}}  \frac{\partial u_j^{(2)}} {\partial w_{ji}^{(2)}}
\end{eqnarray}

2項目は，

\begin{eqnarray}
\frac{\partial u_j^{(2)}} {\partial w_{ji}^{(2)}} &=& \frac{\partial \sum_i w_{ji}^{(2)} z_i }{\partial w_{ji}^{(2)}} \\
  &=& z_i^{(1)}
\end{eqnarray}

つまり第1層の \\(i\\) 番目の出力．（今回は \\(x_i\\) に相当）

問題は第1項目．

以下の図の赤線で示したように \\(u_j^{(2)}\\) (hidden layerの\\(j\\)) は活性化関数 \\(f\\)が適用され，重み \\(w_{kj}  (k=1,2,3)\\) がかかってoutput layerの全てのユニットの入力となる．
（図の意味は本と同じです，線を赤いこと，ユニットの位置が異なることくらいの違いです）

![nn]({{ site.url }}/images/nn2.svg)


式4.3から \\(E_n\\) が \\(u_k^{(3)}(k=1,2,3)\\) の関数であるので，chain ruleを適用すると
\begin{eqnarray}
\frac{\partial E_n}{\partial u_j^{(2)}} &=& \sum_k \frac{\partial E_n}{\partial u_k^{(3)}} \frac{\partial u_k^{(3)}}{\partial u_j^{(2)}}
\end{eqnarray}

最初と同様に項ごとに展開する．

第1項は，\\(E_n\\)を展開するだけなので，
\begin{eqnarray}
\frac{\partial E_n}{\partial u_k^{(3)}} &=& \frac{\partial \frac{1}{2} \sum_k (u_k^{(3)} - d_k)^2}{u_k^{(3)}} \\\
&=& u_k^{(3)} - d_k
\end{eqnarray}

となる．

2項目も同様に分子を展開して微分すると

\begin{eqnarray}
\frac{\partial u_k^{(3)}}{\partial u_j^{(2)}} &=& \frac{\partial \sum_j w_{kj}^{(3)} f(u_j^{(2)}) }{\partial u_j^{(2)}} \\\
&=& w_{kj}^{(3)} f'(u_j^{(2)})
\end{eqnarray}

となる．

以上をまとめると式4.8のように


\begin{eqnarray}
\frac{\partial E_n }{\partial w_{ji}^{(2)}} = (f'(u_j^{(2)}) \sum_k w_{kj}^{(3)} (u_k^{(3)} -d_k)) z_i^{(1)}
\end{eqnarray}

となる．

微分した結果に図で示した赤い部分が現れていることがわかる．

# 所感

青い深層学習も紫の深層学習も数式が丁寧におえないような印象があるので，適宜
<a href="http://goodfeli.github.io/dlbook/">Yoshua Bengio, Ian Goodfellow and Aaron CourvilleさんたちのDeep Learning</a>を参照するといいと思った．
Chain ruleから説明があるしかなり分かりやすかった．

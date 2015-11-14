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

- 回帰を扱うネットワークなので，`output layer`の活性化関数は恒等写像
- \\(E_n\\) は，データ \\(\boldsymbol{x_n}\\) に対する誤差関数（ここでは自乗誤差），対応する正解データは， \\(\boldsymbol{d_n}\\) 
- \\(w_{ji}^{(3)}\\) 3層目の重みで`hidden layer`のユニット \\(i\\) から`output layer`のユニット \\(j\\) へのリンクの重み 
- +1 はバイアスのユニット
- `Input layer`の x1~x4 は1つデータ各次元の値，この場合は \\(\boldsymbol{x}_n\\) は4次元のベクトル
- 出力は，3次元のベクトル \\(\boldsymbol{y(x_n)}\\)
- \\(u_i^{(2)}\\) は `hidden layer`のユニット \\(i\\) の入力
- \\(z_i^{(2)}\\) は `hidden layer`のユニット \\(i\\) の出力
- \\(f\\) は活性化関数

です．

ちなみに，そもそもなんで微分を求めるかというと誤差関数を最小とするような重みを2章の勾配法によって求めるのに必要なためです．

# 出力層の重み

数学がよくわからないので微分したらなんで転置になるのかわからなくてこれが手間取った．

とりあえず愚直に総和を展開します．

微分するほうもされるほうもスカラなので結果もスカラになる．


\begin{eqnarray}
\frac{\partial E_n }{\partial w_{ji}^{(3)}} &=&
\sum_{k=1}^3 \frac{\partial E_n }{\partial y_{k}} \frac{\partial y_k }{\partial w_{ji}^{(3)}} \tag{1}\\\
&=& \sum_{k=1}^3 \frac{\partial ( \frac{1}{2} \sum^3_{l=1} (y_l(\boldsymbol{x}) - d_l)^2) }{\partial y_{k}}\frac{\partial y_k}{\partial w_{ji}^{(3)}} \tag{2}\\\
&=& \sum_{k=1}^3 \frac{\partial ( \frac{1}{2} \sum^3_{l=1} (y_l(\boldsymbol{x}) - d_l)^2) }{\partial y_{k}}
\frac{\sum_{i'} w_{ki'}^{(3)}z_{i'}^{(2)}  }{\partial w_{ji}^{(3)}} \tag{3}\\\
&=& (y_j(\boldsymbol{x})-d_j) z_i^{(2)} \tag{4}
\end{eqnarray}

![nn]({{ site.url }}/images/nn1.svg)
式1の左辺，この図の赤いリンクの重みが \\(w_{ji}^{(3)}\\) ．


![nn]({{ site.url }}/images/nn3.svg) 式1右辺，chain ruleで展開 \\(y_k\\) を間に挟む

式2，誤差関数 \\(E_n\\) を定義通り展開．

式3，chain ruleで展開したもう一方も定義に従って展開する．出力層なので，テキスト式(4.3)に対応．

式4，最終的には \\(k=l=j , i=i'\\)でない項はすべて0になる（ \\(y_1, y_2\\) は無関係）．

![nn]({{ site.url }}/images/nn4.svg)

最終的にこの赤い部分についてだけ微分すればよいとわかる

（直感的には出力層から入力層に向かって重み \\(w_{ji}^{(3)}\\) に関係する部分だけ微分してる）


# 中間層の重みの微分

(出力層から遠いほど計算がしんどくなってくるので，出力層の重みより計算は多くなりますが，がんばります．)

中間層に入る重みでの微分は
\\( \frac{\partial E_n }{\partial w_{ji}^{(2)}} \\)
で表される．

![nn]({{ site.url }}/images/nn5.svg) 

つまり赤いリンクの重みで自乗誤差を微分する．


\\(w_{ji}^{(2)}\\) は`hidden layer`のユニット \\(j\\) の入力の一部として伝わるので，chain ruleを適用する．

\begin{eqnarray}
\frac{\partial E_n }{\partial w_{ji}^{(2)}} = \frac{\partial E_n }{\partial u_j^{(2)}}  \frac{\partial u_j^{(2)}} {\partial w_{ji}^{(2)}} 
\end{eqnarray} 

このとき，2項目 \\(\frac{\partial u_j^{(2)}} {\partial w_{ji}^{(2)}}\\) は，

\begin{eqnarray}
\frac{\partial u_j^{(2)}} {\partial w_{ji}^{(2)}} &=& \frac{\partial \sum_{i'} w_{ji'}^{(2)} z_{i'}^{(1)} }{\partial w_{ji}^{(2)}} \tag{1}\\\
  &=& z_i^{(1)} \tag{2}
\end{eqnarray}


![nn]({{ site.url }}/images/nn6.svg) 

式1の右辺の分子は`Input layer`の各出力 \\(z_i^{(1)}\\) と赤いリンクの重みの積の総和．

これを \\(w_{ji}^{(2)}\\) で微分するので \\(z_i^{(1)}\\) 以外は0になる．

つまり第1層の \\(i\\) 番目の出力．（今回は \\(x_i\\) に相当）

---
 
---

---
 
---

続いて第1項目 \\(\frac{\partial E_n }{\partial u_j^{(2)}}\\) ．

\\(u_j^{(2)}\\) (`hidden layer`のユニット\\(j\\) の入力) は活性化関数 \\(f\\)が適用され，重み \\(w_{kj}^{(3)}  (k=1,2,3)\\) (下図の赤線の重み) がかかって`output layer`の全てのユニットの入力の一部となる．

![nn]({{ site.url }}/images/nn2.svg)

式4.3から \\(E_n\\) が \\(u_k^{(3)}(k=1,2,3)\\) の関数であるので，chain ruleを適用する．

\begin{eqnarray}
\frac{\partial E_n}{\partial u_j^{(2)}} &=& \sum_k \frac{\partial E_n}{\partial u_k^{(3)}} \frac{\partial u_k^{(3)}}{\partial u_j^{(2)}}
\end{eqnarray}

図で表すと赤色のユニットの入力によって微分する．

![nn]({{ site.url }}/images/nn7.svg)

項ごとに展開を行う．出力層と同じく，第1項は，\\(E_n\\)を展開する．

\begin{eqnarray}
\frac{\partial E_n}{\partial u_k^{(3)}} &=& \frac{\partial \frac{1}{2} \sum_{k^{'}} (u_{k^{'}}^{(3)} - d_{k^{'}})^2}{\partial u_k^{(3)}} \\\
&=& u_k^{(3)} - d_k
\end{eqnarray}

となる．

 \\(y1\\) ~ \\(y3\\) (図の赤い\\(y1\\) ~ \\(y3\\)) からそれぞれの正解の値 \\(d_k\\) との差の総和が分子で，それを \\(k\\) の入力で微分しているので，結局図の\\(y1\\)しか残らない．

今回は， \\( y_k = z_k^{(3)} = u_k^{(3)} \\) であるので簡単に求められている．

![nn]({{ site.url }}/images/nn8.svg)

---
 
---

---
 
---

2項目\\(\frac{\partial u_k^{(3)}}{\partial u_j^{(2)}}\\)も同様に分子を展開して微分する．

微分する前に確認すると，\\(k\\)の入力を \\(j\\)の入力で微分するので，赤い部分に注目していることになる．

![nn]({{ site.url }}/images/nn9.svg) 


\begin{eqnarray}
\frac{\partial u_k^{(3)}}{\partial u_j^{(2)}} &=& \frac{\partial \sum_{j'} w_{k{j'}}^{(3)} f(u_{j'}^{(2)}) }{\partial u_j^{(2)}} \tag{1}\\\
&=& w_{kj}^{(3)} f'(u_j^{(2)}) \tag{2}
\end{eqnarray}

式1は分子にあるユニット \\(k\\) の入力を展開しているので，下図の赤いリンクの重みと赤いノードのユニットの出力の形で書き直しているだけ．

![nn]({{ site.url }}/images/nn10.svg) 

\\(u_j^{(2)}\\) で微分するので，結局分子が \\(j=j'\\)のときだけが残るので，式2となる．


以上をまとめると


\begin{eqnarray}
\frac{\partial E_n }{\partial w_{ji}^{(2)}} = (f'(u_j^{(2)}) \sum_k w_{kj}^{(3)} (u_k^{(3)} -d_k)) z_i^{(1)}
\end{eqnarray}

となる．


# 所感

青い深層学習も紫の深層学習も数式が丁寧におえないような印象があるので，適宜
<a href="http://goodfeli.github.io/dlbook/">Yoshua Bengio, Ian Goodfellow and Aaron CourvilleさんたちのDeep Learning</a>を参照するといいと思った．
Chain ruleから説明があるしかなり分かりやすかった．

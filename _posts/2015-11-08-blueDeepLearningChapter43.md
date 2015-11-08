---
layout: post
title: "青深層学習 4.3 多層ネットワークへの一般化"
date: 2015-11-09 01:22:00 +0900
comments: false
---

# はじめに
前回 [青深層学習，誤差逆伝播法の計算](http://nzw0301.github.io/2015/11/blueDeepLearningChapter42/ "青深層学習，誤差逆伝播法の計算")
の続きです．

誤差逆伝播を層が全体で3層だけの場合ではなく，\\(L\\)層に拡張した時の挙動を確認します．

前回と赤で強調する場所が違うかもしれませんが，ご了承ください．
# 本題

第\\(l\\)層の重み\\(w_{ji}^{(l)}\\)で誤差関数を微分することを考える．

前回と同じくネットワークを示すと赤いリンクの重みで誤差関数を微分する．\\(l+1\\) 層にもバイアスはある気がするので，ここでは書いている．

![nn]({{ site.url }}/images/nn431.svg)

前回の中間層の重みの微分と同じく，\\(w_{ji}^{(l)}\\)は\\(l\\)層のユニット\\(j\\)の総入力\\(u_j^{(l)}\\)の一部なので，chain ruleを使って展開する(式1)．

\begin{eqnarray}
\frac{\partial E_n }{\partial w_{ji}^{(l)}} &=&
\frac{\partial E_n }{\partial u_j^{(l)}} \frac{\partial u_j^{(l)} }{\partial w_{ji}^{(l)}} \tag{1}\\\
\end{eqnarray}

式1の第1項\\(\frac{\partial E_n }{\partial u_j^{(l)}}\\)をまず展開する．
下ぼネットワークで示したように
\\(u_j^{(l)}\\)は，活性化関数\\(f\\)が適用され，
出力\\(z_j^{(l)}\\)になり，赤いリンクの重みがかかって\\(l+1\\)層のユニット((\\(l+1\\))層のバイアス以外のユニット)入力の一部になる．

![nn]({{ site.url }}/images/nn432.svg)

なので，\\(E_n\\)を微分するために，chain ruleで展開する．


\begin{eqnarray}
\frac{\partial E_n }{\partial u_{j}^{(l)}} &=&
\sum_{k=1}^{K} \frac{\partial E_n }{\partial u_k^{(l+1)}} \frac{\partial u_k^{(l+1)} }{\partial u_j^{(l)}} \tag{2}\\\
\end{eqnarray}

ここで式3のようにデルタを定義する．
デルタは各層の各ユニットに存在する．

\begin{eqnarray}
\delta_j^{(l)} \equiv 
  \frac{\partial E_n }{\partial u_{j}^{(l)}} \tag{3}
\end{eqnarray}

式2を式3を使った形で展開する．

式2の右辺を項ごとに展開する．
\\(\frac{\partial E_n }{\partial u_k^{(l+1)}} \frac{\partial u_k^{(l+1)} }{\partial u_j^{(l)}}\\)の1項目は，式3のデルタの層が違うだけなので，

\begin{eqnarray}
\frac{\partial E_n }{\partial u_k^{(l+1)}} = \delta_k^{(l+1)} \tag{4}
\end{eqnarray}

2項目 \\(\frac{\partial u_k^{(l+1)} }{\partial u_j^{(l)}}\\)は，前回展開やったように定義に戻って展開する．

\begin{eqnarray}
\frac{\partial u_k^{(l+1)} }{\partial u_{j}^{(l)}} &=& \frac{\partial \sum_{j'} w_{kj'}^{(l+1)} z_{j'}^{(l)} }{\partial u_j^{(l)}} \tag{5} \\\
&=& \frac{\partial \sum_{j'} w_{kj'}^{(l+1)} f(u_{j'}^{(l)}) }{\partial u_j^{(l)}} \tag{6} \\\
&=&  w_{kj}^{(l+1)} f'(u_{j}^{(l)})  \tag{7} \\\
\end{eqnarray}

よって式2に式4と式6を代入するとデルタの関係式が得られる．


\begin{eqnarray}
\delta_j^{(l)}  &=& \sum_{k=1}^{K} \delta_k^{(l+1)} (w_{kj}^{(l+1)} f'(u_{j}^{(l)})) \tag{8}
\end{eqnarray}

これは\\(l\\)層のデルタは(\\(l+1\\))層の全デルタで計算されることを示す．
（くどいが，最終的に必要なデルタは式1の1項目であり，\\(L\\)層から(\\(l+1\\))層までの全デルタを順伝播とは逆向きに求める．これが逆伝播の由来らしい）

式1の2項目は簡単に求められる．（前回の中間層の重みと同じ）
\begin{eqnarray}
\frac{\partial u_j^{(l)}} {\partial w_{ji}^{(l)}} &=& \frac{\partial \sum_{i'} w_{ji'}^{(l)} z_{i'}^{(l-1)} }{\partial w_{ji}^{(l)}} \tag{9}\\\
  &=& z_i^{(l-1)} \tag{10}
\end{eqnarray}

式1に式8と式10を代入すれば任意の重みがデルタと\\(z\\)で表現できる．

\begin{eqnarray}
\frac{\partial E_n }{\partial w_{ji}^{(l)}} &=&
\delta_j^{(l)} z_i^{(l-1)} \tag{11}\\\
\end{eqnarray}


式8の通り，デルタは漸化式の形をしている．

最初のデルタは第\\(L\\)層のデルタであり，
つまりは，誤差関数を出力層の入力\\(u_j^{(L)}\\)の微分である．

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

中間層はこれをほぼおなじやり方でchain ruleと関係式の展開を行っていくので，近いうちに書きます．

青い深層学習も紫の深層学習も数式が丁寧に負えないような印象があるので，適宜
<a href="http://goodfeli.github.io/dlbook/">Yoshua Bengio, Ian Goodfellow and Aaron CourvilleさんたちのDeep Learning</a>を参照するといいと思った．
Chain ruleから説明があるしかなり分かりやすかった．

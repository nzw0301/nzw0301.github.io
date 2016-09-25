---
layout: post
title: Latex command list
date: 2016-09-25 24:00:00 +0900
comments: false
---


# 式内の項や演算子に色をつける

`\textcolor{red}{\eta}` とすると $$\eta$$ が赤くなる．
mathjaxではだめらしい．

# 式番号を任意の文字に変える

`\tag{A}`

```tex
\begin{align}
\eta = 1.0 \tag{A} \\
\phi = 2.0 \tag{B}
\end{align}
```

# 画像としてpdfを読み込む

グラフなどはPDF形式で出力することにしている．
`awesome.pdf` というファイルにグラフがある場合は以下のようにする．


```tex
\begin{figure}[tb]
\centering
\includegraphics[width=7cm]{./images/awesome.pdf}
\caption{\label{fig:image1}
awesome image
}
\end{figure}
```

日本の学会のテンプレのままplatexでコンパイルすると次のようなエラーを出力されることがある．

```! LaTeX Error: Cannot determine size of graphic in ./images/lda.pdf (no Boundin
gBox).```

この場合は，ファイル先頭あたりにある `\usepackage{graphicx}` を `\usepackage[dvipdfmx]{graphicx}` とすればよい．

# よく使うが覚えられない記号など

- $$\propto$$ : ``\propto``
- $$\prod$$ : ``\prod``
- $$\mathbb{R}$$ : `\mathbb{R}`

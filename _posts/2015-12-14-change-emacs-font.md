---
layout: post
title: emacsのデフォルトのフォントを変える
date: 2015-12-14 00:00:00 +0900
comments: false
---

## 概略
Macでemacsを立ち上げたときのデフォルトのフォントを変更

## 環境
- Mac yosemite
- `emacs` 24.5

`prelude` と `Ricty Diminished Discord`は導入済みとする

## 本題
`~/.emacs.d/personal/settings.el`にもろもろの設定を記述しているのでそこに1行加えるだけ．
使えるフォントの一覧は，`Font Book`の一覧から確認できる．


デフォルトのフォントを変えるだけなら以下のような1行を加えるだけ．

```lisp
~省略~
(add-to-list 'default-frame-alist '(font . "Ricty Diminished Discord"))
```

さらにフォントサイズを指定する場合はフォント名の後に`-fontSize`を付ける．

```lisp
~省略~
(add-to-list 'default-frame-alist '(font . "Ricty Diminished Discord-15"))
```

以上です．

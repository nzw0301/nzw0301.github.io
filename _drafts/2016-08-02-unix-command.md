r---
layout: post
title: Unix command list for me
date: 2016-08-02 21:20:00 +0900
comments: false
---


# open pattern matched files in the current directory

Ex. open pdf files:

`find . -name "*.pdf" | xargs open`

Ex. open all files:

`∫ find . -type f -exec open '{}' \;`

# convert pdf to text file

`for f in *.pdf; do pdftotext "$f"; done`

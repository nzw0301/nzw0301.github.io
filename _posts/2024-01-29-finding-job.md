---
layout: post
title: "怪文書：転"
---

本題と関係ないSirSLowのエピソードです。

<iframe width="560" height="315" src="https://www.youtube.com/embed/MgE-e65W5oI?si=QiCfXR3ocH3R1yUn" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

------

### 私について

表現学習の理論寄りの研究で博士号取得後、IBM Research – Tokyo でResearch Scientistとして研究開発を1年4ヶ月やりました。在職中の論文出版はありませんでした。私のせいです。

職歴・学歴・研究業績はこのページの右上にある `CV (PDF)` 、エンジニアリングで公的な成果は [GitHub](https://github.com/nzw0301) にある通りです。

### 転職活動をやるぞ！！

IBMの同僚である数理科学チームと給与には不満はありませんでしたし、働き方もかなり自由でした。同僚の皆さん本当にお世話になりました。なんで辞めるのかというと、業務上でしか知り得ない話になるので、書けません。

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">I get asked a lot: why stay in academia, all the excitement in AI is happening in industry with massive compute. And I am seeing some profs leaving academia, but also seeing lots of researchers in industry looking to go back to academia, especially those who don’t work on LLMs.…</p>&mdash; Russ Salakhutdinov (@rsalakhu) <a href="https://twitter.com/rsalakhu/status/1702702142640042386?ref_src=twsrc%5Etfw">September 15, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

このような観点もあるようです。

### 考慮した点

可能であれば研究を続けたかったので、業務時間に論文執筆が可能なポジションで探しました。以前よりもいわゆる開発の割合が増えてもいいと思ったので、（90% とか）そのように面接で話していました。また、新卒の時とおよそ同じで、以下のことを気にしていました。

- 同僚になる方々と働きたいと思えるか
- 定期的に論文が国際会議等に通っているか
- 金銭面の待遇：前職の初期値以上（具体的には賞与込みで814万円+確定拠出年金が私のポジションの給与としてインターネットに公開されていましたね）
    - 私なんかがこんなにもらえていいのかという気持ちはありましたが、様々な理由で、ここから大きく下げることは考えませんでした
- 任期なし
    - 今後想定されるライフイベントで数ヶ月仕事を止める場合、任期付きで成果が求められるポジションだと、雇用主側からしても好ましくないと思いました
- 裁量労働制：私は夜型で昼頃から働くことが多いためです
- 在宅勤務：居住地による制限です
- 業務内容なりが自分が使っているサービス・興味に関連することか

とはいえ、2023年の初めに複数の企業でレイオフが行われていたため、上記をすべて満たすのは私の能力的には高望みだとポジションを調べていて思ったので、この条件から妥協点はするだろうと思いました。また前回の就活のときにも感じたのですが、私は博士後期課程の時のような理論寄りの研究を会社で続けたいとは言ってないんですが、私のこれまでの業績は企業側からすると続けたいと思われるのか、私は使いにくそうな印象を持っているようで、その辺りを不利な印象を受けました。

### 活動

11月の中旬くらいから始めました。上記をXに書くと叩かれまくる気がしたのとギリギリまで社内に希望を持っていたので、ソーシャルメディア等には何も書きませんでした（例外はLinkedInのステータス）。前回の就活でリファラルを知人からもらった方が選考が有利だと思ったので、まずは友人に相談しました。転職エージェントも利用しましたが、あまり条件の満たされるものがなく、カジュアル面談でもあまり歓迎されていないような印象を受けたので先に進みませんでした（面談の方はそういう意図はなかったかもしれませんが私が受けた印象です）。LinkedInで会社の人事の方が直接面談を設定した場合は話を聞きました。また、知人が基本的に一社に集中していたこともあり、いくつか知り合いがいない会社にも直接応募しました。ちなみに、カジュアル面談2社、書類面接落ちが2社、2次面接落ちが1社、2時面接（？）後にこちらから辞退が1社、内定先1社でした。

### R&D on LLM or Not

これで悩みました。LLMが流行っていて、機械学習の研究者のポジションはこれにかなり置き換わっている印象を受けました（そうでもなかったらすいません）。博士後期課程で研究していた教師なし表現学習は、最近のLLMとパイプラインが類似し、多段の学習が行われるため、馴染みはありました。これに関するポジションであれば、なんとか職にありつけるだろうと思っていました。一方で、これ系を作るためには、かなりの計算リソースが必要で、それがあるに所へ行った方がよいという印象を受けました。もちろん[phi](https://arxiv.org/abs/2309.05463) のような方向性や memory efficient fine-tuning（あるいはparameter efficient fine-tuning）の方向性はありますが、世界中で計算コストを下げたいニーズが存在するので、この領域もかなり競争的な気がします。また、あまりにLLM関係に過集中されている状況もどうなんだろうかと思いました。

とはいえ自分の好きなML理論系の研究者たち [[1](https://pli.princeton.edu/about-pli/directors-message), [2](https://www.voyageai.com/about)]もこの分野に腰を据えているような気がしますし、機械学習の学会でもこれ系も話題・論文が多いので、やることにしました。

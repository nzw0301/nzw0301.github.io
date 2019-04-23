---
layout: page
title: 論文等
permalink: /publications_ja/
---

最終更新日: 2019年02月09日

日本語論文のみ，[英語論文のリストはこちら (English Publication list is here.)]({{site.url}}/publications)

末尾に `[1]` があるものは簡単な背景的なものが書いてあります。

## 論文誌

1. <u>野沢 健人</u>, 若林 啓. __トピックモデルに基づく大規模ネットワークの重複コミュニティ発見__. _IPSJ Transaction on Database_, vol.9, no.2, pp.1--10, 2016. <br /> [[pdf](https://ipsj.ixsq.nii.ac.jp/ej/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=165288&item_no=1&page_id=13&block_id=8)]. [[^2]].
{: reversed="reversed"}
---

## 国内会議（査読有）

1. <u>野沢 健人</u>, 若林 啓. __トピックモデルに基づく大規模ネットワークの重複コミュニティ発見__. _[第8回 Webとデータベースに関するフォーラム (WebDB Forum)](http://db-event.jpn.org/webdbf2015/)_, 2015. <br /> [優秀論文賞](http://db-event.jpn.org/webdbf2015/award.php), [2016年度コンピュータサイエンス領域奨励賞](https://www.ipsj.or.jp/award/cs-award-2016.html) <br /> [[slide](https://speakerdeck.com/nzw0301/topitukumoderuniyorufen-san-biao-xian-huo-de-shou-fa-falseti-an)], [[pdf](https://ipsj.ixsq.nii.ac.jp/ej/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=146098&item_no=1&page_id=13&block_id=8)]. [[^2]].
{: reversed="reversed"}

---

## 国内会議・研究会（査読無）

1. <u>野沢 健人</u>, 若林 啓. __ランダムウォークによる擬似文書を用いたトピックモデルの学習__. _[第19回情報論的学習理論ワークショップ (IBIS)](http://ibisml.org/ibis2016/)_, 2016. [[^4]].
1. <u>野沢 健人</u>, 星野 貴行, 福田拓也, 兼村厚範. __脳波データへの深層学習の適用__. _[第19回情報論的学習理論ワークショップ (IBIS)](http://ibisml.org/ibis2016/)_, 2016. NOTE: ポスターのみ，産総研のRAとして発表．
1. <u>野沢 健人</u>, 若林 啓. __トピックモデルによる分散表現の獲得手法の提案__. _[言語処理学会第22回年次大会 (NLP)](http://www.anlp.jp/nlp2016/)_, 2016. <br /> [[slide](https://speakerdeck.com/nzw0301/topitukumoderuniyorufen-san-biao-xian-huo-de-shou-fa-falseti-an)], [[pdf](http://www.anlp.jp/proceedings/annual_meeting/2016/pdf_dir/B3-2.pdf)]. [[^3]].
1. <u>野沢 健人</u>, 中岡 義貴, 山本 修平, 佐藤 哲司. __word2vecを用いた代替食材の発見手法の提案__. _電子情報通信学会技術研究報告. DE, データ工学_, 2014. [[^1]].
{: reversed="reversed"}

---

## 学位論文

- トピックモデルを用いたグラフ表現に対する潜在的意味解析に関する研究. 平成29年度 筑波大学大学院 図書館情報メディア研究科 図書館情報メディア専攻 情報学プログラム 修士論文.
- トピックモデルによる単語の分散表現獲得手法に関する研究. 平成27年度 筑波大学情報学群知識情報・図書館情報学類 卒業研究論文.

---

[^2]: [似たような研究（LDA をグラフに使う）](https://dl.acm.org/citation.cfm?id=1529607)があり、それに高速な推論アルゴリズムでやってみたらどうなるかといったところで、適用してみました系。夏休みあたりにやりました。なんか賞をいただきました。
[^1]: 学部で NII が提供しているデータを学生に渡して、形態素解析なりネットワーク分析なりで遊ばせる講義を受講していました。教員が「査読問わず論文を書いたら一番いい評価をあげよう」という話でやってみました。応用としては国内ではだいぶ早くやった気がしています。やったことは単純で、レシピの手順から単語の分散表現を求めて、似てる食材を見つけてみようというものです。評価方法がお気に入りで、レシピサイトは他の人が作ったときのコメントがついていて、そこになぜか「OOがなかったのでXXを使いました」といった知恵を書いてる人たちが少なからずいたのでそれを使いました。
[^3]: 卒論です。LDA は普通文書単位で学習しますが、ある単語の共起語の多重集合を単位と学習すれば単語単位で確率ベクトルが推定できます。（LDA の $$\boldsymbol{\theta}$$ 相当です）これが分散表現的なものになります。モチベーションとしては、単語ベクトルが確率ベクトルで表現されてるので、word2vec よりは解釈しやすいでしょうというものです。性能はかなり劣ります。ちなみに、このとき SVI を使っていたので、文書の中を更にサブサンプリングしてもそこそこ動いたのが印象的でした。続けてませんが。
[^4]: IBIS2016 に出したいと行って無理やり考えたものです。LDA は短文書が苦手というのはよく言われているのでそれをどうするかで方向としてはモデルを拡張する方向と、入力をいじる方向があって、自分は後者を取りました。そのほうが速いアルゴリズムを適用しやすいからとか応用的な理由です。短文書を作るときにTF-IDFで重み付けしたグラフ上で random walk させてそれを文書だと思って学習させます。既存のグラフベースのやり方よりは高速かつ（coherence の意味で）良かったです。

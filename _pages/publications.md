---
layout: page
permalink: /
title:
years: [2021,2020,2019,2018,2017]
nav: true
---


__Kento Nozawa__ is a 4th year Ph.D. student who does research on machine learning. His current research interests are _self-supervised learning and PAC-Bayes theory_.
 He is supervised by [Dr. Issei Sato](https://www.ml.is.s.u-tokyo.ac.jp/issei-sato-en) at [Issei Sato Lab](https://www.ml.is.s.u-tokyo.ac.jp/home-en).

__I am probably on the 2021-2023 job market.__

He is also a part-time research assistant at [RIKEN AIP](https://aip.riken.jp/).

During summer 2019, he visited at [UCL AI Centre](https://www.ucl.ac.uk/ai-centre/) and [Modal team](https://team.inria.fr/modal/) Inria Lille Nord Europe to work on [PAC-Bayes and contrastive representation learning](https://arxiv.org/abs/1910.04464).

---

<h2>Publications</h2>
<div class="publications">

{% for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>

<a href="{{ '/publications_ja/' | prepend: site.url }}">Publications written in Japanese</a>

<div class="social">
  {% include social.html %}
  <div class="contact-note">{{ site.contact_note }}</div>
</div>

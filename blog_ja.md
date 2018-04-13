---
layout: default
title: Blog archive
---
<div class="page-content wc-container">
  <h1>Blog Archive</h1>
  {% for post in site.posts %}
    {% if post.lang != "english" %}
    {% capture currentyear %}{{post.date | date: "%Y"}}{% endcapture %}
    {% if currentyear != year %}
        <h5>{{ currentyear }}</h5>
            <ul class="posts">
        {% capture year %}{{currentyear}}{% endcapture %}
    {% endif %}
    <li>{{ post.date | date:'%b %d' }}: <a href="{{ post.url | prepend: site.baseul }}">{{ post.title }}</a></li>
    {% endif %}
  {% endfor %}

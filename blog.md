---
layout: page
title: Blog
permalink: /blog/
---

<div class="post">
    <h3>English</h3>
    {% for post in site.posts %}
        {% if post.lang == "english" %}
            <p class="post-meta">[{{ post.date | date: '%B %-d, %Y' }}] <a class="post-title" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a></p>
        {% endif %}
    {% endfor %}
    <br />

    {% for post in site.posts %}
        {% if post.lang != "english" %}
            <p class="post-meta">[{{ post.date | date: '%B %-d, %Y' }}] <a class="post-title" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a></p>
        {% endif %}
    {% endfor %}
</div>

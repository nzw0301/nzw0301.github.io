---
layout: page
title: Blog
permalink: /blog/
date: 2022-09-02
---

<div class="post">
    <h3>English</h3>
    <ul>
    {% for post in site.posts %}
        {% if post.lang == "english" %}
            <li>
                <a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
                <sub>[{{ post.date | date: '%d %B %Y' }}]</sub>
            </li>
        {% endif %}
    {% endfor %}
    </ul>

    <h3>Japanese</h3>
    <ul>
    {% for post in site.posts %}
        {% if post.lang != "english" %}
            <li>
                <a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
                <sub>[{{ post.date | date: '%d %B %Y' }}]</sub>
            </li>
        {% endif %}
    {% endfor %}
    </ul>
</div>

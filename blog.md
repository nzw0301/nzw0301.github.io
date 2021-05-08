---
layout: page
title: Blog
permalink: /blog/
---

<div class="post">
    <h3>English</h3>
    <ul>
    {% for post in site.posts %}
        {% if post.lang == "english" %}
            <li> [{{ post.date | date: '%d %B %Y' }}]
                <a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </li>
        {% endif %}
    {% endfor %}
    </ul>

    <h3>Japanese</h3>
    <ul>
    {% for post in site.posts %}
        {% if post.lang != "english" %}
            <li> [{{ post.date | date: '%d %B %Y' }}]
                <a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
            </li>
        {% endif %}
    {% endfor %}
    </ul>
</div>

---
layout: page
title:  Recents Posts
---
{% include JB/setup %}

<ul class="posts">
{% for post in site.posts  limit:10 %}
    <a href="{{ BASE_PATH }}{{ post.url }}"><h2> {{ post.title }}<br /></h2></a>
	<u>{{ post.date | date_to_string }}<br /></u> 
        {{ post.content | strip_html | truncatewords:75}}
            <a href="{{ post.url }}">Read more...</a>
    {% endfor %}
</ul>

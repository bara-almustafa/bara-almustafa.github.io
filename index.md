---
layout: default
---

# Welcome

Write-ups and notes by 0xcybersoldier.

## Posts

{% if site.posts.size == 0 %}
No posts yet.
{% endif %}

{% for post in site.posts %}
- {{ post.date | date: "%-d %B %Y" }} — [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}

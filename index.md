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

## Sponsor the project

If my write-ups, tools or apps are useful to you, you can sponsor my work:

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/0xcybersoldier)

☕ **[buymeacoffee.com/0xcybersoldier](https://buymeacoffee.com/0xcybersoldier)**

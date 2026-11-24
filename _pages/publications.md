---
layout: page
permalink: /publications/
title: publications
description: Reverse chronological order.
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

{% include bib_search.liquid %}

<div class="publications">

<h2>Journal Articles</h2>
{% bibliography --query @article %}

<h2>International Conferences</h2>
{% bibliography --query @inproceedings %}

<h2>Domestic Conferences</h2>
{% bibliography --file domestic %}

<h2>Patents</h2>
{% bibliography --file patents %}

</div>

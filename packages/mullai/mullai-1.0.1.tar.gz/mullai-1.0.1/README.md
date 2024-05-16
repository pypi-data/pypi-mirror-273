# Setup Package for release

pip install -e .

python setup.py sdist bdist_wheel
twine upload dist/*


# Front-matter

```
---
title: {{ page.generator.related.book[0].title }}
generator:
    from: mysql
    db: nool
    host: localhost
    port: 3306
    username: root
    password: 
    table: page
    limit: 3
    related:
        -
            table: book 
            where: bookId='{{ page.generator.rows[0].bookId }}'
            limit: 1
    dumpTo: api/pages.json
description: this is a page that will show data
test: this is me2
layout: base
permalink: {{ page.generator.related.book[0].thangtitle | slugify }}/page/{{ page.generator.row.pageNum }}
---
```


access local variable using `page` object, and inside `generator.related` you can access the rows query by using `page.generator.rows`. You can dump `rows` and `related` to a JSON file, this can help you to load them into your website and make static search easier.




# Example MySQL generator

```
---
title: {{ page.generator.related.book[0].title }}
generator:
    from: mysql
    db: nool
    host: localhost
    port: 3306
    username: root
    password: 
    table: page
    limit: 3
    related:
        -
            table: book 
            where: bookId='{{ page.generator.rows[0].bookId }}'
            limit: 1
description: this is a page that will show data
test: this is me2
layout: base
permalink: {{ page.generator.related.book[0].thangtitle | slugify }}/page/{{ page.generator.row.pageNum }}
---
```


```
{% set items = json.parse(page.generator.row.content) %}


{% for item in items %}

{{ item.line }}

{% endfor %}
```

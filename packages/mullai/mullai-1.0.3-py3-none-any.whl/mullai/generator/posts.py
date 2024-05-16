#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2024 suyambu developers (http://suyambu.net/gasper)
See the file 'LICENSE' for copying permission
"""

import os
from datetime import datetime
from markdown import markdown


def generate(gasper, path, plugin=None):
    output = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            src_path = os.path.join(subdir, file)
            filename = os.path.basename(src_path)
            nodes = filename.split("-")
            year = int(nodes.pop(0))
            month = int(nodes.pop(0))
            day = int(nodes.pop(0))
            
            filename = "-".join(nodes)
            date = datetime(year, month, day)
            formated_date = date.strftime("%b %d, %Y")
            
            nodes = filename.split(".")
            nodes.pop()
            filename = ".".join(nodes)
            
            matter = {
                "date": formated_date,
                "filename": filename,
                "permalink": f"{year}/{month}/{day}/{filename}"
            }
            dummy = matter
            for _ in range(2):
                (dummy, _) = gasper.extract_frontmatter(src_path, dummy, debug=True)
            (init_matter, content) = gasper.extract_frontmatter(src_path, dummy, debug=True)
            matter.update(init_matter)
            
            content = gasper.env.from_string(content).render(page=matter, content=None, site=gasper.config)
            
            if src_path.endswith(".md") or src_path.endswith(".markdown"):
                content = markdown(content, extensions=['fenced_code'])
            
            matter["content"] = content
            output.append(matter)
    
    if plugin is not None:
        m = __import__(plugin)
        output = m.plugin(output)
    
    return output
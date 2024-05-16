#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2024 suyambu developers (http://suyambu.net/gasper)
See the file 'LICENSE' for copying permission
"""


import json


def generate(gasper, path, exclude=None, limit=None, plugin=None, reverse=False):
    with open(path, "r") as f:
        data = json.loads(f.read())
        
    if type(data) is not list:
        data = [data]
    
    output = []
    for d in data:
        if exclude is not None:
            for ex in exclude:
                d.pop(ex)
        output.append(d)
        
    if reverse:
        output.reverse()
    
    if limit is not None:
        output = output[:limit]
    
    if plugin is not None:
        m = __import__(plugin)
        output = m.plugin(output)
    
    return output

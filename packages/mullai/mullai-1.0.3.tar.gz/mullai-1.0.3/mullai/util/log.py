#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2024 suyambu developers (http://suyambu.net/gasper)
See the file 'LICENSE' for copying permission
"""


from .colorify import blue, red, green, yellow, green_bg, black, bold


def info(s):
    print("[{}] {}".format(bold(blue("*")), s))


def warn(s):
    print("[{}] {}".format(bold(yellow("!")), s))


def error(s):
    print("[{}] {}".format(bold(red("-")), s))


def success(s):
    print("[{}] {}".format(bold(green("+")), s))
#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2024 suyambu developers (http://suyambu.net/gasper)
See the file 'LICENSE' for copying permission
"""

from peewee import *


def generate(gasper, db, table, host, port, username, password, where=None, limit=None, order=None, only=None, unique=False, plugin=None):
    database = MySQLDatabase(db, host=host, port=port, user=username, passwd=password)
    cursor = database.execute_sql(f"SHOW COLUMNS FROM {db}.{table};")
    col_names = cursor.fetchall()
    output = []
    query = f"SELECT * FROM {table}"
    if where:
        query += f" WHERE {where}"
    if order:
        query += f" ORDER {order}"
    if limit:
        query += f" LIMIT {limit}"
    cursor = database.execute_sql(query)
    for row in cursor.fetchall():
        output.append({})
        for i, col in enumerate(row):
            output[-1][col_names[i][0]] = col
    
    if only is not None:
        tmp = []
        cols = list(map(lambda x: x.strip(), only.split(",")))
        for out in output:
            tmp.append({})
            for k, v in out.items():
                if k in cols:
                    tmp[-1][k] = v
        output = tmp
        
    if unique:
        tmp = []
        matches = []
        for out in output:
            m = "".join(map(lambda x: str(x), out.values()))
            if m in matches:
                continue
            matches.append(m)
            tmp.append({})
            for k, v in out.items():
                tmp[-1][k] = v
                    
        output = tmp

    if plugin is not None:
        m = __import__(plugin)
        output = m.plugin(output)

    return output



if __name__ == "__main__":
    generate(db="automator", table="user", host="localhost", port=3306, username="root", password="rockjeev")

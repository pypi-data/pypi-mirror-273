def any_startswith(c, parts):
    doesit = False
    for part in parts:
        if part.startswith(c):
            doesit = True
            break
    return doesit

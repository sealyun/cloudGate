def checkKey(ob, *args):
    for k in args:
        if k not in ob:
            ob[k] = None
    return ob

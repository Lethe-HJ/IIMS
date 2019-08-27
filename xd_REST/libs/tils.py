

def str_boolean(str_bool):
    if type(str_bool) is bool:
        return str_bool
    str_bool = str_bool.capitalize()
    return True if str_bool == "True" else False

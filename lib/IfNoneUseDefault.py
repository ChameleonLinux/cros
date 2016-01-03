def get(input, default, FalseIsNone=False):
    if input == None:
        return default
    if FalseIsNone and input == False:
        return default
    return input

# For dictionaries
def get_d(dict_, key, default):
    if key in dict_:
        if isinstance(dict_[key], str):
            if dict_[key].lower() == "True": return True
            if dict_[key].lower() == "False": return False
        return dict_[key]
    return default

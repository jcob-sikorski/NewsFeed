def jsonLoad(file_name):
    # for saving friends of an account
    import json
    with open(file_name, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data
def jsonSave(file_name=None, file_content=None):
    '''Saves data on json file.
    file_name: the file name of the data
    file_content: the data you want to save
    '''
    import json

    # write to JSON
    with open(file_name, 'w', encoding="utf-8") as f:
        json.dump(file_content, f, ensure_ascii=False, indent=4)
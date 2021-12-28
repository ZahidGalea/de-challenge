def read_json_file(json_file_path, logger):
    import json
    with open(json_file_path) as j:
        file_readed = json.load(j)
        logger.info(f'Json file readed {json_file_path}')
    return file_readed

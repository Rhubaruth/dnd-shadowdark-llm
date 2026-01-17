from utils import file2dict


def get_last_id(file_path):
    # Find last id
    last_id: int = -1
    for out in file2dict(file_path):
        this_id = out['id']
        if this_id > last_id:
            last_id = this_id
    return last_id

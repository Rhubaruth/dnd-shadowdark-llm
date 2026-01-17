def file2dict(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            doc_dict = {'id': -1}
            content_lines = []
            for line in file:
                if line.startswith('<doc'):
                    id_start = line.find('"')
                    if id_start == -1:
                        doc_dict['id'] = 404
                        content_lines = []
                        continue
                    id_end = line.find('"', id_start+1)
                    doc_dict['id'] = int(line[id_start+1:id_end])
                    content_lines = []
                elif line.startswith('<status>'):
                    status_start = line.find('>')
                    status_end = line.find('<', status_start+1)
                    doc_dict['status'] = line[id_start+1:status_end]
                elif line.startswith('<model'):
                    # parse model name
                    pass
                elif line.startswith('<duration'):
                    dur_start = line.find('>')
                    dur_end = line.find('<', dur_start+1)
                    doc_dict['duration'] = float(line[dur_start+1:dur_end])
                elif line.startswith('</doc'):
                    doc_dict['content'] = content_lines
                    yield doc_dict
                    # reset variables
                    doc_dict = {'id': -1}
                    content_lines = []
                elif line.startswith('<'):
                    # skip lines with tag
                    continue
                else:
                    content_lines.append(line)
            if doc_dict['id'] != -1:
                doc_dict['content'] = content_lines
                yield doc_dict
    except FileNotFoundError:
        print(f'File {file_path} does not exists.')
        return

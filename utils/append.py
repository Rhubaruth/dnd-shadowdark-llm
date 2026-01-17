def append_to_file(
    file_name: str,
    content: dict,
    model: str = ""
):
    try:
        with open(file_name, 'a+') as file:
            lines = [
                "<doc>\n",
                content['content'],
                "\n",
            ]
            if 'status' in content:
                lines.append(f"<status>{content['status']}</status>\n")
            if 'duration' in content:
                lines.append(f"<duration>{content['duration']}</duration>\n")
            if 'model' in content:
                lines.append(f"<model>{content['model']}</model>\n")
            elif model:
                lines.append(f"<model>{model}</model>\n")
            lines.append("</doc>\n")
            file.writelines(lines)
    except TypeError as e:
        print('ERROR append.py:', e)
        print('lines type: ')
        for li in lines:
            print(type(li), ': ', li)


def append_to_plain(file_name: str, content: dict):
    with open(file_name, 'a') as file:
        file.writelines(content)

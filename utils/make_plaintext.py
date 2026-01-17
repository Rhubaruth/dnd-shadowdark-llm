from pathlib import Path
from .append import append_to_plain


def make_plaintext_from(file, name: str = 'test'):
    out_path = f"out/plaintext/{name}"
    Path("out/plaintext/").mkdir(parents=True, exist_ok=True)

    print('File:', out_path)

    if Path(out_path).exists():
        print(f'Plain File {out_path} exists')
        return 1

    for line in file:
        if type(line) is dict:
            line = ''.join(line['content'])
        append_to_plain(out_path, line)
    return 0

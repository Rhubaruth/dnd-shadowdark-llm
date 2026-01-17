def read_czeng(
    file_path: str,
    paragraph_size: int = 100,
) -> [str]:
    """
    Read czeng07 dataset files.
    Splits into paragraphs by number of words (includes whole sentences).

    :param str file_path: Path to the file
    :param int paragraph_size: Number of sentences that counts as paragraph
    :param int batch_size: Number of paragraphs that this will return at once

    :return: List of batched paragraphs
    :rtype: [str]
    """
    with open(file_path, 'r') as file:
        paragraph = []
        sentences = 0
        for line in file:
            if line.startswith('</para'):
                paragraph.append('\n')
            elif line.startswith('<w'):
                word_start = line.find(">")+1
                word_end = line.find("<", word_start)
                word = line[word_start:word_end]
                if "no_space_after=\'1\'" not in line:
                    word += ' '
                paragraph.append(word)
            elif line.startswith('</s'):  # end of sentence
                sentences += 1
                # check if paragraph is long enough
                if sentences >= paragraph_size:
                    yield ''.join(paragraph)
                    paragraph = []
                    sentences = 0
        if paragraph:
            yield ''.join(paragraph)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print('Add filename in argument')
        exit()
    file_name = sys.argv[1]
    paragraphs = 250
    batch_size = 8

    count = 0
    for batch in read_czeng(file_name, paragraphs, batch_size):
        for b in batch:
            print('id: ', count)
            print(b)
            count += 1

        pass

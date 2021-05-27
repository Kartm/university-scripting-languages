import math
import re
import matplotlib.pyplot as plt
import numpy
import requests
from matplotlib.figure import Figure
from PIL import Image

def read_file(path: str):
    with open(path) as f:
        content = f.read()
        return content


def parse_book(plain_text: str):
    title = re.search(r'Title: (?P<title>.*)', plain_text).group('title')
    author = re.search(r'Author: (?P<author>.*)', plain_text).group('author')
    chapter_lines = plain_text.split("\n")[870:1166]

    return title, author, chapter_lines


def get_paragraphs_from_lines(chapter_lines):
    paragraphs = list()
    current_paragraph = ''
    for line in chapter_lines:
        stripped_line = line.strip()

        current_paragraph += ' ' + stripped_line if stripped_line else ''
        # print(current_paragraph)
        if stripped_line == '' and current_paragraph != '':
            paragraphs.append(current_paragraph)
            current_paragraph = ''

    return paragraphs


def get_paragraph_plot(paragraphs) -> Figure:
    def round_to_10(x):
        return int(math.ceil(x / 10.0)) * 10

    paragraphs_word_count = [round_to_10(len(p.split())) for p in paragraphs]
    print(f'Sorted paragraph count: {sorted(paragraphs_word_count)}')
    duplicate_count = {e: paragraphs_word_count.count(e) for e in paragraphs_word_count}
    print(f'Duplicate count: {duplicate_count}')

    plt.hist(paragraphs_word_count, bins=numpy.arange(0, 530, 10))
    plt.xlabel('No. of words')
    plt.ylabel('No. of paragraphs')
    plt.title('Paragraph word count distribution')
    plt.show()

    fig = plt.figure(figsize=(4, 5))
    print(fig)
    plt.close()

    # todo pass these stats to word document

    return fig


def download_image() -> Image:
    url = 'https://www.gutenberg.org/files/52466/52466-h/images/i_005.jpg'
    original_image = Image.open(requests.get(url, stream=True).raw)
    original_image = original_image.convert("RGB")

    smaller_edge = min(original_image.width, original_image.height)
    square_image = original_image.crop((0, 0, smaller_edge, smaller_edge))

    resized_image = square_image.resize((smaller_edge * 2, smaller_edge * 2))

    return resized_image


def load_local_image() -> Image:
    original_image = Image.open("./dinosaur.png")

    black_and_white_image = original_image.convert('LA')

    rotated_image = black_and_white_image.rotate(-25)

    return rotated_image


def combine_pictures(bottom_image, top_image):
    combined_picture = bottom_image.copy()
    combined_picture.paste(top_image, box=(100, 300), mask=top_image.convert("RGBA"))

    return combined_picture


def make_word_document(title, author, picture, paragraph_plot):
    # todo title page
    # todo chart page
    pass


def run():
    title, author, chapter_lines = parse_book(read_file("./52466-0.txt"))
    paragraph_plot = get_paragraph_plot(get_paragraphs_from_lines(chapter_lines))
    picture = combine_pictures(download_image(), load_local_image())
    make_word_document(title, author, picture, paragraph_plot)


if __name__ == "__main__":
    run()

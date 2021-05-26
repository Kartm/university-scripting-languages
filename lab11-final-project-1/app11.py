import re


def read_file(path: str):
    with open(path) as f:
        content = f.read()
        return content


def parse_book(plain_text: str):
    title = re.search(r'Title: (?P<title>.*)', plain_text).group('title')
    author = re.search(r'Author: (?P<author>.*)', plain_text).group('author')
    chapter_lines = plain_text.split("\n")[870:1166]

    return title, author, chapter_lines


def get_paragraph_plot(chapter_lines):
    # todo count words
    # todo create a plot
    pass


def download_image():
    # todo download image
    # book cover https://www.gutenberg.org/files/52466/52466-h/images/i_005.jpg
    # todo crop and resize
    pass


def load_local_image():
    # todo load from disk
    pass


def combine_pictures(bottom_image, top_image):
    # todo rotate top image and paste over bottom
    pass


def make_word_document():
    # todo title page
    # todo chart page
    pass


def run():
    title,author,chapter_lines = parse_book(read_file("./52466-0.txt"))
    paragraph_plot = get_paragraph_plot(chapter_lines)
    picture = combine_pictures(download_image(), load_local_image())
    make_word_document()


if __name__ == "__main__":
    run()

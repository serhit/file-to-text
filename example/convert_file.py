import argparse
import io
from file_to_text import ConverterClient


def main():
    parser = argparse.ArgumentParser(
        description='Convert given file into the plain text using FileToTextService'
    )

    parser.add_argument('in_file', type=str, help="Input file to be converted (pdf, rft, doc, docx, xlsx, etc)")
    parser.add_argument('out_file', type=str, help="Output file. Extracted text will be stored there")

    args = parser.parse_args()

    client = ConverterClient('<url to your service>', '<username>', '<password>')
    text = client.convert(filepath=args.in_file)

    with io.open(args.out_file, "w+", encoding='utf-8') as file:
        file.write(text)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Diego Minguzzi 2025
#
import argparse
import pypdf
import os

#---------------------------------------------------------------------------------------------------
def readPdfAsText( filepath: str ) -> str:
    """ Read the content of all the pages in the PDF file as text.
        Raises an exception if the file is not a valid file.
    """
    if not os.path.isfile(filepath):
        raise ValueError(f'The file {filepath} does not exist.')

    reader = pypdf.PdfReader(filepath)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()  # This preserves newlines and whitespaces by default
        if page_text:  # Only add if text is not None
            text += page_text

    return text

#---------------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Process a PDF file.")

    parser.add_argument(
        "--pdf-file",
        type=str,
        required=True,
        help="Path to the PDF file (required)"
    )

    args = parser.parse_args()

    # Access the provided value with args.pdf_file
    print(f"The provided PDF file path is: {args.pdf_file}")
    try:
      text= readPdfAsText( args.pdf_file)
      print(text)
    except Exception as exc:
      print(f'Exception:{exc}')


if __name__ == "__main__":
    main()

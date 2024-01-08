#!/usr/bin/python3
"""
Write a script markdown2html.py that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name
Requirements:

If the number of arguments is less than 2:
    print in STDERR Usage: ./markdown2html.py README.md README.html and exit 1
If the Markdown file doesn’t exist:
    print in STDER Missing <filename> and exit 1
Otherwise, print nothing and exit 0
"""
import sys
import os
import re

if __name__ == "__main__":
    def markdown_to_html(markdown_text):
        # Convert headers
        markdown_text = re.sub(r'^(#+)\s*(.*?)\s*$', lambda match:f"<h{len(match.group(1))}>{match.group(2)}</h{len(match.group(1))}>", markdown_text, flags=re.MULTILINE)

        # Convert bold and italic
        markdown_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', markdown_text)
        markdown_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', markdown_text)

        # Convert lists
        markdown_text = re.sub(r'^\*\s*(.*?)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
        markdown_text = re.sub(r'(?<!<li>)\n', '<ul>\n', markdown_text)
        markdown_text += '</ul>'

        return f'{markdown_text}'


    if len(sys.argv) < 3:
        print(f"{sys.argv[0]} README.md README.html", file=sys.stderr)
        sys.exit(1)
    elif not os.path.exists(sys.argv[1]):
        print(f"Missing {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        with open(input_file, mode="r", encoding="UTF-8") as file_md:
            markdown_text = file_md.read()


        html_content = markdown_to_html(markdown_text)

        with open(output_file, 'w') as file:
            file.write(html_content)


        sys.exit(0)

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

if __name__ == "__main__":
    def add_header_tags(toks: list[str]) -> str:
        """ Adds header tags
        """
        # if any tok contains '#' from start - end of index:
        # get hash count and break
        line = " ".join(toks)
        hash_count = 0
        for i, tok in enumerate(toks):
            if tok.startswith("#") and len(tok) == tok.count("#"):
                hash_count = tok.count("#")

            if hash_count in range(1, 7):
                break

        line = line.replace("\n", "")
        if hash_count != 0:
            tag = "#"*hash_count
            line = line.replace(f"{tag} ", f"<h{hash_count}>")
            line += f"</h{hash_count}>\n"

        return line

    if len(sys.argv) != 3:
        print(f"{sys.argv[0]} README.md README.html", file=sys.stderr)
        sys.exit(1)
    elif not os.path.exists(sys.argv[1]):
        print(f"Missing {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)
    else:
        file = sys.argv[1]
        output = sys.argv[2]

        with open(file, mode="r", encoding="UTF-8") as file_md:
            lines = file_md.readlines()

        output_lines: list[str] = []

        # #########-parsing-###########
        for line in lines:
            hash_count = 0
            toks: list[str] = line.split(" ")
            first_tok: str = toks[0]

            line = add_header_tags(toks)

            # if first token is -
            if first_tok == "-":
                line = line.replace("- ", "\n<li>")
                line += "</li>"

            # if first token is *
            if first_tok == "*":
                line = line.replace("* ", "\n<oli>")
                line += "</oli>"

            output_lines.append(line)

        # if list tag exists: add <ul> before
        for i, line in enumerate(output_lines):
            if "<li>" in line:
                output_lines[i] = "<ul>" + line
                break

        # start from end and pick first </li> tag: add </ul> after it
        for i in range(len(output_lines) - 1, -1, -1):
            if "</li>" in output_lines[i]:
                output_lines[i] = output_lines[i] + "\n</ul>\n"
                break

        # if list tag is oli: add <ol> before
        for i, line in enumerate(output_lines):
            if "<oli>" in line:
                output_lines[i] = "<ol>" + line
                break

        # start from end and pick first </oli> tag: add </ol> after it
        for i in range(len(output_lines) - 1, -1, -1):
            if "</oli>" in output_lines[i]:
                output_lines[i] = output_lines[i] + "\n</ol>\n"
                break

        # replace <oli> with <li> || file cleanup
        for i, line in enumerate(output_lines):
            output_lines[i] = output_lines[i].replace("<oli>", "<li>")
            output_lines[i] = output_lines[i].replace("</oli>", "</li>")

        # #########-end-of-parsing-###########

        # write into file
        with open(output, mode="w", encoding="UTF-8") as file_out:
            file_out.writelines(output_lines)

        sys.exit(0)

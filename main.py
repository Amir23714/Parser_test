import asyncio
import time

from TXT_parsing.txt_to_list import parse_txt
from TXT_parsing.validate_url import validate_url
from web_parse import Parser


def main():
    start = time.time()
    urls = parse_txt("Static_files\\domains.txt")
    blocked = parse_txt("Static_files\\block_domains.txt")

    urls = validate_url(urls, blocked)

    parser = Parser(urls)

    asyncio.run(parser.parse())

    print("Parsing successfully finished and took ", (time.time() - start), " seconds")


if __name__ == "__main__":
    main()

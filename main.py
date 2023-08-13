from TXT_parsing.txt_to_list import parse_txt
from TXT_parsing.validate_url import validate_url


def main():
    urls = parse_txt("Static_files\\domains.txt")
    blocked = parse_txt("Static_files\\block_domains.txt")

    urls = validate_url(urls, blocked)

    return urls


# if __name__ == "__main__":
#     main()

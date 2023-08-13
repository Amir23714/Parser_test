import re
import lxml
import csv
import requests
from bs4 import BeautifulSoup as bs
import logging


class Parser:
    def __init__(self, urls):
        self.urls = urls

        self.email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        self.phone_pattern = r'\+7\d{10}|8\d{10}'
        self.postal_code_pattern = r'\b\d{6}\b'
        self.inn_pattern = r'\b\d{10}\b'
        self.ogrn_pattern = r'\b\d{13}\b'

        self.csv_path = "Results\\result.csv"
        self.field_names = ["url", "title", "description", "emails", "phones", "postal_codes", "inns", "ogrns"]

    def init_csv(self):
        with open(self.csv_path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            writer.writerow(
                self.field_names
            )

    def fill_csv(self, url: str, title: str, description: str, emails: str, phones: str, postal_codes: str, inns: str,
                 ogrns: str):
        with open(self.csv_path, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            writer.writerow(
                (url, title, description, emails, phones, postal_codes, inns, ogrns)
            )

    def parse_page(self, url: str, response: requests.Response, depth: int):
        if depth == 1:
            soup = bs(response.content, 'lxml')

            title = soup.find('title').string
            description = soup.find("meta", attrs={"name": "description"})["content"]

            # Is used to find elements in html code by using patterns
            text_contents = soup.find_all(string=True)

            emails = []
            phones = []
            postal_codes = []
            inns = []
            ogrns = []
            for content in text_contents:

                emails_temp = re.findall(self.email_pattern, content)
                phones_temp = re.findall(self.phone_pattern, content)
                postal_codes_temp = re.findall(self.postal_code_pattern, content)
                inn_temp = re.findall(self.inn_pattern, content)
                ogrn_temp = re.findall(self.ogrn_pattern, content)

                if emails_temp:
                    alredy_used = []
                    for email in emails_temp:
                        if email not in alredy_used:
                            emails.append(email)
                            alredy_used.append(email)
                if phones_temp:
                    alredy_used = []
                    for phone in phones_temp:
                        if phone not in alredy_used:
                            phones.append(phone)
                            alredy_used.append(phone)
                if postal_codes:
                    alredy_used = []
                    for code in postal_codes_temp:
                        if code not in alredy_used:
                            postal_codes.append(code)
                            alredy_used.append(code)
                if inn_temp:
                    alredy_used = []
                    for inn in inn_temp:
                        if inn not in alredy_used:
                            inns.append(inn)
                            alredy_used.append(inn)
                if ogrn_temp:
                    alredy_used = []
                    for ogrn in ogrn_temp:
                        if ogrn not in alredy_used:
                            ogrns.append(ogrn)
                            alredy_used.append(ogrn)

            emails = "\n".join(emails)
            phones = "\n".join(phones)
            postal_codes = "\n".join(postal_codes)
            inns = "\n".join(inns)
            ogrns = "\n".join(ogrns)

            if emails == "":
                emails = "н/д"
            if phones == "":
                phones = "н/д"
            if postal_codes == "":
                postal_codes = "н/д"
            if inns == "":
                inns = "н/д"
            if ogrns == '':
                ogrns = "н/д"

            self.fill_csv(url, title, description, emails, phones, postal_codes, inns, ogrns)

        elif depth == 0:
            soup = bs(response.content, 'lxml')

            title = soup.find('title').string
            description = soup.find("meta", attrs={"name": "description"})["content"]

            # Is used to find elements in html code by using patterns
            text_contents = soup.find_all(string=True)

            emails = []
            phones = []
            postal_codes = []
            inns = []
            ogrns = []
            for content in text_contents:

                emails_temp = re.findall(self.email_pattern, content)
                phones_temp = re.findall(self.phone_pattern, content)
                postal_codes_temp = re.findall(self.postal_code_pattern, content)
                inn_temp = re.findall(self.inn_pattern, content)
                ogrn_temp = re.findall(self.ogrn_pattern, content)

                if emails_temp:
                    alredy_used = []
                    for email in emails_temp:
                        if email not in alredy_used:
                            emails.append(email)
                            alredy_used.append(email)
                if phones_temp:
                    alredy_used = []
                    for phone in phones_temp:
                        if phone not in alredy_used:
                            phones.append(phone)
                            alredy_used.append(phone)
                if postal_codes:
                    alredy_used = []
                    for code in postal_codes_temp:
                        if code not in alredy_used:
                            postal_codes.append(code)
                            alredy_used.append(code)
                if inn_temp:
                    alredy_used = []
                    for inn in inn_temp:
                        if inn not in alredy_used:
                            inns.append(inn)
                            alredy_used.append(inn)
                if ogrn_temp:
                    alredy_used = []
                    for ogrn in ogrn_temp:
                        if ogrn not in alredy_used:
                            ogrns.append(ogrn)
                            alredy_used.append(ogrn)

            emails = "\n".join(emails)
            phones = "\n".join(phones)
            postal_codes = "\n".join(postal_codes)
            inns = "\n".join(inns)
            ogrns = "\n".join(ogrns)

            if emails == "":
                emails = "н/д"
            if phones == "":
                phones = "н/д"
            if postal_codes == "":
                postal_codes = "н/д"
            if inns == "":
                inns = "н/д"
            if ogrns == '':
                ogrns = "н/д"

            self.fill_csv(url, title, description, emails, phones, postal_codes, inns, ogrns)

            # Doing in-depth searching
            search_texts = ["Контакты", "Contacts"]
            list_items = soup.find_all("a", string=search_texts)
            hrefs = []

            for item in list_items:
                try:
                    link = item["href"]

                    if link.startswith(("http:", "https:")):
                        hrefs.append(link)
                    else:
                        link = url + link
                        hrefs.append(link)

                except Exception:
                    continue

            # Этот массив используется для хэндла тех случаев, когда одна и та же ссылка присутствует на страницу 2 и
            # более раз. Это позволяет избегать повторных запросов к ней, а также дубликатов в .csv файле
            already_visited = []
            for link in hrefs:
                if link not in already_visited:
                    try:
                        response = requests.get(f"https://{link}", verify=False)

                        if response.status_code == 200 or response.status_code == 201:
                            self.parse_page(link, response, 1)

                        already_visited.append(link)

                    except Exception as e:
                        logging.basicConfig(filename='Results\\parser.log', level=logging.ERROR,
                                            format='%(asctime)s - %(levelname)s - %(message)s')
                        logging.error(f"Parsing error\n url : {url}\ndetails : {e}")

    def parse(self):
        logging.basicConfig(filename='Results\\parser.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.init_csv()
        for url in self.urls:
            # If url is broken, access is forbidden or anything else happens, code skips this url and writes it to
            # the error_logs
            try:
                response = requests.get(f"https://{url}", verify=False)

                if response.status_code == 200 or response.status_code == 201:
                    self.parse_page(url, response, 0)

            except Exception as e:
                logging.error(f"Parsing error\n url : {url}\ndetails : {e}")

            # TODO добавить таймаут в 3 секунды

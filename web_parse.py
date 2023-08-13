import re
import lxml
import csv
import requests
from bs4 import BeautifulSoup as bs
from main import main
import logging


urls = main()


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
        with open(self.csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            writer.writerow(
                self.field_names
            )

    def fill_csv(self, url: str, title :str, description : str ,emails: str, phones: str, postal_codes: str, inns: str, ogrns: str):

        with open(self.csv_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            writer.writerow(
                (url,title, description, emails, phones, postal_codes, inns, ogrns)
            )

    def parse_page(self, url, response):

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
                for email in emails_temp:
                    emails.append(email)
            if phones_temp:
                for phone in phones_temp:
                    phones.append(phone)
            if postal_codes:
                for code in postal_codes_temp:
                    postal_codes.append(code)
            if inn_temp:
                for inn in inn_temp:
                    inns.append(inn)
            if ogrn_temp:
                for ogrn in ogrn_temp:
                    ogrns.append(ogrn)

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

    def parse(self):
        logging.basicConfig(filename='Results\\parser.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.init_csv()
        for url in urls:
            # If url is broken, access is forbidden or anything else happens, code skips this url and writes it to the error_logs
            try:
                response = requests.get(f"https://{url}", verify=False)

                if response.status_code == 200 or response.status_code == 201:

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
                            for email in emails_temp:
                                emails.append(email)
                        if phones_temp:
                            for phone in phones_temp:
                                phones.append(phone)
                        if postal_codes:
                            for code in postal_codes_temp:
                                postal_codes.append(code)
                        if inn_temp:
                            for inn in inn_temp:
                                inns.append(inn)
                        if ogrn_temp:
                            for ogrn in ogrn_temp:
                                ogrns.append(ogrn)

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

            except Exception as e:
                logging.error(f"Parsing error\n url : {url}\ndetails : {e}")

            #TODO добавить таймаут в 3 секунды


par = Parser(urls)
par.parse()

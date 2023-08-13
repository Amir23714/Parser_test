import asyncio
import re
import time

from tqdm import tqdm
import aiohttp
import lxml
import csv
from bs4 import BeautifulSoup as bs
import logging

import aiofiles



class Parser:
    """A class for parsing data from websites

    parser = Parser(["BOOKING-DUBROVKA.RU"])
    asyncio.run(parser.parse())

    Saves data by the path Results/result.csv
    Logs errors by the path Results/parser.log
    """

    def __init__(self, urls):
        self.urls = urls

        self.email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        self.phone_pattern = r'\+7\d{10}|8\d{10}'
        self.postal_code_pattern = r'\b\d{6}\b'
        self.inn_pattern = r'\b\d{10}\b'
        self.ogrn_pattern = r'\b\d{13}\b'

        self.csv_path = "Results\\result.csv"
        # Field names for header columns of .csv file
        self.field_names = ["url", "title", "description", "emails", "phones", "postal_codes", "inns", "ogrns"]

    async def init_csv(self):
        """Initializes result.csv file"""
        async with aiofiles.open(self.csv_path, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            await writer.writerow(
                self.field_names
            )

    async def fill_csv(self, url: str, title: str, description: str, emails: str, phones: str, postal_codes: str, inns: str,
                 ogrns: str):
        """Appends data to result.csv file"""
        async with aiofiles.open(self.csv_path, 'a', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            await writer.writerow(
                (url, title, description, emails, phones, postal_codes, inns, ogrns)
            )

    async def parse_page(self, url: str, response, depth: int, session):
        """A function for parsing html pages.
        The depth variable is responsible for the depth of the search relative to the start page.

        The parser goes deep to one level if it finds a link to a contact page on the home page.

        """
        if depth == 1:
            soup = bs(await response.text(), 'lxml')

            # Title finding and validating
            title = soup.find('title')
            if title:
                title = title.string
            else:
                title = "н/д"

            # Description finding and validating
            description = soup.find("meta", attrs={"name": "description"})

            if description:
                description = description["content"]
            else:
                description = "н/д"

            # Is used to find elements in html code by using patterns
            text_contents = soup.find_all(string=True)

            # Variables for storage important data to be written to .csv
            emails = []
            phones = []
            postal_codes = []
            inns = []
            ogrns = []

            # Variables for validating values already written to the .csv file
            alredy_used_emails = []
            alredy_used_phones = []
            alredy_used_codes = []
            alredy_used_inns = []
            alredy_used_ogrns = []

            for content in text_contents:

                emails_temp = re.findall(self.email_pattern, content)
                phones_temp = re.findall(self.phone_pattern, content)
                postal_codes_temp = re.findall(self.postal_code_pattern, content)
                inn_temp = re.findall(self.inn_pattern, content)
                ogrn_temp = re.findall(self.ogrn_pattern, content)

                if emails_temp:
                    for email in emails_temp:
                        if email not in alredy_used_emails:
                            emails.append(email)
                            alredy_used_emails.append(email)
                if phones_temp:
                    for phone in phones_temp:
                        if phone not in alredy_used_phones:
                            phones.append(phone)
                            alredy_used_phones.append(phone)
                if postal_codes:
                    for code in postal_codes_temp:
                        if code not in alredy_used_codes:
                            postal_codes.append(code)
                            alredy_used_codes.append(code)
                if inn_temp:
                    for inn in inn_temp:
                        if inn not in alredy_used_inns:
                            inns.append(inn)
                            alredy_used_inns.append(inn)
                if ogrn_temp:
                    for ogrn in ogrn_temp:
                        if ogrn not in alredy_used_ogrns:
                            ogrns.append(ogrn)
                            alredy_used_ogrns.append(ogrn)

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

            await  self.fill_csv(url, title, description, emails, phones, postal_codes, inns, ogrns)

        elif depth == 0:
            soup = bs(await response.text(), 'lxml')

            logging.basicConfig(filename='Results\\parser.log', level=logging.ERROR,
                                format='%(asctime)s - %(levelname)s - %(message)s')

            # Title finding and validating
            title = soup.find('title')
            if title:
                title = title.string
            else:
                title = "н/д"

            # Description finding and validating
            description = soup.find("meta", attrs={"name": "description"})

            if description:
                description = description["content"]
            else:
                description = "н/д"

            # Is used to find elements in html code by using patterns
            text_contents = soup.find_all(string=True)

            # Variables for storage important data to be written to .csv
            emails = []
            phones = []
            postal_codes = []
            inns = []
            ogrns = []

            # Variables for validating values already written to the .csv file
            alredy_used_emails = []
            alredy_used_phones = []
            alredy_used_codes = []
            alredy_used_inns = []
            alredy_used_ogrns = []

            for content in text_contents:

                emails_temp = re.findall(self.email_pattern, content)
                phones_temp = re.findall(self.phone_pattern, content)
                postal_codes_temp = re.findall(self.postal_code_pattern, content)
                inn_temp = re.findall(self.inn_pattern, content)
                ogrn_temp = re.findall(self.ogrn_pattern, content)

                if emails_temp:
                    for email in emails_temp:
                        if email not in alredy_used_emails:
                            emails.append(email)
                            alredy_used_emails.append(email)
                if phones_temp:
                    for phone in phones_temp:
                        if phone not in alredy_used_phones:
                            phones.append(phone)
                            alredy_used_phones.append(phone)
                if postal_codes:
                    for code in postal_codes_temp:
                        if code not in alredy_used_codes:
                            postal_codes.append(code)
                            alredy_used_codes.append(code)
                if inn_temp:
                    for inn in inn_temp:
                        if inn not in alredy_used_inns:
                            inns.append(inn)
                            alredy_used_inns.append(inn)
                if ogrn_temp:
                    for ogrn in ogrn_temp:
                        if ogrn not in alredy_used_ogrns:
                            ogrns.append(ogrn)
                            alredy_used_ogrns.append(ogrn)

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

            await self.fill_csv(url, title, description, emails, phones, postal_codes, inns, ogrns)

            # Doing in-depth searching
            search_texts = ["Контакты", "Contacts"]
            list_items = soup.find_all("a", string=search_texts)
            hrefs = []

            # Not all sites return a valid URL, so we supplement them to valid ones
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

            # This array is used to handle those cases when the same link is present on page 2 and
            # more times. This allows you to avoid repeated requests to it, as well as duplicates in the .csv file
            already_visited = []
            tasks = []
            for link in hrefs:
                if link not in already_visited:
                    try:
                        # start = time.time()
                        response = await session.get(f"https://{link}", verify_ssl=False)
                        # print(f"response for {link} took {time.time() - start} seconds")
                        if response.status == 200 or response.status == 201:
                            task = asyncio.create_task(self.parse_page(link, response, 1, session))
                            tasks.append(task)

                        already_visited.append(link)

                    except Exception as e:
                        logging.error(f"Parsing error\n url : {url}\ndetails : {e}")
            try:
                # Running collected tasks to search deeper into 1 level using asyncio.gather
                await asyncio.gather(*tasks)
            except Exception as e:
                logging.error(f"Parsing error\n url : {url}\ndetails : {e}")

    async def parse(self):
        """
    This method initiates the parsing process for the given list of URLs.
    """
        # Configure logging for error handling
        logging.basicConfig(filename='Results\\parser.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Initialize the CSV file for storing results
        await self.init_csv()

        tasks = []

        # Create an aiohttp ClientSession for making asynchronous HTTP requests
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for url in tqdm(self.urls):
                # If url is broken, access is forbidden or anything else happens, code skips this url and writes it to
                # the error_logs
                try:
                    # start = time.time()
                    response = await session.get(f"https://{url}", verify_ssl=False)
                    # print(f"response for {url} took {time.time()-start} seconds")
                    # Check if the response status indicates success (200 or 201)
                    if response.status == 200 or response.status == 201:
                        task = asyncio.create_task(self.parse_page(url, response, 0, session))
                        tasks.append(task)

                except Exception as e:
                    # Log any exceptions that occur during parsing
                    logging.error(f"Parsing error\n url : {url}\ndetails : {e}")

            try:
                # Gather and execute all parsing tasks, handling exceptions if they occur
                await asyncio.gather(*tasks)
            except Exception as e:
                # Log any exceptions that occur during parsing
                logging.error(f"Parsing error\n url : {url}\ndetails : {e}")

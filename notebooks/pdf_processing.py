import pdfplumber
import re


class PDFHandler:
    def __init__(self, filepath):
        self.pdf = pdfplumber.open(filepath)
        self.date = []
        self.location = []
        self.title = filepath.parts[-1].split(".")[0]

    def print_info(self):
        print('Title:', self.title)
        print("Number of pages:", len(self.pdf.pages))
        print("Date:", self.get_date())
        print("Location:", self.get_location())

    def original_page(self, page_number):
        return self.pdf.pages[page_number].extract_text()

    def extract_speech(self, pat):
        full_text = ""

        for i in range(len(self.pdf.pages)):
            text = self.pdf.pages[i].extract_text()

            search = re.search(pat, text)

            if i == 0:
                self.date = [search.group("day").strip(), search.group("mon").strip(), search.group("year").strip()]
                self.location = [search.group("location_small").strip(), search.group("location_big").strip()]

            full_text += search.group("content") + " "

        return full_text.strip()

    @staticmethod
    def replace(text, old, new):
        for i in range(len(old)):
            pat = re.compile(old[i])
            text = pat.sub(new[i], text)
        return text

    def get_date(self):
        return self.date.copy()

    def get_location(self):
        return self.location.copy()

import pdfplumber
import re
import unicodedata


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
            # \xa0 and a space look the same but have different encoding
            # text = text.replace(u'\xa0', u' ')
            # characters that look the same but have different encodings are normalized
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

            search = re.search(pat, text)

            if i == 0:
                day = search.group("day")
                mon = search.group("mon")
                year = search.group("year")
                loc = search.group("location")

                if day is not None and mon is not None and year is not None:
                    self.date = [day.strip(), mon.strip(), year.strip()]

                if loc is not None:
                    self.location = [loc.strip()]

            full_text += search.group("content") + " "

        return full_text.strip()

    @staticmethod
    def replace(text, old, new):
        for i in range(len(old)):
            pat = re.compile(old[i])
            text = pat.sub(new[i], text)
        return text

    def get_date(self):
        if len(self.date) > 0:
            return self.date.copy()
        else:
            return ["unknown_date"]

    def get_location(self):
        if len(self.location) > 0:
            return self.location.copy()
        else:
            return ["unknown_location"]

    @staticmethod
    def multiple_speakers(text):
        pat = re.compile(r"[a-z0-9]+\s*:", re.I)
        all_speakers = pat.findall(text)
        all_speakers = [s.lower() for s in all_speakers]
        print('"Obama:" count:', all_speakers.count('obama:'))
        print('"President:" count:', all_speakers.count('president:'))
        print('"Question:" count:', all_speakers.count('question:'))
        print('"Audience:" count:', all_speakers.count('audience:'))
        print('"Member:" count:', all_speakers.count('member:'))
        return all_speakers

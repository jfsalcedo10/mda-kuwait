import pdfplumber
import re
import regex
import unicodedata


class PDFHandler:
    def __init__(self, filepath):
        self.pdf = pdfplumber.open(filepath)
        self.date = []
        self.location = []
        self.title = filepath.parts[-1].split(".")[0]

    def get_title(self):
        return self.title

    def get_nb_pages(self):
        return len(self.pdf.pages)

    def get_date(self):
        if len(self.date) > 0:
            return self.date.copy()
        else:
            return ["unknown_date"]

    def get_date_str(self):
        if len(self.date) > 0:
            return self.date[0] + " " + self.date[1] + " " + self.date[2]
        else:
            return "unknown_date"

    def get_location(self):
        if len(self.location) > 0:
            return self.location.copy()
        else:
            return ["unknown_location"]

    def get_location_str(self):
        if len(self.location) > 0:
            return self.location[0]
        else:
            return "unknown_location"

    def print_info(self):
        print('Title:', self.get_title())
        print("Number of pages:", self.get_nb_pages())
        print("Date:", self.get_date_str())
        print("Location:", self.get_location_str())

    def original_page(self, page_number):
        return self.pdf.pages[page_number].extract_text()

    def extract_speech(self, pat):
        full_text = ""

        for i in range(len(self.pdf.pages)):
            text = self.pdf.pages[i].extract_text()
            # before normalizing
            text = self.match_replace(text, [r"['’‘`´]"], [r"'"])
            # characters that look the same but have different encodings are normalized
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

            search = regex.search(pat, text)

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

    def full_extract(self, pat, count, rep_old, rep_new, re_old, re_new):
        speech = self.extract_speech(pat)

        counts, speakers = self.multiple_speakers(speech, count)

        clean_speech = self.substring_replace(speech, rep_old, rep_new)
        clean_speech = self.match_replace(clean_speech, re_old, re_new)

        title = self.get_title()
        nb_pages = self.get_nb_pages()
        date = self.get_date_str()
        loc = self.get_location_str()
        highest_count = max(counts.values())

        return title, nb_pages, date, loc, highest_count, clean_speech

    @staticmethod
    def match_replace(text, old, new):
        for i in range(len(old)):
            pat = re.compile(old[i])
            text = pat.sub(new[i], text)
        return text

    @staticmethod
    def substring_replace(text, old, new):
        clean_text = text
        for i in range(len(old)):
            clean_text = clean_text.replace(old[i], new[i])
        return clean_text

    @staticmethod
    def multiple_speakers(text, keys):
        pat = re.compile(r"[a-z0-9]+\s*:", re.I)
        all_speakers = pat.findall(text)
        all_speakers = [s.lower().replace(" ", "") for s in all_speakers]

        counts = dict.fromkeys(keys)
        for s in counts.keys():
            counts[s] = all_speakers.count(s.lower().replace(" ", ""))

        return counts, all_speakers

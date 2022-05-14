import pdfplumber
import re
import regex
import unicodedata


class PDFHandler:
    """
    A class used for extracting the text and additional information out of a pdf file

    The pdf is assumed to be a speech of Barack Obama, retrieved from
    https://www.americanrhetoric.com/barackobamaspeeches.htm

    Attributes
    ----------
    pdf : instance of the pdfplumber.PDF class
        the pdf file to process
    title : str
        the title of the pdf file
    date : str
        the date on which the speech took place
    location : str
        the location where the speech took place

    Methods
    -------
    __init__(self, filepath)
        The constructor of the PDFHandler class
    get_title(self)
        Returns the title of the pdf
    get_nb_pages(self)
        Return the number of pages
    get_date(self)
        Return the date
    get_location(self)
        Returns the location
    print_info(self)
        Prints the title, number of pages, date, and location
    original_page(self, pagenumber)
        Returns the text extracted from the given page number before processing
    extract_speech(self, pat)
        Return the contents of the entire speech, with the contents as defined by the given pattern
    full_extract(self, pat, count, rep_old, rep_new, re_old, re_new)
        Returns a tuple containing all the information of the entire speech, ready to be read into a database
    match_replace(text, old_arr, new_arr)
        Returns the given text for which regular expression patterns have been replaced by the given strings
    substring_replace(text, old_arr, new_arr)
        Returns the given text for which substrings have been replaced by the corresponding strings
    multiple_speakers(text, keys)
        Returns a list of all occurrences of a word followed by a ":" in the text and counts the occurrences in that
        list for the given keys
    """

    date = ""
    location = ""

    def __init__(self, filepath):
        """
        Creates a PDFHandler object

        :param filepath: Filepath of the pdf to process
        :type filepath: pathlib.Path instance
        """
        self.pdf = pdfplumber.open(filepath)
        # the last part of the filepath is filename.pdf
        self.title = filepath.parts[-1].split(".")[0]

    def get_title(self):
        """
        Get the title of the pdf

        :return: Title of the pdf
        :rtype: string
        """
        return self.title

    def get_nb_pages(self):
        """
        Get the number of pages of the pdf

        :return: Number of pages of the pdf
        :rtype: integer
        """
        return len(self.pdf.pages)

    def get_date(self):
        """
        Get the date at which the speech took place

        :return: The date
        :rtype: string
        """
        # if no date was present, the date attribute is an empty string
        if len(self.date) > 0:
            return self.date
        else:
            return "unknown_date"

    def get_location(self):
        """
        Get the location at which the speech took place

        :return: The location
        :rtype: string
        """
        # if no location was present, the location attribute is an empty string
        if len(self.location) > 0:
            return self.location
        else:
            return "unknown_location"

    def print_info(self):
        """
        Prints the title of the pdf, number of pages, date, and location
        """
        print('Title:', self.get_title())
        print("Number of pages:", self.get_nb_pages())
        print("Date:", self.get_date())
        print("Location:", self.get_location())

    def original_page(self, page_number):
        """
        Extracts the text from a page of the pdf, without any additional processing

        :param page_number: The page number of the text to extract
        :type page_number: integer

        :return: The extracted text
        :rtype: string
        """
        return self.pdf.pages[page_number].extract_text()

    def extract_speech(self, pat):
        """
        Extracts the entire speech from the pdf as well as the date and location (if present).

        The contents of the pdf are extracted page by page and concatenated into one string. The given regular
        expression should have named groups "day", "mon", and "year" (for the date), "location", and "content" (for the
        actual text of the speech). Only the text in the content group is returned by the method. If the date and
        location are present, the respective attributes are updated with these values. The date and location, if
        present, are assumed to be on the first page of the pdf.

        :param pat: A compiled regular expression to extract the contents of the pdf
        :type pat: regex.Pattern

        :return: The extracted text from the entire pdf
        :rtype: string
        """

        full_text = ""

        for i, page in enumerate(self.pdf.pages):
            text = page.extract_text()
            # different quotation marks are replaced by "'", otherwise they will be deleted during the normalization
            text = self.match_replace(text, [r"['’‘`´]"], [r"'"])
            # characters that look the same but have different encodings are normalized and only ascii supported
            # characters are kept
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

            search = regex.search(pat, text)

            # the date and location are assumed to be on the first page of the pdf
            if i == 0:
                day = search.group("day")
                mon = search.group("mon")
                year = search.group("year")
                loc = search.group("location")

                # if the date was present, the attribute is updated
                if day is not None and mon is not None and year is not None:
                    self.date = day.strip() + " " + mon.strip() + " " + year.strip()

                # if the location was present, the attribute is updated
                if loc is not None:
                    self.location = loc.strip()

            # the extracted content of the speech is added to that of the previous pages
            full_text += search.group("content") + " "

        # leading and trailing whitespace is stripped
        return full_text.strip()

    def full_extract(self, pat, count, rep_old, rep_new, match_old, match_new):
        """
        Processes the entire pdf and returns the cleaned text as well as additionally extracted information.

        The extract_speech(self, pat) method is used to extract the text of the pdf. The extracted speech is cleaned
        with match_replace(text, match_old, match_new) and substring_replace(text, rep_old, rep_new).
        multiple_speakers(text, count) is used to count the number of occurrences of certain strings, which are used as
        indications that there are multiple speakers. All information is read out as a tuple so it can easily be
        written into a new file as a row.

        :param pat: A compiled regular expression to extract the contents of the pdf
        :type pat: regex.Pattern
        :param count: Strings that indicate the presence of multiple speakers, of which the number of occurrences in
        the text should be counted
        :type count: tuple of strings
        :param rep_old: List of substrings to replace
        :type rep_old: list
        :param rep_new: List of strings to replace with
        :type rep_new: list
        :param match_old: List of regular expressions (as strings) to replace
        :type match_old: list
        :param match_new: List of strings to replace with
        :type match_new: list

        :return: The title of the pdf, number of pages, date, location, highest count for the multiple speakers
        indicators, and the cleaned speech
        :rtype: tuple of strings
        """

        # extract the entire speech
        speech = self.extract_speech(pat)

        # count the multiple speakers indicators
        counts, speakers = self.multiple_speakers(speech, count)

        # clean the extracted speech
        clean_speech = self.substring_replace(speech, rep_old, rep_new)
        clean_speech = self.match_replace(clean_speech, match_old, match_new)

        # get all additional information
        title = self.get_title()
        nb_pages = str(self.get_nb_pages())
        date = self.get_date()
        loc = self.get_location()
        highest_count = str(max(counts.values()))

        return title, nb_pages, date, loc, highest_count, clean_speech

    @staticmethod
    def match_replace(text, old_arr, new_arr):
        """
        Uses regular expressions to replace patterns in the given text.

        :param text: The text to clean
        :type text: string
        :param old_arr: The regular expressions (as strings) to replace
        :type old_arr: list
        :param new_arr: The strings to replace with
        :type new_arr: list

        :return: The cleaned text
        :rtype: string
        """
        for old, new in zip(old_arr, new_arr):
            pat = re.compile(old)
            text = pat.sub(new, text)
        return text

    @staticmethod
    def substring_replace(text, old_arr, new_arr):
        """
        Uses the str.replace function to replace substrings in the given text.

        :param text: The text to clean
        :type text: string
        :param old_arr: The substrings to replace
        :type old_arr: list
        :param new_arr: The strings to replace with
        :type new_arr: list

        :return: The cleaned text
        :rtype: string
        """
        clean_text = text
        for old, new in zip(old_arr, new_arr):
            clean_text = clean_text.replace(old, new)
        return clean_text

    @staticmethod
    def multiple_speakers(text, keys):
        """
        Gives an indication of whether there could be multiple speakers in the given text.

        A list is compiled of all occurrences of the ":" character preceded by a combination of numbers and letters
        (e.g. "question:"), whitespace before the ":" is allowed. The given keys are used to make a dictionary, where
        the values are the number of times the key is present in the previously compiled list. The given keys can be
        chosen such that high dictionary values indicate the presence of multiple speakers (e.g. "Question:", "Obama:",
        "Audience:").

        :param text: The text to process
        :type text: string
        :param keys: Strings that indicate the presence of multiple speakers (not case sensitive)
        :type keys: tuple of strings

        :return: A list of all occurrences of the ":" character preceded by a combination of numbers and letters, and
        a dictionary of the given keys and the number of times they are in the aforementioned list
        :rtype: tuple of a dictionary and list
        """
        pat = re.compile(r'[a-z0-9]+\s*:', re.I)
        all_speakers = pat.findall(text)
        # make everything lower case and remove whitespaces
        all_speakers = [s.lower().replace(' ', '') for s in all_speakers]

        counts = dict.fromkeys(keys)
        for s in counts:
            # make everything lower case and remove whitespaces
            counts[s] = all_speakers.count(s.lower().replace(' ', ''))

        return counts, all_speakers

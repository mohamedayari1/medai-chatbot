"""Docs parser.

Contains parsers for docx, pdf files.

"""
from pathlib import Path
from typing import Dict

from app.parser.file.base_parser import BaseParser
from app.core.settings import settings

import requests

class PDFParser(BaseParser):
    """PDF parser."""

    def _init_parser(self) -> Dict:
        """Init parser."""
        return {}

    def parse_file(self, file: Path, errors: str = "ignore") -> str:
        """Parse file."""
        # if settings.PARSE_PDF_AS_IMAGE:
        #     doc2md_service = "https://llm.arc53.com/doc2md"
        #     # alternatively you can use local vision capable LLM
        #     with open(file, "rb") as file_loaded:
        #         files = {'file': file_loaded}
        #         response = requests.post(doc2md_service, files=files)   
        #         data = response.json()["markdown"] 
        #     return data

        try:
            import PyPDF2
        except ImportError:
            raise ValueError("PyPDF2 is required to read PDF files.")
        text_list = []
        with open(file, "rb") as fp:
            # Create a PDF object
            pdf = PyPDF2.PdfReader(fp)

            # Get the number of pages in the PDF document
            num_pages = len(pdf.pages)

            # Iterate over every page
            for page in range(num_pages):
                # Extract the text from the page
                page_text = pdf.pages[page].extract_text()
                text_list.append(page_text)
        text = "\n".join(text_list)

        return text



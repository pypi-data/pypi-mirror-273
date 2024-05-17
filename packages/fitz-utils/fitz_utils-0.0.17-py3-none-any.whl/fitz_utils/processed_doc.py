from pathlib import Path

import fitz

from .processed_page import ProcessedPage


class ProcessedDoc:
    """Class to provide extra methods to pymupdf doc class"""

    def __init__(self, fname: Path = None, stream: bytes = None) -> None:
        if not fname:
            self.doc = fitz.open(stream=stream)
        else:
            self.doc = fitz.open(str(fname))

    def crop_pdf_bytes(self, from_page: int, to_page: int) -> bytes:
        """
        Crop the PDF document from the specified starting page to the specified ending page and return the cropped document as bytes.

        Args:
        - from_page (int): The starting page number (inclusive) for cropping the document.
        - to_page (int): The ending page number (inclusive) for cropping the document.

        Returns:
        - bytes: The cropped document as bytes.
        """
        page_doc = fitz.open()
        page_doc.insert_pdf(self.doc, from_page=from_page, to_page=to_page)
        page_doc_bytes = page_doc.write()
        page_doc.close()
        return page_doc_bytes

    def __len__(self) -> int:
        return len(self.doc)

    def __getitem__(self, key) -> ProcessedPage:
        return ProcessedPage(self.doc[key])

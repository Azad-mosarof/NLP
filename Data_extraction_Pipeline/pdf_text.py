import pdfplumber

file = "/home/azadm/Desktop/Natural Language Processing Recipes_ Unlocking Text Data with Machine Learning and Deep Learning using Python ( PDFDrive ).pdf"

import pdfplumber
with pdfplumber.open(file) as pdf:
    first_page = pdf.pages[88]
    print(first_page.extract_text())

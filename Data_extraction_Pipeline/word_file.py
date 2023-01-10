# from docx import Document

# #example file -> file_name = "file.docx"

# def extract_data_from_document(file_name):
#     doc = open(file_name,'rb')
#     document = Document(doc)
#     docu = ""
#     for para in document.paragraphs:
#         docu += para.text

#     return docu

s = "My name is azad mosarof.\nI am a student"
s1 = "I am a developer"

print(s.replace('azad', 'raj'))
print(s.find("name"))
print(s.rfind("name"))
print(s.rindex("name"))
print(s.join(s1))
print(s.split())
print(s.splitlines())
print(s.lower())
print(s.upper())
print(s.title())
print(s.strip())   #a copy of s without leading or trailing whitespace


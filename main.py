import PyPDF2, pdfminer, pdf2image
import pdfminer.layout
import pdfminer.high_level
from PIL import Image
import pytesseract
import os

def text_extraction(element):
    line_text=element.get_text() # вытягиваем текст

    line_formats=[] #метаданные текста
    if isinstance(element, pdfminer.layout.LTTextContainer):
        for text_element in element:
            if isinstance(text_element, pdfminer.layout.LTTextLine):
                for character in text_element:
                    if isinstance(character, pdfminer.layout.LTChar):
                        line_formats.append(character.fontname)
                        line_formats.append(character.size)

                        # LTTextContainer, LTTextLine и LTChar как промежуточные контейнера нужны
    format_list_text=list(line_formats)  #set() добавить?

    return (line_text,format_list_text)

"""

pytesseract_scan(Image_path):
    images = pdf2image.convert_from_path(input_file)

    text_image = Image.open(Image_path)

    text_convector= pytesseract.image_to_string(text_image)


    return text_convector
"""
"""def __main__():
    return 0"""


PDF=('text.pdf') #открываем содержимое файла
# exact_path_pdf = os.path.abspath(PDF) путь до файла

PYPDF_file_open= open(PDF,'rb') #читаем файл (бинарник тоже)
PYPDF_read_file= PyPDF2.PdfReader(PYPDF_file_open,password=None, strict=False) # принимает открытый объект pdf

#for нужен для открытия каждой страницы и парсинга данных
for pagenum, page in enumerate(pdfminer.high_level.extract_pages(PDF)):
    print(f'страница {pagenum}')
    pdf= PYPDF_read_file.pages[pagenum]

    # списки нужны для парсинга
    text_line = []
    size_text_line = []

    # Бинарники для if
    #table_extraction_text_flag = False

    #page_table_len = pdf.find_tables()

    #Находим все элементы
    page_elements=[]
    for element in page._objs:
        page_elements.append((element.y1, element))

    page_elements.sort(reverse=True)



    for i in enumerate(pdf):
        #if table_extraction_text_flag==False:
        text_line, size_text_line= text_extraction(element)



        pass
        pass

        if isinstance (element, pdfminer.layout.LTFigure):

            pass
            pass
        if isinstance(element, pdfminer.layout.LTRect):

            pass
            pass

print(text_line,size_text_line)
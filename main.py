import PyPDF2, pdfminer, pdf2image, pdfplumber
import pdfminer.layout
import pdfminer.high_level
from PIL import Image
import pytesseract
import os


#функция для парсинга текста
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



def crop_image(element,pdf_object_page):
    coords_xy_0=[element.x0,element.y0]
    coords_xy_1=[element.x1,element.y1]

    pdf_object_page.mediabox.left=coords_xy_0
    pdf_object_page.mediabox.right=coords_xy_1

    crop_image_pdf_write=PyPDF2.writter()
    crop_image_pdf_write.add_page(pdf_object_page)

    with open('cropped_image.pdf', 'wb') as crop_image_pdf_file:
        crop_image_pdf_write.write(crop_image_pdf_file)

def convert_pdfobject_png(input_pdf):
    images=pdf2image.convert_from_path(input_pdf)
    image=images[0]
    print(image.size)
    print(image.mode)

    image.save('output_file.png',"PNG")



def pytesseract_scan(Image_path):
    images = pdf2image.convert_from_path(Image_path)

    text_image = Image.open(Image_path)

    text_convector= pytesseract.image_to_string(text_image)


    return text_convector


def extract_table(PDF,pagenum,table_num):
    pdf_table=PDF.pdflumber.open(PDF)

    page_table=pdf_table.pages[pagenum]

    table_pars=page_table.extract_table()[table_num]

    return table_pars


def convert_table(table):
    cleaned_now=[]
    table_string=''
    for row in table:

        for item in None:
            cleaned_now.append('')
        else:
            cleaned_now.append(str(item).replace('\n','')).strip()

        table_string+='|'+'|'.join(cleaned_now)+'|\n'

    if table!=None:
        header_table='|'+'|'.join('---')*len(table[0])+'|\n'
        table_string=table_string.split('\n')[0]+'\n'+header_table+'\n'.join(table_string.split('\n')[1:])

    return table_string



"""def __main__():
    return 0"""


PDF=('Doc1.pdf') #открываем содержимое файла
# exact_path_pdf = os.path.abspath(PDF) путь до файла

PYPDF_file_open= open(PDF,'rb') #читаем файл (бинарник тоже)
PYPDF_read_file= PyPDF2.PdfReader(PYPDF_file_open,password=None, strict=False) # принимает открытый объект pdf

#for нужен для открытия каждой страницы и парсинга данных
for pagenum, page in enumerate(pdfminer.high_level.extract_pages(PDF)):
    print(f'страница {pagenum}')
    pdf_object_page= PYPDF_read_file.pages[pagenum]

    # списки нужны для парсинга
    text_line = []
    size_text_line = []

    pdf_lumber_table=pdfplumber.open(PDF)
    page_table=pdf_lumber_table.pages[pagenum]
    tables=page_table.find_tables()

    # Бинарники для if
    #table_extraction_text_flag = False

    #page_table_len = pdf.find_tables()

    #Находим все элементы
    page_elements=[]
    for element in page._objs:
        page_elements.append((element.y1, element))

    page_elements.sort(reverse=True)



    for i in enumerate(pdf_object_page):
        #if table_extraction_text_flag==False:
        if isinstance(pdf_object_page,pdfminer.layout.LTTextContainer):
            text_line, size_text_line= text_extraction(element)

        if isinstance (element, pdfminer.layout.LTFigure):
            peremennaya= crop_image(element,pdf_object_page)
            crop_image('cropped_image.pdf')

            peremennaya=pytesseract_scan('output_file.png')

        if isinstance(element, pdfminer.layout.LTRect):
            crop_box=page.bbox()[1]-tables.bbox()[0]


            table_pars = extract_table()
            table_string=convert_table(table_pars)

            pass
            pass

print(text_line,size_text_line)
from bs4 import BeautifulSoup
from openpyxl import load_workbook

def clear_html_in_excel(file_path, columns=[]):
    """
    clear html code in excel file.
    after clear, the content will be replace back to the cell.
    @param file_path: str, the path of excel file.
    @param columns: list, the columns that need to be clear.
    """

    wb = load_workbook(file_path)
    
    sheet = wb.active
    
    for col in columns:
        for i, cell in enumerate(sheet[col], 1):
            cell.value = clear_html(cell.value)
    
    wb.save(file_path)
    
    pass

def clear_html(html:str):
    """
    clear html code.
    @param html: str, the html code.
    @return: str, the text after clear html code.
    """
    if html is None:
        return html
    html = html.replace(" ", "")
    html = BeautifulSoup(html, 'html.parser').get_text()
    return html
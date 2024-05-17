import openpyxl

def save_to_excel(headers, formatted_data, file_name):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(headers)
    for row in formatted_data:
        worksheet.append(row)
    workbook.save(file_name)
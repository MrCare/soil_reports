'''
Author: Mr.Car
Date: 2024-02-29 18:13:50
'''
def fill_template(sheet, start_position, value_list, horizon=True):
    start_row, start_col = int(start_position[1:]), ord(start_position[0].upper()) - 64 # B4 转为 列标数字
    for each in value_list:
        sheet.cell(row=start_row, column=start_col, value=each)
        if horizon:
            start_col += 1
        else:
            start_row += 1
    return sheet

def fill_title(sheet, title, position="A1"):
    sheet[position] = title 
    return sheet

def fill_value(sheet, value, position):
    sheet[position] = value
    return sheet

def get_sheet(wb, template):
    sheet_name = next(x for x in wb.sheetnames if template in x)
    sheet = wb[sheet_name]
    return sheet

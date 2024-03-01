'''
Author: Mr.Car
Date: 2024-02-29 18:13:50
'''
def fill_template(sheet, start_position, value_list):
    start_row, start_col = int(start_position[1:]), ord(start_position[0].upper()) - 64 # B4 转为 列标数字
    for each in value_list:
        sheet.cell(row=start_row, column=start_col, value=each)
        start_col += 1
    return sheet
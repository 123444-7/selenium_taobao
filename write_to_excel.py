from openpyxl import Workbook


def write_excel(my_list, excel_name, sheet_name):
    """
    将list中的订单信息写入excel
    :param my_list: 包含淘宝订单信息的列表
    :param excel_name: 生成的excel文件名
    :param sheet_name: 写入的excel表名
    :return: None
    """
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    # 写入表头
    ws.append(['订单编号', '订单生成日期', '商品链接', '商品标题', '实付款'])
    goods_list = my_list
    # for循环遍历list并写入表格
    for i in goods_list:
        print(f'正在写入数据{i}')
        order_no = i['order_no']
        order_date = i['order_date']
        product_link = i['product_link']
        product_title = i['product_title']
        disbursements = i['disbursements']
        ws.append([order_no, order_date, product_link, product_title, disbursements])

    # 设定列宽，使得打开excel即可完整呈现出全表内容
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 80
    ws.column_dimensions['D'].width = 75
    ws.column_dimensions['E'].width = 10
    wb.save(f"{excel_name}.xlsx")
    print(f"写入完成，共写入了{len(goods_list)}条数据。")

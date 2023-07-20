import get_list
import write_to_excel

goods_list = get_list.get_list()  # 调用get_list方法，爬取订单信息
write_to_excel.write_excel(goods_list, "taobao_data", "淘宝订单信息")  # 将订单信息写入excel

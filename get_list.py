from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_list():
    """
    获取淘宝所有订单信息并转成list输出
    :return: 包含淘宝订单信息的list
    """
    # 配置chrome 防止出现滑块验证
    options = webdriver.ChromeOptions()  # 配置chrome 防止出现滑块验证
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--disable-blink-features=AutomationControlled')
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()  # 窗口最大化，防止元素重叠无法点击

    driver.get("http://www.taobao.com/")

    # 获取登录按钮并点击
    login_button1 = driver.find_element(By.XPATH,
                                        '/html/body/div[3]/div[2]/div[2]/div[2]/div[5]/div/div[2]/div[1]/a[1]')
    login_button1.click()

    # 点击登录按钮，会跳转至登录页面需要重定位活跃窗口
    driver.switch_to.window(driver.window_handles[-1])
    driver.implicitly_wait(15)  # 等待网页加载

    # 获取用户名、密码input以及登录button
    username_input = driver.find_element(By.XPATH,
                                         '/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/form/div[1]/div[2]/input')
    password_input = driver.find_element(By.XPATH,
                                         '/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/form/div[2]/div[2]/input')
    login_button2 = driver.find_element(By.XPATH,
                                        '/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/form/div[4]/button')

    # 输入用户名密码并单击登录按钮
    username_input.send_keys('your_username')
    sleep(1)
    password_input.send_keys('your_pwd')
    sleep(1)
    login_button2.click()

    # 登录后会进行用户验证，需要手机淘宝点击确认登陆
    input("请进行手机验证，验证通过后按回车继续脚本")

    # 进入我的淘宝页面
    my_tb = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/ul[2]/li[2]/div[1]/a')
    my_tb.click()

    # 进入订单页面
    driver.implicitly_wait(15)
    goods_form_page = driver.find_element(By.XPATH, '//*[@id="bought"]')
    goods_form_page.click()

    driver.switch_to.window(driver.window_handles[-1])
    driver.implicitly_wait(15)

    # 定义订单列表
    goods_list = []

    # 翻页操作，非尾页时，循环执行
    while True:
        goods_form = driver.find_elements(By.CLASS_NAME, 'js-order-container')  # 获取订单信息父元素
        for i in goods_form:
            dist = {}
            dist['order_no'] = i.find_element(By.XPATH, './div/table/tbody[1]/tr/td[1]/span/span[3]').text
            dist['order_date'] = i.find_element(By.XPATH, './div/table/tbody[1]/tr/td[1]/label/span[2]').text
            dist['product_link'] = i.find_element(By.XPATH,
                                                  './div/table/tbody[2]/tr[1]/td[1]/div/div[2]/p[1]/a[1]'
                                                  ).get_attribute(
                "href")
            dist['product_title'] = i.find_element(By.XPATH,
                                                   './div/table/tbody[2]/tr[1]/td[1]/div/div[2]/p[1]/a[1]/span[2]').text
            dist['disbursements'] = i.find_element(By.XPATH,
                                                   './div/table/tbody[2]/tr[1]/td[5]/div/div[1]/p/strong/span[2]').text
            goods_list.append(dist)
        next_page = driver.find_element(By.CLASS_NAME, 'pagination-next')  # 获取下一页按钮元素

        # 判断是否尾页，尾页的下一页button，class类为“pagination-disabled pagination-next”，非尾页的下一页button，class类为“pagination-next”
        if next_page.get_attribute("class") != 'pagination-next':  # 若不为“pagination-next”则尾页，跳出死循环
            break
        else:  # 否则非尾页，继续循环爬取

            # 点击下一页按钮
            driver.find_element(By.XPATH,
                                '/html/body/div[2]/div/div[1]/div[1]/div[3]/div/div[54]/div[2]/ul/li[6]/a').click()
            sleep(3)

    print("页面抓取完毕")
    driver.close()
    return goods_list

import time

import allure
import pytest
from selenium.webdriver.common.by import By

import mes
from selenium import webdriver


class TestCeshien:
    # 前置 所有用例执行之前执行一次
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)

    # 每个用例执行前会执行一次,访问ceshiren网址
    def setup(self):
        self.driver.get(mes.MesID.url)
        self.driver.maximize_window()
        # 点击搜索按钮
        self.driver.find_element(By.ID, mes.MesID.search_button).click()
        # 点击高级搜索按钮
        self.driver.find_element(By.CLASS_NAME, mes.MesID.advanced_search_class).click()

    # 所有用例执行后执行一次
    def teardown_class(self):
        self.driver.quit()

    # 正向测试用例
    @pytest.mark.parametrize(
        "search_mes",
        [
            "selenium",
            "appium"
        ]
    )
    def test_search(self, search_mes):
        """
        测试步骤
        1、打开测试网站
        2、点击搜索按钮
        3、点击高级搜索按钮
        4、输入搜索内容
        5、点击搜索
        6、断言信息是否正确
        """
        # 输入搜索内容search_mes
        self.driver.find_element(By.XPATH, mes.MesID.search_input).send_keys(search_mes)
        # 点击搜索按钮
        self.driver.find_element(By.XPATH, mes.MesID.button).click()
        # 获取搜索结果的内容标题
        res_item = self.driver.find_element(By.CSS_SELECTOR, ".topic-title")
        # 断言搜索内容是否正确
        assert search_mes in res_item.text.lower()

    def test_search_Withkind(self):
        """
        测试搜索内容选择文章类别
        测试步骤
        1、打开测试网站
        2、点击搜索按钮
        3、点击高级搜索按钮
        4、输入搜索内容
        5、选择类别标签
        6、点击搜索
        7、断言信息是否正确
        """
        # 输入搜索内容appium
        self.driver.find_element(By.XPATH, mes.MesID.search_input).send_keys("appium")
        # 点击搜索类别下拉框
        self.driver.find_element(By.ID, "search-type").click()
        # 点击第二个选项
        self.driver.find_element(By.XPATH, """//*[@class="select-kit-collection"]/li[2]""").click()
        # 点击搜索按钮
        self.driver.find_element(By.XPATH, mes.MesID.button).click()
        # 获取搜索结果的类别
        res_head = self.driver.find_element(By.CLASS_NAME, "tag-heading")
        # 获取搜索结果的内容标题
        res_item = self.driver.find_element(By.CSS_SELECTOR, ".tag-items")
        # 断言类别与内容是否正确
        assert "标签" == res_head.text
        assert "appium" in res_item.text.lower()

    # 搜索内容为空测试用例
    def test_searchnull(self):
        """
        搜索内容为空时
        测试步骤
        1、打开测试网站
        2、点击搜索按钮
        3、点击高级搜索按钮
        4、不输入内容，点击搜索按钮
        7、断言信息是否正确
        """
        # 点击搜索按钮
        self.driver.find_element(By.XPATH, mes.MesID.button).click()
        # 获取搜索结果
        res = self.driver.find_element(By.CLASS_NAME, "search-notice")
        # 截图操作
        self.driver.save_screenshot("search_null.png")
        # 塞入报告(ps：执行时要用命令行的方式执行，命令：pytest test_ceshiern.py(用例文件名) --alluredir=./report(指定报告路径)
        # 查看报告 allure serve 报告名称report
        allure.attach.file("search_null.png", name="搜索内容为空", attachment_type=allure.attachment_type.PNG)
        # 断言类别与内容是否正确
        assert "您的搜索词过短。" == res.text

    @pytest.mark.parametrize(
        "search_message",
        [
            "@#$",
            "012345678901234567890123456789012345678901234567890123456789"
        ]
    )
    # 搜索内容不存在（搜索内容过长）测试用例
    def test_search_not(self, search_message):
        """
        搜索内容不存在时
        测试步骤
        1、打开测试网站
        2、点击搜索按钮
        3、点击高级搜索按钮
        4、输入内容，点击搜索按钮
        7、断言信息是否正确
        """
        # 输入搜索内容
        self.driver.find_element(By.XPATH, mes.MesID.search_input).send_keys(search_message)
        # 点击搜索按钮
        self.driver.find_element(By.XPATH, mes.MesID.button).click()
        # 获取搜索结果
        res = self.driver.find_element(By.CLASS_NAME, "search-results")
        print(res.text)
        # 截图操作
        self.driver.save_screenshot("search_notexit.png")
        # 塞入报告(ps：执行时要用命令行的方式执行，命令：pytest test_ceshiern.py(用例文件名) --alluredir=./report(指定报告路径)
        # 查看报告 allure serve 报告名称report
        allure.attach.file("search_notexit.png", name="搜索内容不存在", attachment_type=allure.attachment_type.PNG)
        # 断言类别与内容是否正确
        assert "找不到结果。" in res.text


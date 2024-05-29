import logging

import scrapy
from selenium.webdriver.common.by import By
from webSpider.items import EmployItem
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
import time
from lxml import etree
from selenium.webdriver.support.ui import Select


class ExperienceSpider(scrapy.Spider):
    name = "espider"
    allowed_domains = ["nowcoder.com"]

    # start_urls = ["https://www.nowcoder.com/feed/main/detail/3364c82e4c3b4eac9dfca2ee92100b06"]

    def __init__(self):
        """
        包含链接的页面是用Ajax动态渲染的，先使用selenium模拟浏览器爬取
        """
        super(ExperienceSpider, self).__init__()
        self.urls = {}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        # driver = webdriver.Chrome(options=chrome_options)
        driver = webdriver.Chrome()
        driver.get("https://www.nowcoder.com/jobs/recommend/campus")

        # 点击全部职位
        driver.find_element(By.XPATH, "//div[@data-v-3683ca40]").click()
        # element = driver.find_element(By.XPATH, "//div[@data-v-3683ca40]")
        # driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        logging.info("Clicked All Jobs")

        # 选择一级职位
        category_elements = driver.find_elements(By.XPATH,
                                                 "//div[@class='el-scrollbar nowcoder-custom el-cascader-menu'][1]//li")
        category = {c.text: c for c in category_elements if c.text != ""}
        logging.info("Find job categories: " + category.keys().__str__())

        # 循环点击一级职位
        # for k, v in category.items():
        for k, v in {"软件开发": category["软件开发"]}.items():
            v.click()
            # driver.execute_script("arguments[0].click();", v)
            time.sleep(1)
            logging.info("Clicked button " + k)

            # 选择二级职位
            sub_category_elements = driver.find_elements(By.XPATH,
                                                         "//div[@class='el-scrollbar nowcoder-custom el-cascader-menu'][2]//li")
            sub_category = {c.text: c for c in sub_category_elements if c.text != ""}
            logging.info("Find sub_categories: " + sub_category.keys().__str__())

            # 点击二级职位
            # for s_k, s_v in sub_category.items():
            for s_k, s_v in {"后端开发": sub_category["后端开发"]}.items():
                s_v.click()
                # driver.execute_script("arguments[0].click();", s_v)
                time.sleep(1)
                logging.info("Clicked button " + s_k)

                # 选择三级职位
                sub_sub_category_elements = driver.find_elements(By.XPATH,
                                                                 "//div[@class='el-scrollbar nowcoder-custom el-cascader-menu'][3]//span[@class='el-cascader-node__label']")
                sub_sub_category = {c.text: c for c in sub_sub_category_elements if c.text != ""}
                logging.info("Find sub_sub_categories: " + sub_sub_category.keys().__str__())

                # 点击三级职位
                for ss_k, ss_v in sub_sub_category.items():
                    ss_v.click()
                    # driver.execute_script("arguments[0].click();", ss_v)
                    time.sleep(2)
                    logging.info("Clicked button " + ss_k)

                    # 将滚动条滑动到页面底部
                    while True:
                        # 模拟滑动操作
                        actions = ActionChains(driver)
                        actions.send_keys(Keys.END).perform()

                        # 等待页面加载
                        time.sleep(3)

                        # 检查是否已到达页面底部
                        if driver.execute_script(
                                "return window.pageYOffset + window.innerHeight >= document.body.scrollHeight"):
                            break

                    # 获取页面的源代码
                    content = driver.page_source
                    html = etree.HTML(content, parser=etree.HTMLParser())
                    self.urls[k + '-' + s_k + '-' + ss_k] = html.xpath(
                        '//a[@class="recruitment-job-card feed-job-card"]/@href')

                    driver.find_element(By.XPATH, "//div[@data-v-3683ca40]").click()
                    # element = driver.find_element(By.XPATH, "//div[@data-v-3683ca40]")
                    # driver.execute_script("arguments[0].click();", element)
                    time.sleep(1)

        with open("urls.txt", "w", encoding='utf-8') as f:
            f.write(self.urls.__str__())
        driver.close()

    def start_requests(self):
        for category, urls in self.urls.items():
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse, meta={"category": category}, dont_filter=True)

    def parse(self, response):
        item = EmployItem()
        item["company"] = response.xpath("//div[@class='company-card card-container']/div//text()").extract()[0]
        salary = response.xpath("//div[@class='salary']//text()").extract()[0]
        if salary == '薪资面议' or salary is None:
            item["salary"] = None
        else:
            strs = salary.strip().strip("薪").split('*')
            months = int(strs[1])
            s_min, s_max = strs[0].strip().strip("K").split("-")
            item["salary"] = months * 0.5 * (int(s_min) + int(s_max)) * 1000
        infos = response.xpath("//div[@class='extra flex-row']")
        item["city"] = infos.xpath("//span[@class='el-tooltip']//text()").extract()[0]
        item["education"] = infos.xpath("//span[@class='edu-level']//text()").extract()[0]
        item["job"] = response.meta["category"]
        item["details"] = '\n'.join(response.xpath("//div[@class='job-detail-infos tw-flex-auto']//text()").extract())

        yield item

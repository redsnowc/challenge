import json
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

results = []


def parse(response):
    for comment in response.css('div.comment-list-item'):
        result = {}
        result['name'] = comment.css(
            'div.user-username a::text').extract_first().strip()
        result['content'] = ', '.join(comment.css(
            'div.comment-item-content.markdown-box p::text').extract())
        results.append(result)
    return results


def has_next_page(response):
    if bool(response.css('li.disabled.next-page').extract()):
        return False
    else:
        return True


def goto_next_page(driver):
    driver.find_element_by_class_name('next-page').click()


def wait_page_return(driver, page):
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//ul[@class="pagination"]/li[@class="active"]'),
            str(page)
        )
    )


def spider():
    driver = webdriver.PhantomJS()
    # 本地推荐用chrome、firefox
    # driver = webdriver.Firefox()
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1

    while True:
        wait_page_return(driver, page)
        html = driver.page_source
        response = HtmlResponse(url, body=html.encode('utf8'))
        parse(response)
        if not has_next_page(response):
            break
        page += 1
        goto_next_page(driver)

    with open('comments.json', 'w', encoding='utf-8') as f_obj:
        json.dump(results, f_obj, ensure_ascii=False)

    driver.close()


if __name__ == '__main__':
    spider()

#https://googlechromelabs.github.io/chrome-for-testing/#stable
'''
1. 元素定位
2. 元素被遮掩
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

import random

import threading
'''
click_element(driver, 'id', 'some-id')
click_element(driver, 'class_name', 'some-class')
click_element(driver, 'xpath', '//div[@class="some-class"]')
'''
def get_element(driver, locator, value, wait_time=10, attempts=3):
    wait = WebDriverWait(driver, wait_time)
    for attempt in range(attempts):
        try:
            element = wait.until(EC.visibility_of_element_located((getattr(By, locator.upper()), value)))
            # WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((getattr(By, locator.upper()), value)))
            return element

        except StaleElementReferenceException:
            if attempt < attempts - 1:  # 如果不是最后一次尝试，那么就忽略异常
                continue
            else:  # 如果是最后一次尝试，那么就抛出异常
                raise



dir_path = os.path.dirname(os.path.realpath(__file__))
# 创建一个webdriver的实例，指定chromedriver的路径
service = Service(os.path.join(dir_path, 'chromedriver'))
browser = webdriver.Chrome(service=service)
# browser = webdriver.Chrome(executable_path=os.path.join(dir_path, 'chromedriver'))
# browser.implicitly_wait(30) # seconds

course_list=[]

def SelectElem(name):
  return browser.find_element(By.CSS_SELECTOR, name)

def WaitElem(name, time):
  wait = WebDriverWait(browser, time)
  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, name)))

# 元素name表:



def login():

  browser.get('https://new.cddyjy.com/login/pwd')
  # 等待登录按钮出现
  WaitElem("button.login-button.ant-btn.ant-btn-primary" ,10)


# guliangjin 341B31B386087188  J1j26ffr
  idcard_element = SelectElem("input#username.ant-input.ant-input-lg")
  password_element = SelectElem("input#password.ant-input.ant-input-lg")
  idcard_element.send_keys('341B31B386087188')
  password_element.send_keys('J1j26ffr')

  check_button = SelectElem("input.ant-checkbox-input")
  check_button.click()
  login_button = SelectElem("button.login-button.ant-btn.ant-btn-primary")
  login_button.click()

  # 使用 WebDriverWait 等待下一个页面的特定元素加载完成
  try:
      # 假设你要等待的元素是下一个页面的某个标识元素
      WebDriverWait(browser, 100).until(
          EC.visibility_of_element_located((By.CSS_SELECTOR, "div.ant-dropdown-trigger"))
      )
  except Exception as e:
      print("Error waiting for the next page to load:", e)


def go_course_page():
  # 创建 ActionChains 实例
  actions = ActionChains(browser)

  # 打开一个新的浏览器标签
  actions.send_keys(Keys.CONTROL + 't').perform()

  # 切换到新的浏览器标签
  browser.switch_to.window(browser.window_handles[-1])

  # 在新的标签中打开另一个网页
  # browser.get('https://rcxf.cddyjy.com/dyjy/civilServant')  #必修
  browser.get('https://rcxf.cddyjy.com/dyjy/civilServant')  #选修
  
  # 假设你要等待的元素是课程列表中的一个元素
  WebDriverWait(browser, 100).until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, ".civil-item"))
  )

  # 等待所有“选修课”选项卡元素加载完成
  elective_tab = WebDriverWait(browser, 20).until(
      EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-tabs-tab') and text()='选修课']"))
  )

  elective_tab.click()
  print("成功点击第一个选修课按钮")
  time.sleep(5)

def get_course_list():
    unfinished_courses = []

    try:
        # 等待所有课程容器加载完成
        course_elements = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".civil-item"))
        )

        for course in course_elements:
            # 检查课程状态
            status = course.find_element(By.CSS_SELECTOR, ".right-tag").text

            if status == "未完成":
                # 添加到列表中      
                title = course.find_element(By.CSS_SELECTOR, "h3").text
                button = course.find_element(By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.ant-btn-circle')
                unfinished_courses.append((title, button))

        print(unfinished_courses)
    except Exception as e:
        print("未能找到课程元素:", e)

    return unfinished_courses

def learn_course(course):

  # 获取未完成课程列表  
  title, button = course 

  try:
      # 点击“去学习”按钮  
      button.click()  


      # 等待视频播放按钮加载并点击
      wait = WebDriverWait(browser, 5)
      play_buttons = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.vjs-big-play-button')))
      play_buttons.click()

      # 循环学习
      while not is_video_finished():
          time.sleep(60)

  except Exception:
      print(f"An error occurred with {title}, retrying...")

  close_button = browser.find_element(By.CSS_SELECTOR,'svg[data-icon="close"]')
  close_button.click()

def is_video_finished():

  progress_bar = browser.find_element(By.XPATH, "//div[contains(@class, 'vjs-progress-holder')]")

  # 获取进度条的当前进度
  progress = float(progress_bar.get_attribute('aria-valuenow'))

  if progress >= 100.0:
      print("视频已播放完成")
      return True
  else:
      print(f"视频还未播放完成,进度{progress}%")
      return False


if __name__ == '__main__':

  login()
  go_course_page()
  time.sleep(1)
  courses = get_course_list()
  continue_not_found_course_time = 0

  while True:  
    try:
      # 从课程列表中获取一个课程
      if len(courses) > 0:
          continue_not_found_course_time = 0
          course = random.choice(courses)
          learn_course(course)
      else:
          # 如果没有课程，尝试点击“下一页”按钮
          try:
              next_button = WebDriverWait(browser, 10).until(
                  EC.element_to_be_clickable((By.CSS_SELECTOR, "li.ant-pagination-next"))
              )
              next_button.click()

              # 等待下一页的课程列表加载完成
              WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".civil-item"))
              )
              # 重新获取课程列表
              courses = get_course_list()
          except Exception:
              # 如果找不到“下一页”按钮或超时，说明已经是最后一页
              continue_not_found_course_time += 1
              if continue_not_found_course_time > 100:
                  print(f"can't found course, try {continue_not_found_course_time} fail, exit!!!")
                  break
    except Exception:
      print("NoSuchElementException occurred, going back to course list...")
      go_course_page()  # 如果找不到元素，重新进入课程列表
      courses = get_course_list()  # 重新获取课程列表
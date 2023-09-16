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
browser = webdriver.Chrome(executable_path=os.path.join(dir_path, 'chromedriver'))
# browser.implicitly_wait(30) # seconds

course_list=[]



def login():
  
  browser.get('https://new.cddyjy.com/login/pwd')
  # 点击登录按钮
  # 等待登录按钮出现
  wait = WebDriverWait(browser, 60)
  login_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='登录']")))


  idcard_element = browser.find_element_by_class_name('ivu-input-large')
  idcard_element.send_keys('8F354445292435B2 ')
  password_element = browser.find_element_by_xpath("//input[@type='password']")
  password_element.send_keys('Rcxf123456')
  
  login_button.click()

  time.sleep(5)


def GoCouseList():
  # 创建 ActionChains 实例
  actions = ActionChains(browser)

  # 打开一个新的浏览器标签
  actions.send_keys(Keys.CONTROL + 't').perform()

  # 切换到新的浏览器标签
  browser.switch_to.window(browser.window_handles[-1])

  # 在新的标签中打开另一个网页
  browser.get('https://new.cddyjy.com/member-education/online/courseinfo?id=08db30f3-2ed6-b5f7-dba9-21acc9bdf544')

  time.sleep(5)
  
def GetCourseList():
    try:
        unfinished_courses = []
        # 找到所有课程的元素
        course_elements = browser.find_elements(By.CSS_SELECTOR, "tr.ivu-table-row")

        for course in course_elements:
            # 检查课程状态是不是"未完成"
            status = course.find_element(By.CSS_SELECTOR, "td:nth-child(6) div span").text
            if status == '未完成':
                # 如果课程未完成，获取课程名称并添加到列表中
                title = course.find_element(By.CSS_SELECTOR, "td:nth-child(1) div span span").text
                # 获取"去学习"按钮的元素
                button = course.find_element(By.CSS_SELECTOR, "td:nth-child(7) div a")
                unfinished_courses.append((title, button))

        time.sleep(2)
        return unfinished_courses

    except Exception:
        print("An error occurred while getting the course list, retrying...")
        return []  # 返回一个空列表

def LearnCourse(course):
  try:
      clicker = course[1]
      browser.execute_script("arguments[0].click();", clicker)
      wait = WebDriverWait(browser, 5)
      play_buttons = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.vjs-big-play-button')))
      play_buttons.click()
      while not isVideoFinished():
          time.sleep(60)
  except Exception:
      print(f"An error occurred with {course}, retrying...")

def isVideoFinished():
 
  progress_bar = browser.find_element(By.XPATH, "//div[contains(@class, 'vjs-progress-holder')]")

  # 获取进度条的当前进度
  progress = float(progress_bar.get_attribute('aria-valuenow'))

  if progress >= 100.0:
      print("视频已播放完成")
      return True
  else:
      print(f"视频还未播放完成,进度{progress}%")
      return False
   



login()
time.sleep(10)
GoCouseList()
courses = GetCourseList()
continue_not_found_course_time = 0

# print(courses)
while True:  
  try:
      # 从课程列表中获取一个课程
      if len(courses) > 0:
        continue_not_found_course_time = 0
        course = random.choice(courses)
        # course = courses.pop(0)
        # print("start : ", course)
        LearnCourse(course)
      GoCouseList()
  except Exception:
      print("NoSuchElementException occurred, going back to course list...")
      GoCouseList()  # 如果找不到元素，重新进入课程列表
  courses = GetCourseList()
  if len(courses) == 0:
    continue_not_found_course_time += 1
    if continue_not_found_course_time > 100:
      print(f"can't found course, try {continue_not_found_course_time} fail, exit!!!")











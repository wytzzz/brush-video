from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
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
            WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((getattr(By, locator.upper()), value)))
            return element
    
        except StaleElementReferenceException:
            if attempt < attempts - 1:  # 如果不是最后一次尝试，那么就忽略异常
                continue
            else:  # 如果是最后一次尝试，那么就抛出异常
                raise


dir_path = os.path.dirname(os.path.realpath(__file__))
# 创建一个webdriver的实例，指定chromedriver的路径
browser = webdriver.Chrome(executable_path=os.path.join(dir_path, 'chromedriver'))
course_list=[]



def login():

  browser.get('https://www.zgzjzj.com/learncenter/my-all-course')
  # 点击登录按钮
  # 等待登录按钮出现
  wait = WebDriverWait(browser, 10)
  login_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='登录 / 注册']")))
  login_button.click()

  # 等待身份证输入框出现
  wait = WebDriverWait(browser, 10)
  id_card_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'login_idCardInput')))

  # 输入身份证号和密码
  id_card_input.send_keys('510322197010174722')
  password_input = browser.find_element_by_class_name('login_pwdInput')
  password_input.send_keys('abcd1234')
  
  # 勾选复选框
  checkbox = browser.find_element_by_class_name('el-checkbox__inner')
  checkbox.click()

  # 提交登录表单（这取决于网页的具体结构，可能需要找到并点击一个"提交"按钮）
  submit_button = browser.find_element_by_class_name('login_submit')
  submit_button.click()
  

def GoCouseList():
  get_element(browser, "xpath", "//div[contains(text(),'学习中心')]").click()
  get_element(browser, 'xpath', "//button/span[contains(text(),'学习')]").click()
  get_element(browser, 'xpath', "//li[contains(text(),'未完成')]").click()

def GetCourseList():
  time.sleep(2)
  # 等待页面加载并找到所有的 'buyCourse_itemMain'
  items = browser.find_elements(By.CLASS_NAME, 'buyCourse_listItem')
  # if items:
  #   print(f'Found {len(items)} items.')
  # else:
  #   print('No items found.')
  # for item in items:
  #     title = item.find_element(By.CLASS_NAME, 'buyCourse_itemTitle').text
  #     course_type = item.find_element(By.CLASS_NAME, 'buyCourse_type').text
  #     course_time = item.find_element(By.CLASS_NAME, 'buyCourse_classTime').text
  #     progress_text = item.find_element(By.CLASS_NAME, 'progress_text').text
  #     print(f"Title: {title}")
  #     print(f"Type: {course_type}")
  #     print(f"Time: {course_time}")
  #     print(f"Progress: {progress_text}")
  #     print("\n")
  #     course_list.append(title)
  return items

def LearnCourse(course):
  
  time.sleep(2)
  # title_element = browser.find_element(By.XPATH, f"//span[@class='buyCourse_itemTitle el-popover__reference' and contains(text(), '{course_name}')]")
  start_button = course.find_element(By.XPATH, ".//ancestor::div[@class='buyCourse_listItem']//button/span[contains(text(), '学 习')]")
  start_button.click()
  time.sleep(5)
  while not IsCourseFinished():
    StartVideo()
    time.sleep(1)
    try_reset_video()
    time.sleep(3)
    while not isVideoFinished():
      time.sleep(10)
    time.sleep(1)
    NextVideo()
    time.sleep(5)
    if (IsLastVideo()):
      print("last video")
    



def StartVideo():
  try:
    play_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="vjs-big-play-button"]'))
    )
    play_button.click()
  except Exception as e:
    print(f"An error occurred: {e}")

def NextVideo():
    next_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, './/li[contains(@class, "nextdontcheatorshit")]'))
    )
    next_button.click()
     
def try_reset_video():
    try:
      time.sleep(2)  # 等待页面加载
      # 定位按钮
      reset_button = browser.find_element_by_xpath('//button[contains(@class, "vjs-play-control") and contains(@class, "vjs-paused")]')
      if reset_button and reset_button.is_displayed():
        reset_button.click()
      else:
        print("not find")
    except NoSuchElementException as e:
      print(f"An error occurred: {e}")

def isVideoFinished():
 
  # 找到视频进度条元素
  progress_element = browser.find_element(By.XPATH, "//div[@class='vjs-progress-holder vjs-slider vjs-slider-horizontal']")

  # 获取 aria-valuenow 属性的值，转换为浮点数
  progress_value = float(progress_element.get_attribute('aria-valuenow'))
  # print("curr video prograss ", progress_value)
  # 如果进度值等于 100，说明视频已经播放完毕
  if progress_value >= 100:
      return True
  else:
      return False

def IsLastVideo():
  try:
    confirm_button = browser.find_element_by_xpath("//button[contains(@class, 'el-button') and contains(@class, 'el-button--default') and contains(@class, 'el-button--small') and contains(@class, 'el-button--primary')]//span[contains(text(), '确定')]/..")
    if confirm_button and confirm_button.is_displayed():
        confirm_button.click() 
        time.sleep(1)  # 休眠1秒，你可以根据需要调整这个值
        return True
    else:
        return False
  except NoSuchElementException:
        print(f"An error occurred")
        return False

def IsCourseFinished():
    # return True
    # 寻找进度条元素
    progress_element = browser.find_element(By.XPATH, "//div[@role='progressbar']")
    # 获取进度条的当前值
    progress_value = progress_element.get_attribute("aria-valuenow")
    print("curr course prograss ", progress_value)
    if int(progress_value) >= 100:  # 检查进度是否达到100%
        return True
    else:
        return False
  

  
    
# def PauseCheckTimer():
#     while True:  # 永远不会自己结束
#         if IsVideoPaused():
#             print("Button found! Stopping video...")
#             # 在这里添加停止视频的代码
#         time.sleep(30)  # 每5秒检查一次

# def PlayCheck():
#   timer = threading.Thread(target=PauseCheckTimer)
#   timer.start() 


login()
time.sleep(2)
GoCouseList()
courses = GetCourseList()
while len(courses) > 0:  
    try:
        # 从课程列表中获取一个课程
        course = courses.pop(0)
        print("start : ", course)
        LearnCourse(course)
        GoCouseList()
    except NoSuchElementException:
        print(f"An error occurred with {course}")
        break
    # 在每次循环结束时，都重新获取课程列表
    courses = GetCourseList()









import sys,os,re,time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole  

# 提供元素选择功能
class BluesElementAction():

  def __init__(self,driver):
    self.driver = driver

  # === part 1:  find element === #
  def wait(self,selector,timeout=10,wait_type='presence'):
    '''
    @description : wait and return a WebElement
    @param {str}  selector : css selector
    @param {int} timeout : Maximum waiting time (s)
    @param {str} wait_type
    @returns {bool} if the element exists in the maximum time
    '''
    wait_func = self.__get_wait_func(selector,wait_type)
    try:
      BluesConsole.wait(selector,'Wait for element')
      return WebDriverWait(self.driver,timeout=timeout).until(wait_func)
    except Exception as e:
      return None

  def wait_removed(self,selector,timeout=20,step=1):
    '''
    @description : wait a element to be removed
    @param {str}  selector : css selector
    @param {int} timeout : Maximum waiting time (s)
    @param {int} set : wait seconds every time
    @returns {bool} if the element removed in maximum time
    '''
    for i in range(timeout):
      time.sleep(step)
      if not self.exists(selector):
        return True 
    return False

  def get(self,selector):
    '''
    @description : get the first WebElement, if none exists, an exception is thrown - dont't wait 1 second
    @param {str} selector : css selector
    @returns {WebElement}
    '''
    return self.driver.find_element(By.CSS_SELECTOR,selector)

  def get_all(self,selector):
    '''
    @description : get the first WebElement, if none exists, return empty list - dont't wait 1 second
    @param {str} selector : css selector
    @returns {WebElement[] | []}
    '''
    return self.driver.find_elements(By.CSS_SELECTOR,selector)

  # === part 2:  get element info === #
  def get_attr(self,selector,key):
    '''
    @description : get element's attribute
    @param {str} selector : css selector
    @param {str} key : attribute name, all HTML DOM attributes can be accessed
      - innerHTML
      - innerText
    @returns {str}
    '''
    web_element = self.wait(selector)
    return web_element.get_attribute(key)

  def get_text(self,selector):
    web_element = self.wait(selector)
    return web_element.text

  # === part 3:  check element status === #
  def exists(self,selector):
    '''
    @description : Determines whether the element exists
    @param {str} selector : css selector
    @returns {bool}
    '''
    eles = self.get_all(selector)
    return True if eles else False

  def is_presence(self,selector,timeout=1):
    return self.__get_status(selector,timeout,'presence')

  def is_visibility(self,selector,timeout=1):
    return self.__get_status(selector,timeout,'visibility')

  def is_clickable(self,selector,timeout=1):
    return self.__get_status(selector,timeout,'clickable')
  
  def is_enabled(self,selector):
    return self.get(selector).is_enabled()

  def is_displayed(self,selector):
    return self.get(selector).is_displayed()

  def is_selected(self,selector):
    return self.get(selector).is_selected()

  # === part last:  tool func === #
  def __get_status(self,selector,timeout,wait_type):
    '''
    @description : Determines whether the element exists
    @param {str} selector : css selector
    @param {str} wait_type
    @returns {bool}
    '''
    try:
      self.wait(selector,timeout,wait_type)
      return True
    except Exception as e:
      return False

  def __get_wait_func(self,selector,wait_type='presence'):
    '''
    @description 获取条件判断函数
    '''
    # 内置条件函数入参tuple格式
    css_selector = (By.CSS_SELECTOR,selector)

    funcs = {
      'presence':expected_conditions.presence_of_element_located, # 存在于DOM中（可见或不可见）
      'visibility':expected_conditions.visibility_of_element_located, # 存在于DOM中且可见（非隐藏状态，不一定再当前窗口中）
      'clickable':expected_conditions.element_to_be_clickable, # 存在于DOM中且可见，可点击（在当前窗口中）
      'selected':expected_conditions.element_to_be_selected, # 专用于下拉选择项，存在与DOM中，且元素是被选中
    }

    func = funcs.get(wait_type,funcs['presence']) 
    return func(css_selector)

    
    


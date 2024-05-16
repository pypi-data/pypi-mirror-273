
from selenium.webdriver import ActionChains
from .BluesElementAction import BluesElementAction

class BluesEventAction():
  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElementAction(driver)
    self.chains = ActionChains(driver)

  def click(self,selector):
    '''
    @description 单击
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.click(locator).perform()
  
  def hold(self,selector):
    '''
    @description 点击按住不放
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.click_and_hold(locator).perform()

  def release(self,selector):
    '''
    @description 释放按下的鼠标
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.release(locator).perform()

  def right_click(self,selector):
    '''
    @description 右击
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.context_click(locator).perform()

  def double_click(self,selector):
    '''
    @description 双击
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.double_click(locator).perform()

  def hover(self,selector):
    '''
    @description 鼠标移入元素，悬浮上方
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.move_to_element(locator).perform()

  
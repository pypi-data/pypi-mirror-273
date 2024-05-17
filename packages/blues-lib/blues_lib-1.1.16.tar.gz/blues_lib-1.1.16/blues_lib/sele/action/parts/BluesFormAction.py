from selenium.webdriver.common.keys import Keys
from .BluesElementAction import BluesElementAction

class BluesFormAction():

  SHORTCUTS={
    'select':Keys.CONTROL+"A",
    'copy':(Keys.CONTROL+"A",Keys.CONTROL+"C"),
    'paste':Keys.CONTROL+"V",
    'cut':(Keys.CONTROL+"A",Keys.CONTROL+"X"), # 拼接为同时使用
    'clear':(Keys.CONTROL+"A",Keys.DELETE), # 元组元素为依次使用
    'space':Keys.SPACE,
    'enter':Keys.ENTER,
  }

  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElementAction(driver)

  def shortcut(self,selector,shortcut):
    texts = self.SHORTCUTS.get(shortcut)
    if not texts:
      return 
    
    if type(texts) == str:
      texts = (texts,)

    # multi shortcuts must be type one by one 
    for text in texts:
      self.__type(selector,text) 
    
  def __type(self,selector,texts):
    '''
    @description : type text
    @param {str} selector : css selector
    @param {str|tuple|list} texts
    '''
    web_element = self.element_action.wait(selector)
    input_texts = (texts,) if type(texts)==str else texts 
    web_element.send_keys(*input_texts)

  def write(self,selector,texts):
    '''
    @description : type text
    @param {str} selector : css selector
    @param {str|tuple|list} texts
    '''
    self.shortcut(selector,'clear')
    self.__type(selector,texts)

  def write_after(self,selector,texts):
    self.__type(selector,texts)
  
  def write_file(self,selector,texts):
    self.__type(selector,texts)
  
  def empty(self,selector):
    self.shortcut(selector,'clear')
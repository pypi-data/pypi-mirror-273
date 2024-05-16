import sys,os,re,time
from .BluesJavaScriptAction import BluesJavaScriptAction

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesType import BluesType 

# 提供窗口相关功能
class BluesWindowAction():
 
  def __init__(self,driver):
    self.driver = driver
    self.js_action = BluesJavaScriptAction(driver)
    self.history_handles = [self.get_handle()]
  
  def shot(self,file=None):
    '''
    @description : shot screen as a file
    @param {str} file : File save address
    @returns {None} 
    '''
    file_path = file if file else self.__get_default_file()
    shot_status = self.driver.save_screenshot(file_path)
    return file_path if shot_status else ''

  def shot_base64(self):
    '''
    @description : shot screen as base64 string
    @returns {str} : base64 string
    '''
    return self.driver.get_screenshot_as_base64()

  def __get_default_file(self,prefix='screenshot'):
    timestamp = int(time.time()) 
    return './%s-%s.png' % (prefix,timestamp)

  def get_handle(self):
    '''
    @description : get current active tab's handle id
    @returns {str} handle id, such as : 3D31BF6D96E5671253E70BCF33DC7F39
    '''
    return self.driver.current_window_handle

  # 所有窗口句柄 list
  def get_handles(self):
    '''
    @description : get all tab's handle id
    @returns {list} handle id, such as : ['3D31BF6D96E5671253E70BCF33DC7F39']
    '''
    return self.driver.window_handles

  def switch(self,handle):
    '''
    @description window窗口切换（切换浏览器tab页签）
    @param {string} handle 窗口句柄
    '''
    self.driver.switch_to.window(handle)

  def open_tab(self,url,name=''):
    self.js_action.open(url,name)
    new_handle = self.get_handles()[-1]
    self.history_handles.append(new_handle)
    self.switch(new_handle)

  def back_tab(self):
    if len(self.history_handles) > 1:
      prev_handle = self.history_handles[-2]
      self.switch(prev_handle)

  def forward_tab(self):
    current_handle = self.get_handle()
    current_handle_index = BluesType.last_index(self.history_handles,current_handle)
    if len(self.history_handles)-1>current_handle_index:
      next_handle = self.history_handles[current_handle_index+1]
      self.switch(next_handle)

  def get_size(self):
    '''
    @descripton : get current window's size
    @returns {dict} : {'width': 1755, 'height': 946}
    '''
    return self.driver.get_window_size()

  def resize(self,size):
    '''
    @description 修改窗口尺寸
    @param {tuple|list} size (width,height)
    '''
    self.driver.set_window_size(*size)

  def maximize(self):
    '''
    @description : maximize
    '''
    self.driver.maximize_window()

  def minimize(self):
    '''
    @description : hide the chrome window
    '''
    self.driver.minimize_window()

  def fullscreen(self):
    '''
    @description : maximize and hide the tabs
    '''
    self.driver.fullscreen_window()

  def position(self,position):
    '''
    @description 修改窗口位置
    @param {tuple} position (x,y)
    '''
    self.driver.set_window_position(*position)
     
  def refresh(self):
    self.driver.refresh()
      
  def back(self):
    self.driver.back()
      
  def forward(self):
    self.driver.forward()

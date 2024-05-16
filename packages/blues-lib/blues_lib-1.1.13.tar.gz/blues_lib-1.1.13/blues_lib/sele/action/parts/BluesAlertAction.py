import time
# Provides methods for handling three pop-ups
class BluesAlertAction():
 
  def __init__(self,driver):
    self.driver = driver

  '''
  @description frame 切换到alert，不区分三种弹框类型
  @returns {WebElement} alert对象
  '''
  def switch(self):
    return self.driver.switch_to.alert

  '''
  @description 接受-并关闭弹框,the driver will back to main window automatically
  @param {string} text prompt框输入文本
  '''
  def accept(self,text=None):
    alert = self.switch()
    if text!=None:
      alert.send_keys(text)
    alert.accept()
      
  '''
  @description 取消-并关闭弹框
  @param {string} text prompt框输入文本
  '''
  def dismiss(self,text=None):
    alert = self.switch()
    if text!=None:
      alert.send_keys(text)
    alert.dismiss()




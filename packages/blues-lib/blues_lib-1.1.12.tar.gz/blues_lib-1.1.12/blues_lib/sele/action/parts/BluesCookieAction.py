# 提供Cookie相关功能
class BluesCookieAction():
 
  def __init__(self,driver):
    self.driver = driver

  def get(self,name=''):
    '''
    @description : get one cookie
    @param {str} name : cookie name
    @returns {dict} 形如：{'domain': 'mp.163.com', 'httpOnly': True, 'name': 'NTESwebSI', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '2A7C7F8FCD65F7D74650E13D349C60CC'}
    '''
    return self.driver.get_cookie(name)

  def get_all(self):
    '''
    @description : get all cookies
    @returns {dict[]} 形如：[{'domain': 'mp.163.com', 'httpOnly': True, 'name': 'NTESwebSI', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '2A7C7F8FCD65F7D74650E13D349C60CC'}]
    '''
    return self.driver.get_cookies()
      
  '''
  @description 添加cookie
  @param {dict} cookie 字典形式的cookie对象，至少包含(其他元素自动填充默认)：
    - name
    - value
  '''
  def set(self,cookie):
    if cookie.get('name') and 'value' in cookie:
      self.driver.add_cookie(cookie)

  '''
  @description 删除cookie
  @param {string} name cookie name
  '''
  def remove(self,name=''):
    return self.driver.delete_cookie(name)
  
  def clear(self):
    return self.driver.delete_all_cookies()
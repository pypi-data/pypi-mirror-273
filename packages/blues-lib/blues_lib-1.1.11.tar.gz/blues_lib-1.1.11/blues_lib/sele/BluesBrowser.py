from .browser.BluesChrome import BluesChrome 
from .browser.BluesDebugChrome import BluesDebugChrome
from .browser.BluesProxyChrome import BluesProxyChrome

class BluesBrowser():

  @classmethod
  def chrome(cls,config={},arguments={},experimental_options={}):
    return BluesChrome(config,arguments,experimental_options)
  
  @classmethod
  def debug_chrome(cls,config={},arguments={},experimental_options={}):
    return BluesDebugChrome(config,arguments,experimental_options)
  
  @classmethod
  def proxy_chrome(cls,config={},arguments={},experimental_options={}):
    return BluesProxyChrome(config,arguments,experimental_options)
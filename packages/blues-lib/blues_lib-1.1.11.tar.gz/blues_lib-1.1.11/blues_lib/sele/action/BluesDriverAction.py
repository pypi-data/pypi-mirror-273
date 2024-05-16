from .parts.BluesElementAction import BluesElementAction
from .parts.BluesFormAction import BluesFormAction  
from .parts.BluesWindowAction import BluesWindowAction   
from .parts.BluesDocumentAction import BluesDocumentAction    
from .parts.BluesCookieAction import BluesCookieAction     
from .parts.BluesEventAction import BluesEventAction      
from .parts.BluesMoverAction import BluesMoverAction       
from .parts.BluesFrameAction import BluesFrameAction        
from .parts.BluesJavaScriptAction import BluesJavaScriptAction         
from .parts.BluesSelectAction import BluesSelectAction          
from .parts.BluesAlertAction import BluesAlertAction           

class BluesDriverAction():

  def __init__(self,driver):
    self.javascript = BluesJavaScriptAction(driver)
    self.element = BluesElementAction(driver)
    self.form = BluesFormAction(driver)
    self.window = BluesWindowAction(driver)
    self.document = BluesDocumentAction(driver)
    self.cookie = BluesCookieAction(driver)
    self.event = BluesEventAction(driver)
    self.mover = BluesMoverAction(driver)
    self.frame = BluesFrameAction(driver)
    self.select = BluesSelectAction(driver)
    self.alert = BluesAlertAction(driver)
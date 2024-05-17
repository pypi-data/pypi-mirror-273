class BluesConsole():

  COLORS = {
    'warn' : '\033[93m',
    'success' : '\033[92m',
    'info' : '\033[94m',
    'error' : '\033[91m',
    'wait' : '\033[95m',
    'bold' : '\033[1m',
    'underline' : '\033[4m',
    'default' : '\033[0m',
  }

  @classmethod
  def success(cls,value,label='Sucess'):
    '''
    @description : print value with colorful prefix
    @param {any} value : any type of value
    @param {str} label :  the label in prefix
    '''
    print(f"\n{cls.COLORS['success']}{label} >>> {cls.COLORS['default']}",value)
  
  @classmethod
  def info(cls,value,label='Info'):
    print(f"\n{cls.COLORS['info']}{label} >>> {cls.COLORS['default']}",value)
  
  @classmethod
  def warn(cls,value,label='Warn'):
    print(f"\n{cls.COLORS['warn']}{label} >>> {cls.COLORS['default']}",value)
  
  @classmethod
  def error(cls,value,label='Error'):
    print(f"\n{cls.COLORS['error']}{label} >>> {cls.COLORS['default']}",value)
  
  @classmethod
  def wait(cls,value,label='Wait'):
    print(f"\n{cls.COLORS['wait']}{label} >>> {cls.COLORS['default']}",value)
  
  @classmethod
  def bold(cls,value,label='Bold'):
    print(f"\n{cls.COLORS['bold']}{label} >>> {cls.COLORS['default']}",value)
  
  @classmethod
  def underline(cls,value,label='Underline'):
    print(f"\n{cls.COLORS['underline']}{label} >>> {cls.COLORS['default']}",value)
  
  @classmethod
  def print(cls,value,label='Log'):
    print(f"\n{label} >>> ",value)


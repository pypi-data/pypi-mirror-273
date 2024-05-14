class BluesConsole():

  COLORS = {
    'warn' : '\033[93m',
    'success' : '\033[92m',
    'info' : '\033[94m',
    'error' : '\033[91m',
    'light' : '\033[95m',
    'bold' : '\033[1m',
    'underline' : '\033[4m',
    'default' : '\033[0m',
  }

  @classmethod
  def success(cls,value,label='sucess: '):
    '''
    @description : print value with colorful prefix
    @param {any} value : any type of value
    @param {str} label :  the label in prefix
    '''
    print(f"\n{cls.COLORS['success']}>>> {label}{cls.COLORS['default']}",value)
  
  @classmethod
  def info(cls,value,label='info: '):
    print(f"\n{cls.COLORS['info']}>>> {label}{cls.COLORS['default']}",value)
  
  @classmethod
  def warn(cls,value,label='warn: '):
    print(f"\n{cls.COLORS['warn']}>>> {label}{cls.COLORS['default']}",value)
  
  @classmethod
  def error(cls,value,label='error: '):
    print(f"\n{cls.COLORS['error']}>>> {label}{cls.COLORS['default']}",value)
  
  @classmethod
  def light(cls,value,label='light: '):
    print(f"\n{cls.COLORS['light']}>>> {label}{cls.COLORS['default']}",value)
  
  @classmethod
  def bold(cls,value,label='bold: '):
    print(f"\n{cls.COLORS['bold']}>>> {label}{cls.COLORS['default']}",value)
  
  @classmethod
  def underline(cls,value,label='underline: '):
    print(f"\n{cls.COLORS['underline']}>>> {label}{cls.COLORS['default']}",value)
  
  @classmethod
  def print(cls,value,label='log: '):
    print(f"\n>>> {label}",value)


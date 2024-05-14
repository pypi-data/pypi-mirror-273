import time

class BluesDateTime():

  spend = 0

  @classmethod
  def count_down(cls,payload):
    '''
    @description : count down
    @param {int} payload.duration  : duration seconds
    @param {int} payload.interval  : interval seconds
    @param {str} payload.title  : title
    @param {bool} payload.printable  : print in the console
    '''

    duration = payload.get('duration',10)
    interval = payload.get('interval',1)
    title = payload.get('title','coutdown')
    printable = payload.get('printable')
    
    if printable: 
      print('===> %s : %s' % (title,duration-cls.spend))

    time.sleep(interval) 
    cls.spend+=interval
    if cls.spend < duration:
      cls.count_down(payload)
    else:
      cls.spend=0
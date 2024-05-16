import sys,os,re,json
from seleniumwire import webdriver
from seleniumwire.utils import decode
from .BluesChrome import BluesChrome

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesFiler import BluesFiler  

class BluesProxyChrome(BluesChrome):
  # https://pypi.org/project/selenium-wire/
  def __init__(self,config={},arguments={},experimental_options={}):
    super().__init__(config,arguments,experimental_options)

  def after_created(self):
    self.__set_wire()
    super().after_created()

  def __set_wire(self):
    wire = self.config.get('wire')
    if not wire:
      return
    for key,value in wire.items():
      setattr(self.driver,key,value)

  def get_driver_creator(self):
    '''
    @description : get the webdirver isntance
    '''
    return webdriver

  def get_requests(self,config={}):
    '''
    @description : get all request and response info
    @prams {dict} config:
      - is_light : weather returen the repsone's body 
      - url_pattern : If this parameter is passed, urls are filtered accordingly
      - json_file : save the req and res info to a json file
    @returns [dict[]] 字典数组
    '''
    config['is_light']=False
    return self.__get_req_res(config)
    
  def get_light_requests(self,config):
    '''
    @description : get light weight requests data, without response's body
    '''
    config['is_light']=True
    return self.__get_req_res(config)

  def __save_to_json(self,json_file,requests):
    try:
      BluesFiler.write(json_file,json.dumps(requests,indent=2))
      return {
        'code':200,
        'message':'success',
        'json_file':json_file,
      }
    except Exception as e:
      return {
        'code':500,
        'message':'%s' % e,
      }

  def __get_req_res(self,config):
    if not self.driver.requests:
      return None

    requests = []
    maxcount = config.get('maxcount',-1) # -1 indicates that all data is obtained
    url_pattern = config.get('url_pattern')
    cookie_pattern = config.get('cookie_pattern')
    filter_func = config.get('filter_func')
    json_file = config.get('json_file')

    for request in self.driver.requests:
      if not request.response:
        continue
      
      # filter by url_pattern
      if url_pattern:
        if not re.search(url_pattern,request.url):
          continue

      # filter by cookie_pattern
      if cookie_pattern:
        cookie = request.headers.get('Cookie')
        if not cookie or not re.search(cookie_pattern,cookie):
          continue

      item = self.__get_item(request,config)
      # filter by user-defined func
      if filter_func:
        if not filter_func(item):
          continue
       
      requests.append(item)

      # break by maxcount
      if maxcount!=-1 and len(requests)>=maxcount:
        break

    if json_file :
      return self.__save_to_json(json_file,requests)
    else:
      return requests if requests else None


  def __get_item(self,request,config):
    is_light = config.get('is_light',False)
    return {
      'url':request.url, 
      'path':request.path, 
      'querystring':request.querystring, 
      'method':request.method, 
      'headers':dict(request.headers), 
      'cookie':request.headers.get('Cookie'),
      'params':request.params, 
      'date':request.date.isoformat(), 
      #'cert':request.cert, 
      'body':self.__get_request_body(request.body), 
      'response':self.__get_response(request.response,is_light), 
    }

  def __get_request_body(self,body):
    return str(body, encoding='utf-8')

  def __get_response(self,response,is_light=False):
    item = {
      'status_code':response.status_code, 
      'reason':response.reason, 
      'headers':dict(response.headers), 
      'date':response.date.isoformat(), 
    }
    if not is_light:
      encoding = response.headers.get('Content-encoding', 'identity')
      body = decode(response.body, encoding)
      item['body'] = body

    return item

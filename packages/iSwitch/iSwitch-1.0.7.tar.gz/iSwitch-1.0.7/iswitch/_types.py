from _collections_abc import dict_keys
import sys
import simplejson as Json
from typing import (
    Any, TypedDict, Sequence, Optional,
    Mapping
)
    
from iswitch._utils import (
    Logger
)

####
##      APPLICATION MODEL
#####
class Application(TypedDict):
    ''' Application Representation class. '''
    
    id: str                         # APPLICATION IDENTIFYER
    code: str                       # APPLICATION REFERENCE CODE
    email: str                      # APPLICATION EMAIL
    username: str                   # APPLICATION USERNAME
    phone_number: str               # APPLICATION PHONE NUMBER
    is_active: bool                 # IF APPLICATION IS ACTIVE OR NOT
    is_verified: bool               # IF APPLICATION ACCOUNT IS VERIFIED
    created: str                    # DATE OF CREATION
    modified: str                   # LAST MODIFICATION DATE
    last_login: str                 # LAST LOGIN DATE
    
    
####
##      AUTH MODEL
#####
class Credential(TypedDict):
    ''' Authentication Credentials Model. '''
    
    username : str                        # Username
    password : str                        # Password
  
  
####
##      CONFIGS REPRESENTATION CLASS
#####
class Config(TypedDict,total=True):
    """ The base class for all configs. """
    
    service : str                         # ServiceName
    raise_on_error :bool                  # IF SET TO TRUE, RAISE IF EXCEPTION OCCURES 
    

####
##      AUTH CONFIGS REPRESENTATION CLASS
#####
class AuthConfig(Config):
    """ The Auth configs. """
    
    credentials : Credential              # AUTH MODEL
    host: Optional[str] = None,           # HOST
        

####
##      TRANSACTION CLASS
#####
class Transaction(object):
    ''' Represents Transaction.

        - `amount` : int
        Amount of the transaction 
        - `callback_url` : str
        Callback URL to receive notifications about the transaction
        - `return_url` : str
        Return URL after a successful payment
       - `application` : str
        The requesting Application id 
        - `order` : dict
        Transaction Order extra informations.
    '''
    
    def __init__(
        self,
        amount,
        callback_url = None,
        return_url = None,
        application = '',
        order = {}
    ):
        self.amount = amount
        self.callback_url = callback_url
        self.return_url = return_url
        self.application = application
        self.order = order
        self.provider = None
        
    def to_representation(self):
        ''' Return a dict representation of a transaction. '''
        
        return {
            'amount': self.amount,
            'callback_url': self.callback_url,
            'return_url': self.return_url,
            'application': self.application,
            'provider': self.provider,
            'order': self.order
        }
        
        
####
##      REQUEST RESPONSE
#####
class Response:
    ''' Request response Manager. '''
    
    def __init__(
        self,
        response = None,
        context = {}
    ):
        self.response = response
        self.context = context
        
        # INITIALIZE LOGGER
        self.logger = Logger('Response Manager')
        
    @property
    def json(self):
        ''' Return response json content. '''
        return self.response.json()
    
    @property
    def client(self):
        ''' Get the request Client instance. '''
        return self.context.get('client')
    
    @property
    def request(self):
        ''' Get the related request object. '''
        return self.response.request
    
    @property
    def status_code(self):
        ''' Get HTTP Status Code of the response. '''
        return self.response.status_code
    
    @property
    def base_url(self):
        ''' Return context Base URL. '''
        return self.context['base_url']
    
    @property
    def has_error(self):
        ''' Check if it's an error response. '''
        return False
    
    def __str__(self) -> str:
        return f'<Class {self.__class__.__name__} status: {self.status_code}, error: {self.has_error}>'
    
    
####
##      PAGGINATED RESPONSE MANAGER
#####
class PagginatedResponse(Response):
    ''' Used to manage pagginated responses. '''
    
    # OBJECTS COUNT
    count : int = 0
    # NEXT PAGE URL
    next_url : str = ''
    # PREVIOUS PAGE URL
    previous_url : str = ''
    # RESULTS 
    results: Sequence[Mapping[str,Any]] = []
    
    def __init__(self, response=None, context={}):
        super().__init__(response, context)
        
        self.process_data()
        
        # LOGGING SUCCESS
        self.logger.info(
            f'{self.request.method} {self.request.url} {self.response.status_code}'
        )
        
    def __str__(self):
        return f'''
            'status': {self.response.status_code}
            'count': {self.count},
            'next':{self.next_url},
            'previous':{self.previous_url},
        '''
        
    def process_data(self):
        '''  '''
        
        data = self.json
        self.count = data['count']
        self.next_url = data['next'] or None
        self.previous_url = data['previous'] or None
        self.results = data['results']
        
    @property
    def has_next(self):
        return self.next_url is not None
    
    @property
    def has_prev(self):
        return self.previous_url is not None
        
    @property
    def next_page(self):
        ''' Send request to get next page objects '''
        # RAISE VALUE ERROR IF NEXT URL IS NONE
        if not self.next_url: raise
        
        # GET ENDPOINT FROM URL
        _,__,endpoint = self.next_url.partition(
            self.base_url
        )
        # SEND REQUEST
        return self.send_request(endpoint = endpoint)
    
    @property
    def previous_page(self):
        ''' Send request to get previous page objects '''
        # RAISE VALUE ERROR IF NEXT URL IS NONE
        if not self.previous_url: raise
        
        # GET ENDPOINT FROM URL
        _,__,endpoint = self.previous_url.partition(
            self.base_url
        )
        # SEND REQUEST
        return self.send_request(endpoint = endpoint)
        
    def send_request(self,endpoint):
        ''' Send request using context client. '''
        # DON'T FORGET AUTHENTICATION
        self.client.authenticate()
        
        return self.client._request(
            "GET", True, end_point = endpoint 
        )
      
      
####
##      ERROR RESPONSE
#####
class ErrorResponse(Response):
    ''' Error Response Manager. '''
    
    # MESSAGE ATTR KEYS
    keys = [
        'detail','message','non_field_errors'
    ]
    
    def __init__(self, response=None, context={}):
        super().__init__(response, context)
        
        self.logger.error(
            self.get_message()
        )
        
    @property
    def has_error(self):
        ''' Check if it's an error response. '''
        return True
        
    def get_message(self) -> str:
        ''' Get message from response. '''
        
        # GET MESSAGE FROM RESPONSE JSON
        try:
            for key in self.keys:
                if key in self.json:
                    return self.json.get(
                        key, self.response.text
                    )
            return f'{self.json}'
                    
        except Exception as e:
            # RETURN RESPONSE TEXT OTHERWISE
            return self.response.text
            
    
####
##      RESPONSE ERROR
#####        
class ResponseError(Exception):
  """
  Common class for response errors.
  """

  def __init__(self, error: str, status_code: int = -1):
    try:
      # TRY TO PARSE CONTENT AS JSON AND EXTRACT 'error'
      # FALLBACK TO RAW content if JSON parsing fails
      error = Json.loads(error).get('detail', error)
    except Json.JSONDecodeError:
      ...

    super().__init__(error)
    self.error = error
    'Reason for the error.'

    self.status_code = status_code
    'HTTP status code of the response.'
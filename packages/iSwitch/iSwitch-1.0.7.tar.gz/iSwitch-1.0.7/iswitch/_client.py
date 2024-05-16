import sys
import httpx
import platform
import simplejson as Json
from importlib import metadata

try:
    __version__ = metadata.version('iSwitch')
except metadata.PackageNotFoundError:
    __version__ = '0.0.0'
    
from iswitch._utils import (
    UrlUtils, Logger
)
from iswitch._services import get_service
from iswitch._types import (
    AuthConfig, Transaction,Response,
    PagginatedResponse, ResponseError,
    ErrorResponse, Application
)
    
## VARIABLES
USER_AGENT = (
    f'iSwitch-python/{__version__} ({platform.machine()}'
    f'{platform.system().lower()}) Python/{platform.python_version()}'
    )

DEFAULT_API_HOST = 'http://127.0.0.1:9000'

  
####
##      BASE CLIENT
#####
class BaseClient:
    """
        Creates a httpx client. Default parameters are the same as those defined in httpx
        except for the following:
        - `follow_redirects`: True
        - `timeout`: None
        - `configs`: AuthConfig
        `kwargs` are passed to the httpx client.
    """
    
    def __init__(
        self,
        configs : AuthConfig,
        **kwargs,
    ) -> None:
        
        # INITIALIZE CONFIGS
        self.config = AuthConfig(**configs)
        self.service  = get_service(
            self.config['service'],
        )
        self.token = None
        self._client = self.get_client(**kwargs)
        self.logger = Logger('Client')
        
        # ACTIVE APPLICATION
        self.application = None
        
        # PAYMENT PROVIDER
        self.provider = None
        
    def set_token(self,token):
        ''' Update token. '''
        
        self.token = token
        
    def set_application(self,data:Application):
        ''' Fill up active appliation informations. '''
        
        self.application = data

    def get_client(self,auth = False,**kwargs):
        ''' Return a new httpx client. '''
        # CREATE CLIENT NOW
        return httpx.Client(
            base_url = UrlUtils().parse_host(
                self.config.get('host') or DEFAULT_API_HOST
            ),
            headers = self._get_headers(
                authorization = auth
            ),
            **kwargs,
        )
    
    def _get_headers(self,authorization=False):
        ''' Return request Headers. '''

        # FILL REQUEST HEADERS
        headers = {
            'Content-Type':'application/json'
        }
        headers['Accept'] = 'application/json'
        headers['User-Agent'] = USER_AGENT
        if authorization:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def _get_response_context(self):
        ''' Return serponse context dic. '''
        return {
            'client': self,
            'base_url': DEFAULT_API_HOST
        }
    
    def _request(self, method: str, auth: bool, end_point: str = '', detail = False, **kwargs) -> httpx.Response:
        ''' Send request and return an Httpx Response. '''
        
        # ADD HEADERS TO
        response = self.get_client(auth).request(
            method, self.config['host'] + end_point, **kwargs
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self.logger.error(f'{e}')

        return self.process_response(
            response, detail = detail
        )
    
    def process_response(self,response ,detail = False):
        ''' Return appropriate response based on response. '''
        
        # GET CONTEXT
        context = self._get_response_context()
        
        # CHECK FOR SUCCESS
        if response.status_code in (200,201):
            
            return PagginatedResponse(
                response,context
            )if not detail else Response(
                response,context
            )
        
        # THEN RAISE RESPONSE ERROR IF NEEDED
        if self.config['raise_on_error']:
            raise ResponseError(
                response.text,response.status_code
            ) from None
        # RETURN ERROR RESPONSE ELSE
        else:
            return ErrorResponse(
                response, context
            )
        
####
##      CLIENT
#####
class Client(BaseClient):
    ''' iSwitch client 😎. '''
    
    def __init__(self, configs: AuthConfig, **kwargs) -> None:
        super().__init__(configs, **kwargs)
        
        self.provider = self.get_provider()
        
    def get_provider(self):
        ''' Return a payment provider based on configs. '''
        
        providers = self.list_providers()
        
        def search(prds:PagginatedResponse):
            ''' Search for a provider in pagginatedResponse '''
            if not prds.has_error:
                for p in prds.results:
                    if p['name'] == self.config['service']:
                        return p
                # THEN THIS PAGE DON'T CONTAINS THE SPECIFIED PROVIDER
                if p.has_next:
                    search(p.next_page)
            
            return None       
        return search(providers)     
    
    def authenticate(self):
        ''' Authenticates App. '''
        
        # GET AUTH CREDENTIALS
        creds = self.config['credentials']
        
        # SEND REQUEST
        res = self._request(
            "POST", auth = False, end_point = 'auth/login', 
            detail = True, json = creds
        )
        # SET TOKEN 
        tkn = res.json.get('access_token')
        self.set_token(
            tkn
        )
        # SETTING UP ACTIVE APPLICATION
        self.set_application(
            res.json.get('user')
        )
        
    def get_application(self):
        ''' Return active application. '''
        return self.application
    
    def list_providers(self):
        ''' Returns a list of available providers services. '''
        
        # AUTHENTICATE REQUEST FIRST
        self.authenticate()
        
        # THEN SEND REQUEST
        return self._request(
            'GET', auth = True,
            end_point = '/payments/aggregators'
        )
    
    def list_transactions(self):
        ''' Return App Transactions. '''
        
        # AUTHENTICATE REQUEST FIRST
        self.authenticate()
        
        # SEND REQUEST TO API
        return self._request(
            "GET", auth = True, 
            end_point = '/payments/transactions',
        )
      
    def create_transaction(self,transaction:Transaction):
        ''' Initialize a new payment transaction. '''
        # AUTHENTICATE REQUEST
        self.authenticate()
        
        # ADD PROVIDER TO TRANSACTION
        transaction.provider = self.provider['id']
        
        # VALIDATE TRANSACTION ORDER
        t = self.service(
            transaction,
            context = self._get_response_context()
        ).prepare_transaction()
        
        # SEND REQUEST TO API
        return self._request(
            "POST", auth = True,detail = True,
            end_point = '/payments/transactions',
            json = t
        )
        
    def get_transaction(self,transaction_id:str):
        ''' Get details for a specific transaction. '''
        
        # AUTHENTICATE REQUEST FIRST
        self.authenticate()
        
        # SEND REQUEST TO API
        return self._request(
            "GET", auth = True, detail = True,
            end_point = f'/payments/transactions/{transaction_id}'
        )
        
    def get_bill_url(self,transaction_id:str):
        ''' Returns the URL to view a bill associated with a specific transaction. '''
        # AUTHENTICATE REQUEST
        self.authenticate()
        
        return self._request(
            "GET", auth = True, detail = True,
            end_point = f'payments/transactions/{transaction_id}/get_bill_url',
        )
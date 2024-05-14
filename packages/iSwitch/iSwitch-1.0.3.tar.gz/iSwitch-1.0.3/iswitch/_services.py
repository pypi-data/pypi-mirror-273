from iswitch._types import (
    Transaction
)
from iswitch._utils import (
    Logger
)
import simplejson as Json

####
##      SERVICES FACTORY
#####
class Factory:
    ''' Factory of all Registred payment services. '''
    
    # REGISTRY
    registry = {}
    # LOGGER
    logger = Logger('Services Factory')
    
    @classmethod
    def register(cls, name):
        ''' Decorator to add connector to registry. '''
        def decorator(manager_class):
            # SERVICE MANAGER MUST BE BASE SERVICE INSTANCE
            if issubclass(manager_class, BaseService):
                # ADD SERVICE TO REGISTRY
                cls.registry[name] = manager_class
                # LOGGING
                cls.logger.info(
                    f'{name} service registered.'
                )
                return manager_class
            # RAISE EXCEPTION ELSE
            else:
                # LOGGING
                cls.logger.warning(
                    f'Cannot register service {name}.'
                    f'Invalid service type, looking for "BaseService" '
                    f'got "{manager_class.__name__}" abborting...'
                )
                # raise TypeError(
                #     f'Invalid service type, looking for "BaseService" '
                #     f'got {manager_class.__name__}'
                # )
        return decorator
            
    @classmethod  
    def get(cls,name):
        ''' return a registred manager by name. '''

        manager = cls.registry.get(name,None)
        if manager:
            return manager
        
        # DISPLAY HELP
        cls.help(name)
        
    @classmethod
    def help(cls,obj):
        ''' Raises an exeption... '''

        raise AttributeError(
            'Invalid Service name, '
            f'Factory has no registered service with name "{obj}".'
            f'choices are {cls.get_choices()}'
        )
    
    @classmethod
    def get_choices(cls):
        ''' Return a list of registered Connectors names '''

        return list(cls.registry.keys())


####
##      BASE SERVICE
#####
class BaseService:
    ''' Base service for all Payments Aggregators service. '''
        
    # ORDER REQUIRED FIELDS
    order_required_fields = {}
    
    def __init__(self,transaction:Transaction,context = {}) -> None:
        ''' Initialize service. '''
        
        self.transaction = transaction
        self.context = context
        
    def get_order_required_fields(self)->list:
        ''' return a equired fields to validate an order. '''
        return self.order_required_fields
    
    def validate_order(self, order: dict,required_fields = None,name = 'order'):
        ''' Validate the order against required fields. '''

        # GET REQUIRED FIELDS
        required_fields = required_fields or self.get_order_required_fields()

        def check(fields: list, parent: dict, name = name):
            ''' Check for fields. '''
            
            for field in fields:
                if field not in parent:
                    return False, f"Missing key '{field}' in '{name}' object."
            return True, ''

        def check_levels(obj, level_fields, name = name):
            ''' Recursive function to go through nested objects. '''
            # global required_fields
            
            for field, subfields in level_fields.items():
                
                if field not in obj:
                    return False, f"Missing key '{field}' in '{name}' object."
                
                if isinstance(subfields, dict):
                    # Recursively check nested fields
                    # check_levels(obj[field], subfields, f"{name}.{field}")
                    required_fields = self.get_order_required_fields()['second_level_fields'].get(field)
                    res, message = self.validate_order(
                        obj.get(field),required_fields,name=f'{name}.{field}'
                    )
                    if not res:
                        return res, message
            return True, ''

        # CHECK FIRST LEVEL OF ORDER
        res, message = check(required_fields['first_level_fields'], order)
        if not res:
            return res, message

        if 'second_level_fields' in required_fields:
            res, message = check_levels(order, required_fields['second_level_fields'])

        return res, message
    
    def validate_dict(self,data):
        ''' Check that data has all required valid keys. '''
        
        # GET REQUIRED FIELDS
        required_fields = self.get_order_required_fields()
        
        def check(fields, obj):
            ''' Check for fields. '''
            for field, subfields in fields.items():
                if field not in obj:
                    return False, f"Missing key '{field}' in '{obj}' object."
                if isinstance(subfields, dict):
                    result, error = check(subfields, obj[field])
                    if not result:
                        return result, error
                elif isinstance(subfields, list):
                    for subfield in subfields:
                        if subfield not in obj[field]:
                            return False, f"Missing key '{subfield}' in '{obj[field]}' object."
            return True, None

        if 'first_level_fields' in required_fields:
            result, error = check({'first_level_fields': required_fields['first_level_fields']}, data)
            if not result:
                return result, error

        if 'second_level_fields' in required_fields:
            for field, subfields in required_fields['second_level_fields'].items():
                if field in data:
                    result, error = check(subfields, data[field])
                    if not result:
                        return result, error

        return True, None
    
    def prepare_transaction(self) -> dict:
        ''' Prepare Transaction object for initialisation request. '''
        
        # CAN DO CUSTOM LOGIC HERE BASED ON 
        # PAYMENT SERVICE PROVIDER
        
        valid,msg =  self.validate_order(
            self.transaction.order
        )
        if not valid:
            # GET CONFIG FROM CONTEXT
            config = self.context.get('client').config
            if config['raise_on_error']:
                raise AttributeError(msg)
            else:
                self.context['client'].logger.warning(msg)
                
        # UPDATE TRANSACTION 
        rep = self.transaction.to_representation() 
        rep |= {
            'order': Json.dumps(
                self.transaction.order
            )
        }
        return rep
    
    
####
##      CINETPAY SERVICE
#####
@Factory.register(name = 'CINETPAY')
class CinetPay(BaseService):
    ''' CinetPay services. '''
    
    # ORDER REQUIRED FIELDS
    order_required_fields = {
        'first_level_fields': [
            'currency','transaction_id',
            'description','customer_name',
            'customer_surname'
        ]
    }
    
    
####
##      SEMOA SERVICE
#####
@Factory.register(name = 'SEMOA')
class Semoa(BaseService):
    ''' Semoa services. '''
    
    # ORDER REQUIRED FIELDS
    order_required_fields = {
        'first_level_fields':['merchant_reference','client'],
        'second_level_fields':{
            'client':{
                'first_level_fields': [
                    'first_name', 'last_name', 'phone'
                ]
            }
        }
    }
    

##      GET SERVICE FUNCTION
def get_service(service:str) -> BaseService|None:
    ''' Return service from a given name. '''
    
    return Factory.get(service)
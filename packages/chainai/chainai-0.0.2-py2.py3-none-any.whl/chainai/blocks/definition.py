from pydantic import BaseModel, Field, RootModel, ValidationError, validator
from typing import Any, Dict, List, Optional, Set, TypeVar, Generic, Type, Callable, Literal
from ..connector import BaseExecutionOutput
import yaml
import importlib
import functools


class EventDefinition(BaseModel):
    event: str
    description: str

class ActionsDefinition(BaseModel):
    trigger: Optional[List[EventDefinition]]
    output: Optional[List[EventDefinition]]

class BlockConfigDefinition(BaseModel):
    apiVersion: str = Field(..., alias='apiVersion')
    type: str
    metadata: Dict[str, Any]
    handler: str
    modes: List[str]
    actions: ActionsDefinition
    pool: Optional[Literal['cpu', 'cpu-listener', 'gpu']]
                 
def read_block_definition(yaml_path: str) -> BlockConfigDefinition:
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return BlockConfigDefinition(**data)

def register_trigger_handler(event_name: str) -> Callable:
    """Register a given function as a handler for a event trigger named `event_name`."""
    def decorator(func: Callable[..., BaseExecutionOutput]) -> Callable[..., BaseExecutionOutput]:
        # Use functools.wraps to preserve the metadata of the original function
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> BaseExecutionOutput:
            # Call the original function
            result = func(*args, **kwargs)
            # Check if the return type of the function is as expected
            if not isinstance(result, BaseExecutionOutput):
                raise TypeError(f"Expected return type {BaseExecutionOutput.__name__}, got {type(result).__name__}")
            result.mode = "trigger"
            result.event = event_name
            return result
        # Mark the function with the event name
        wrapper._event_name = event_name
        return wrapper
    return decorator

def register_output_handler(output_name: str) -> Callable:
    def decorator(func: Callable[..., BaseExecutionOutput]) -> Callable[..., BaseExecutionOutput]:
        """Register a given function as a handler for an output named `output_name`."""
        # Use functools.wraps to preserve the metadata of the original function
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> BaseExecutionOutput:
            # Call the original function
            result = func(*args, **kwargs)
            # Check if the return type of the function is as expected
            if not isinstance(result, BaseExecutionOutput):
                raise TypeError(f"Expected return type {BaseExecutionOutput.__name__}, got {type(result).__name__}")
            result.mode = "output"
            result.event = output_name
            return result
        # Mark the function with the event name
        wrapper._output_name = output_name
        return wrapper
    return decorator

class HandlerType(type):
    def __new__(cls, name, bases, namespace):
        cls_instance = super().__new__(cls, name, bases, namespace)
        cls_instance.trigger_handlers = {}
        cls_instance.output_handlers = {}
        # Register marked methods as handlers
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and hasattr(attr_value, '_event_name'):
                event_name = getattr(attr_value, '_event_name')
                cls_instance.trigger_handlers[event_name] = attr_value
            if callable(attr_value) and hasattr(attr_value, '_output_name'):
                output_name = getattr(attr_value, '_output_name')
                cls_instance.output_handlers[output_name] = attr_value
        return cls_instance
    
class StatelessPipelineBlock(metaclass=HandlerType):
    trigger_handlers: Dict[str, Callable]
    output_handlers: Dict[str, Callable]
    def __init__(self, config, instance_config):
        super().__init__()
        self.config = config
        self.instance_config = instance_config
        config_dict = config.dict()
        self.validate_instance_config(self.instance_config)
        if 'trigger' in config_dict['actions']:
            assert hasattr(self, 'trigger_handlers'), "No trigger handlers are defined"
            for trigger in config_dict['actions']['trigger']:
                if trigger['event'] not in self.trigger_handlers:
                    raise ValueError(f"Trigger event {trigger['event']} defined in manifest, but no handler is defined!")
        if 'output' in config_dict['actions']:
            assert hasattr(self, 'output_handlers'), "No output handlers are defined"
            for output in config_dict['actions']['output']:
                if output['event'] not in self.output_handlers:
                    raise ValueError(f"Output event {output['event']} defined in manifest, but no handler is defined!")
    def validate_instance_config(self, parameters: dict) -> None:
        """Code to validate the instance configuration. This function must raise an error if the configuration is invalid."""
        raise NotImplementedError("You must implement an instance configuration validator!")

class StatefulPipelineBlock(StatelessPipelineBlock):
    def __init__(self, config, instance_config):
        super().__init__(config=config, instance_config=instance_config)
    def listener_start(self):
        raise NotImplementedError("You must implement a listener start function!")
    def listener_stop(self):
        raise NotImplementedError("You must implement a listener stop function!")
    
def load_block(full_class_string):
    """
    Dynamically imports a class from a given string, handling nested modules.

    :param full_class_string: 'package.module.ClassName'
    :return: class object
    """
    module_name, class_name = full_class_string.rsplit('.', 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls
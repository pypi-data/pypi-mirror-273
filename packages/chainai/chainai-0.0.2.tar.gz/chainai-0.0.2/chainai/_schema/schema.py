from pydantic import BaseModel, Field, RootModel, ValidationError, field_validator
from typing import Any, Dict, List, Optional, Set

class TypeSpecificConfig(RootModel):
    pass

class BlockConfig(BaseModel):
    type: str
    typeSpecificConfig: TypeSpecificConfig

class Trigger(BaseModel):
    name: str
    event: str
    filter: str

class Output(BaseModel):
    id: str
    triggers: Optional[List[str]] = []
    inputs: Optional[List[str]] = []
    destination: str

class Stage(BaseModel):
    id: str = Field(..., max_length=255)
    type: str
    blockSpec: str
    blockConfig: BlockConfig
    triggers: List[Trigger] = []
    outputs: List[Output]

class Pipeline(BaseModel):
    apiVersion: str = Field(..., alias='apiVersion')
    type: str
    metadata: Dict[str, Any]
    stages: List[Stage]
    @field_validator('metadata')
    def metadata_must_contain_name_and_description(cls, v):
        if 'name' not in v:
            raise ValueError("The 'metadata' field must contain the 'name' field.")
        if 'description' not in v:
            raise ValueError("The 'metadata' field must contain the 'description' field.")
        return v

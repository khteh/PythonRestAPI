from datetime import datetime, date
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field, computed_field

class ContentModal(BaseModel):
    """
    The content object schema
    """
    data: bytes = Field(
        description="The data of the StorageObject"
    )
    mimeType: str = Field(
        description="The mime type of the StorageObject"
    )
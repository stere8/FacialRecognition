from pydantic import BaseModel
from typing import List, Dict

class RecognitionResult(BaseModel):
    names:List[str]
    boxes: List[Dict[str, int]]   # e.g., [{"top": ..., "right": ..., "bottom": ..., "left": ...}, ...]

from pydantic import BaseModel
from typing import List, Optional

class FHIRReference(BaseModel):
    reference: str

class FHIRCodeableConcept(BaseModel):
    text: Optional[str]
    coding: List[FHIRCoding]

class FHIRCoding(BaseModel):
    system: str
    code: str

class FHIREffectiveDateTime(BaseModel):
    effectiveDateTime: str

class FHIREffectivePeriod(BaseModel):
    start: str
    end: Optional[str]

class FHIRObservation(BaseModel):
    resourceType: str = "Observation"
    id: Optional[str]
    status: str
    code: FHIRCodeableConcept
    subject: Optional[FHIRReference]
    effectiveDateTime: Optional[str]
    effectivePeriod: Optional[FHIREffectivePeriod]
    valueQuantity: Optional[dict]
    interpretation: Optional[List[FHIRCodeableConcept]]
    comments: Optional[str]
    category: Optional[List[FHIRCodeableConcept]]
    component: Optional[List['FHIRObservation']]

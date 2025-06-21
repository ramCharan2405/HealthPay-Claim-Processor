from pydantic import BaseModel, Field
from typing import List, Optional, Union

class DocumentBase(BaseModel):
    type: str

class Bill(DocumentBase):
    type: str = "bill"
    hospital_name: Optional[str] = None
    total_amount: Optional[float] = None
    date_of_service: Optional[str] = None

class DischargeSummary(DocumentBase):
    type: str = "discharge_summary"
    patient_name: Optional[str] = None
    diagnosis: Optional[str] = None
    admission_date: Optional[str] = None
    discharge_date: Optional[str] = None
    
class MedicalRecord(DocumentBase):
    type: str = "medical_record"
    patient_name: Optional[str] = None
    record_details: Optional[str] = None


class IDCard(DocumentBase):
    type: str = "id_card"
    patient_name: Optional[str] = None
    policy_number: Optional[str] = None


class Validation(BaseModel):
    missing_documents: List[str] = []
    discrepancies: List[str] = []

class ClaimDecision(BaseModel):
    status: str
    reason: str

class ClaimResponse(BaseModel):
    documents: List[Union[Bill, DischargeSummary, MedicalRecord, IDCard]]
    validation: Validation
    claim_decision: ClaimDecision

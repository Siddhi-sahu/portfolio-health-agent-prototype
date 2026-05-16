from pydantic import BaseModel
from typing import List

class Loan(BaseModel):
    clientName: str
    daysLate: int
    loanAmount: float
    missedPayments: int
    inArrears: bool
    isNPA: bool
    delinquentAmount: float
    riskFlags: List[str]
    loanStatus: str


class OfficerFeedback(BaseModel):
    client: str
    decision: str
    notes: str

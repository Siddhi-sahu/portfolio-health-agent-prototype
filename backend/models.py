from pydantic import BaseModel


class Loan(BaseModel):
    clientName: str
    daysLate: int
    loanAmount: float
    missedPayments: int
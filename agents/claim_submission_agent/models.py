from concurrent.futures import thread
from pickle import TRUE
from sqlalchemy import Column, Integer, String
from database import Base

"""
Traditional RCM
=================

Eligibility → Prior-auth approval → Clinical documentation → 
Medical coding → Claims scrubbing → Claims submission → 
Remittance tracking → Denial management → Claims resubmission → Remittance tracking → Reconciliation.
"""

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    user_type = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, index=True, nullable=False)
    thread_id = Column(String, index=True, nullable=False)
    patient_id = Column(String, index=True, nullable=True)
    workflow_type = Column(String, index=True, nullable=False)
    current_step = Column(String, nullable=True)
    status = Column(String, index=True, nullable=False)
    result = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

class Claim(Base):
    __tablename__ = "claims"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True, nullable=False)
    claim_data = Column(String, nullable=False)
    status = Column(String, index=True, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    workflow_run_id = Column(Integer, nullable=False)

class EligibilityCheck(Base):
    __tablename__ = "eligibility_checks"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True, nullable=False)
    insurance_id = Column(String, nullable=False)
    plan = Column(String, nullable=False)
    copay = Column(String, nullable=False)
    eligible = Column(String, index=True, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    workflow_run_id = Column(Integer, nullable=False)

class PriorAuth(Base):
    __tablename__ = "prior_auths"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True, nullable=False)
    procedure_code = Column(String, nullable=False)
    auth_number = Column(String, nullable=False)
    status = Column(String, index=True, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    workflow_run_id = Column(Integer, nullable=False)

class Denial(Base):
    __tablename__ = "denials"
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, index=True, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    workflow_run_id = Column(Integer, nullable=False)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, nullable=False)
    amount = Column(String, nullable=False)
    status = Column(String, index=True, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    workflow_run_id = Column(Integer, nullable=False)

class Reconciliation(Base):
    __tablename__ = "reconciliations"
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, nullable=False)
    payment_id = Column(Integer, nullable=False)
    status = Column(String, index=True, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    workflow_run_id = Column(Integer, nullable=False)
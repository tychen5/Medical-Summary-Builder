from __future__ import annotations

import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ClaimantProfile(BaseModel):
    """Structured claimant attributes extracted from the case file."""

    claimant_name: Optional[str] = Field(default=None)
    ssn: Optional[str] = Field(default=None)
    date_of_birth: Optional[datetime.date] = Field(default=None)
    alleged_onset_date: Optional[datetime.date] = Field(default=None)
    date_last_insured: Optional[datetime.date] = Field(default=None)
    age_at_aod: Optional[int] = Field(default=None)
    current_age: Optional[int] = Field(default=None)
    education: Optional[str] = Field(default=None)
    claim_title: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)


class MedicalEvent(BaseModel):
    """Event row for the timeline table."""

    date: Optional[datetime.date] = Field(default=None)
    provider: Optional[str] = Field(default=None)
    reason: Optional[str] = Field(default=None)
    reference: Optional[str] = Field(default=None, description="Source reference such as page 12/504")


class CustomTableInstruction(BaseModel):
    """User-provided instructions for bespoke table layouts."""

    instruction_text: str
    columns: List[str] = Field(default_factory=list)
    examples: Optional[str] = Field(default=None)


class MedicalSummary(BaseModel):
    """Combined data structure for the generated medical summary."""

    profile: ClaimantProfile = Field(default_factory=ClaimantProfile)
    events: List[MedicalEvent] = Field(default_factory=list)
    custom_tables: dict[str, list[dict[str, str]]] = Field(default_factory=dict)

from __future__ import annotations

from pydantic import BaseModel

from datetime import datetime
from typing import List, Optional


class DateObserved(BaseModel):
    type: str
    value: datetime


class Payload(BaseModel):
    victimid: str
    incidentid: str
    devicetype: str
    respiratoryrate: Optional[float] = None
    systolicbloodpressure: Optional[float] = None
    diastolicbloodpressure: Optional[float] = None
    temperature: Optional[float] = None
    pulserate: Optional[float] = None
    heartratevariability: Optional[float] = None
    pulseoxymetry: Optional[float] = None
    skinmoisture: Optional[float] = None
    encounterdatetime: datetime


class Model(BaseModel):
    id: str
    type: str
    dateObserved: DateObserved
    payload: Payload

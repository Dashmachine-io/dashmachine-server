from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, conlist

from .file import File
from .activity import ActivityResponse


class UserCreate(BaseModel):
    phone: str
    password: str
    birthday: datetime


class GenderOptions(str, Enum):
    male = "Male"
    female = "Female"
    non_binary = "Non-Binary"


class PronounOptions(str, Enum):
    she = "she"
    her = "her"
    hers = "hers"
    he = "he"
    him = "him"
    his = "his"
    they = "they"
    them = "them"
    theirs = "theirs"
    ve = "ve"
    ver = "ver"
    vis = "vis"
    ze = "ze"
    hir = "hir"
    hirs = "hirs"
    other = "other"


class Pronoun(BaseModel):
    name: PronounOptions

    class Config:
        orm_mode = True


class RelationshipStatusOptions(str, Enum):
    single = "Single"
    married = "Married"
    in_relationship = "In a relationship"
    in_open_relationship = "In an open relationship"
    casually_dating = "Casually dating"


class SexualityOptions(str, Enum):
    straight = "Straight"
    gay = "Gay"
    lesbian = "Lesbian"
    bisexual = "Bisexual"
    fluid = "Fluid"
    pansexual = "Pansexual"
    queer = "Queer"
    other = "Other"


class EthnicityOptions(str, Enum):
    american_indian = "American Indian"
    black = "Black/African Decent"
    east_asian = "East Asian"
    hispanic = "Hispanic/Latino"
    middle_eastern = "Middle Eastern"
    pacific_islander = "Pacific Islander"
    southeast_asian = "Southeast Asian"
    white = "White/Caucasian"
    other = "Other"


class UserBase(BaseModel):
    phone: Optional[str]
    birthday: Optional[datetime]
    first_name: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    username: Optional[str]
    bio: Optional[str]
    gender: Optional[GenderOptions]
    relationship_status: Optional[RelationshipStatusOptions]
    sexuality: Optional[SexualityOptions]
    ethnicity: Optional[EthnicityOptions]
    job_title: Optional[str]

    gender_hidden: Optional[bool]
    relationship_status_hidden: Optional[bool]
    sexuality_hidden: Optional[bool]
    ethnicity_hidden: Optional[bool]
    job_title_hidden: Optional[bool]
    pronouns_hidden: Optional[bool]

    age_min: Optional[int]
    age_max: Optional[int]

    auto_detect_location: Optional[bool]
    location: Optional[List[float]]
    lat: Optional[float]
    lng: Optional[float]
    city: Optional[str]
    state: Optional[str]
    radius: Optional[int]

    schedule_notes: Optional[str]
    schedule_mon: Optional[str]
    schedule_tues: Optional[str]
    schedule_wed: Optional[str]
    schedule_thurs: Optional[str]
    schedule_fri: Optional[str]
    schedule_sat: Optional[str]
    schedule_sun: Optional[str]


class UserResponse(UserBase):
    id: str
    pronouns: Optional[conlist(Pronoun, min_items=0, max_items=4)]
    activities: Optional[List[ActivityResponse]]
    profile_complete: bool
    files_sorted: List[File]
    main_image: Optional[File]

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    password: Optional[str]
    pronouns: Optional[conlist(PronounOptions, min_items=1, max_items=4)]


class Token(BaseModel):
    access_token: str
    token_type: str


class CheckPhoneResponses(str, Enum):
    login = "login"
    register = "register"


class CheckPhoneResponse(BaseModel):
    message: CheckPhoneResponses

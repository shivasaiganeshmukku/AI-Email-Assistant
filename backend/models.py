
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Email(BaseModel):
    sender: str = Field(min_length=1, max_length=254)
    recipient: str = Field(min_length=1, max_length=254)
    subject: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=20000)

    @field_validator("sender", "recipient", "subject", "body")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty or whitespace only.")

        return value



class EmailCategory(str, Enum):
    WORK = "Work"
    PERSONAL = "Personal"
    FINANCE = "Finance"
    MEETING = "Meeting"
    SUPPORT = "Support"
    OTHER = "Other"


class EmailPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class ReplyTone(str, Enum):
    PROFESSIONAL = "Professional"
    FRIENDLY = "Friendly"
    CONCISE = "Concise"



class EmailStatus(str, Enum):
    ACTION_REQUIRED = "Action Required"
    REPLY_NEEDED = "Reply Needed"
    AWAITING_RESPONSE = "Awaiting Response"
    INFORMATIONAL = "Informational"
    NO_ACTION_NEEDED = "No Action Needed"
    UNCLEAR = "Unclear"


class EmailAnalysis(BaseModel):
    summary: str
    category: EmailCategory
    priority: EmailPriority
    action_required: bool
    email_status: EmailStatus
    deadline: str | None = None
    recommended_action: str



class EmailClassification(BaseModel):
    category: EmailCategory


class ActionItem(BaseModel):
    task: str
    deadline: str | None = None
    assignee: str | None = None


class ActionItemsResponse(BaseModel):
    action_items: list[ActionItem]


class EmailReplyRequest(BaseModel):
    email: Email
    tone: ReplyTone = ReplyTone.PROFESSIONAL


class EmailReplyResponse(BaseModel):
    subject: str
    body: str
    tone: ReplyTone

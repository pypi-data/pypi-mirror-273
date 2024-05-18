from enum import StrEnum
from typing import Any

import iso639
from pydantic import BaseModel, Field


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class ProjectConfigKey(StrEnum):
    BOTSERVICE_APP_ID = "botservice_app_id"
    BOTSERVICE_APP_PASSWORD = (
        "botservice_app_pwd"  # pragma: allowlist secret # noqa S105
    )
    BOTSERVICE_SECRET = "botservice_secret"  # pragma: allowlist secret # noqa S105
    WELCOME_MESSAGE = "welcome_message"
    # TODO: eventually add the model configuration parameters here


class Plan(StrEnum):
    FREE = "Free"
    BASIC = "Basic"
    PREMIUM = "Premium"
    ENTERPRISE = "Enterprise"


class IsoLanguage(StrEnum):
    GERMAN = iso639.Language.from_part1("de").part1  # German
    ENGLISH = iso639.Language.from_part1("en").part1  # English


class LLM(StrEnum):
    OPENAI = "OpenAI"
    GOOGLE = "Google"
    ANTHROPIC = "Anthropic"


class RetrieverType(StrEnum):
    DEFAULT = "default"
    MULTIQUERY = "multiquery"
    COMPRESSION = "compression"


class SearchType(StrEnum):
    MMR = "mmr"
    SIMILARITY = "similarity"


class DistanceStrategy(StrEnum):
    """Enumerator of the Distance strategies."""

    EUCLIDEAN = "l2"
    COSINE = "cosine"
    MAX_INNER_PRODUCT = "inner"


class User(BaseModel):
    id: int = Field(default=0)
    api_key: str = Field(default="")
    name: str
    company: str
    contact: str | None = None
    plan: Plan = Field(default=Plan.BASIC)
    active: bool = Field(default=True)


class ProjectDocument(BaseModel):
    project_id: int
    id: int
    name: str
    hash: str


class Project(BaseModel):
    id: int
    name: str
    language: IsoLanguage = Field(default=IsoLanguage.GERMAN)
    llm: LLM = Field(default=LLM.OPENAI)
    prompt: str | None = None

    number_of_documents: int = 0
    storage_size: int = 0

    documents: list[ProjectDocument] = []
    configuration: dict[str, str] = {}


class SourceDocument(BaseModel):
    page: str
    content: str
    source: str
    title: str


class AskResponse(BaseModel):
    question: str
    answer: str
    source_paragraphs: list[str]
    source_documents: list[SourceDocument]


class Retriever(StrEnum):
    default = "default"
    multiquery = "multiquery"
    compression = "compression"


class RetrievedDocument(BaseModel):
    content: str
    metadata: dict[str, Any]

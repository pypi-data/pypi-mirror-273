from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Union, Optional, Any, List
from enum import Enum
from datetime import datetime

PrimitiveType = Union[str, int, float, bool]


class RequestBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class HaystackVersion(BaseModel):
    hs_version: str


class Usage(BaseModel):
    total_tokens: int
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None


class Meta(BaseModel):
    models: List[str]
    usage: Usage
    index: Optional[int] = None
    finish_reason: Optional[str] = None


class Writer(BaseModel):
    documents_written: int


class FilterRequest(BaseModel):
    filters: Optional[Dict[str, Any]] = {}


class FilterDocStoreResponse(BaseModel):
    id: str
    content: Optional[str] = None
    dataframe: Optional[Union[str, Any]] = None
    blob: Optional[Union[str, Any]] = None
    meta: Dict[str, Any]
    score: Optional[float] = None
    embedding: Union[List[float], Optional[str]] = None


class DocTokenCounter(BaseModel):
    meta: Meta


class UploadFileResponse(RequestBaseModel):
    DocTokenCounter: DocTokenCounter
    Writter: Writer


class DocumentQueryResponse(BaseModel):
    id: str
    content: str
    dataframe: Optional[Union[str, Any]] = None
    blob: Optional[Union[str, Any]] = None
    meta: Dict[str, Any]
    score: Optional[float] = None
    embedding: Union[List[float], Optional[str]] = None


class ChatRole(str, Enum):
    """Enumeration representing the roles within a chat."""

    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    FUNCTION = "function"


class ChatMessage(BaseModel):
    content: str
    role: ChatRole
    name: Optional[str]
    meta: Dict[str, Any]


class Answer(BaseModel):
    data: ChatMessage
    query: str
    documents: List[DocumentQueryResponse]
    meta: Meta


class AnswerBuilder(BaseModel):
    answers: List[Answer]


class QueryRequest(RequestBaseModel):
    query: str
    chat_history: Optional[List[ChatMessage]] = None
    stream: bool = False
    params: Optional[dict] = None
    debug: Optional[bool] = False


class QueryResponse(RequestBaseModel):
    AnswerBuilder: AnswerBuilder


class GetFileS3Reponse(RequestBaseModel):
    url: str


class DeleteDocResponse(RequestBaseModel):
    n_deleted_documents: int
    n_deleted_s3: int
    deleted_s3_keys: List[str]


class RetrievedDoc(RequestBaseModel):
    original_file_name: str
    doc_id: str
    text: str
    score: float


class EsrTicket(BaseModel):
    company_or_client_name: str
    ticket_category: str
    command_number: str
    serial_number: str
    my_portal_account: str


class UsageJSON(BaseModel):
    input_tokens: int
    output_tokens: int


class MetaJSON(BaseModel):
    id: Optional[str] = None
    model: Optional[str] = None
    usage: Optional[UsageJSON] = None
    stop_reason: Optional[str] = None
    stop_sequence: Optional[str] = None


class ValidatedItem(BaseModel):
    content: str
    role: str = "assistant"
    name: Optional[str] = None
    meta: MetaJSON


class SchemaValidator(BaseModel):
    validated: Optional[List[ValidatedItem]] = None
    validation_error: Optional[List] = None


class DataExtractRequest(BaseModel):
    email_content: str


class DataExtractResponse(BaseModel):
    schema_validator: SchemaValidator


class CPUUsage(BaseModel):
    used: float = Field(..., description="REST API average CPU usage in percentage")

    @field_validator("used")
    @classmethod
    def used_check(cls, v):
        return round(v, 2)


class MemoryUsage(BaseModel):
    used: float = Field(..., description="REST API used memory in percentage")

    @field_validator("used")
    @classmethod
    def used_check(cls, v):
        return round(v, 2)


class GPUUsage(BaseModel):
    kernel_usage: float = Field(..., description="GPU kernel usage in percentage")
    memory_total: int = Field(..., description="Total GPU memory in megabytes")
    memory_used: Optional[int] = Field(
        ..., description="REST API used GPU memory in megabytes"
    )

    @field_validator("kernel_usage")
    @classmethod
    def kernel_usage_check(cls, v):
        return round(v, 2)


class GPUInfo(BaseModel):
    index: int = Field(..., description="GPU index")
    usage: GPUUsage = Field(..., description="GPU usage details")


class HealthResponse(BaseModel):
    version: str = Field(..., description="Haystack version")
    cpu: CPUUsage = Field(..., description="CPU usage details")
    memory: MemoryUsage = Field(..., description="Memory usage details")
    gpus: List[GPUInfo] = Field(default_factory=list, description="GPU usage details")


class StatusEnum(str, Enum):
    completed = "completed"
    processing = "processing"
    failed = "failed"


class IndexingResponse(BaseModel):
    message: str
    s3_keys: List[str]
    group_id: str


class IndexingTask(BaseModel):
    group_id: str
    job_queue_uuid: Union[str, None]
    description: Union[str, None]
    timestamp: datetime
    type: str
    id: int
    name: Union[str, None]
    status: StatusEnum
    s3_key: str
    time_taken: Union[float, None]

class DocInfos(BaseModel):
    filename: str
    group_id: str
    document_date: Union[datetime, None]
    keywords: Union[List[str], None]
    n_chunks: int
    embedding_model: str
    indexation_timestamp: datetime
    is_deleted: bool
    content_type: str
    s3_key: str
    pythia_document_category: Union[str, None]
    language: Union[str, None]
    file_meta: dict
    total_tokens: int
    task_id: int

class PredictIntentResponse(BaseModel):
    intent: str


class AddIntentResponse(BaseModel):
    Writter: Writer


class DeleteIntentResponse(BaseModel):
    deleted_intent: str
    n_deleted_intent_data: int

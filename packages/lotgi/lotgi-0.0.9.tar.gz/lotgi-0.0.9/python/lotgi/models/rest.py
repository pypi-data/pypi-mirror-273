from pydantic import BaseModel, Field, model_validator, Extra
from typing import Optional
import shortuuid

uuid_generator = shortuuid.ShortUUID(alphabet="abcdefghijklmnopqrstuvwxyz1234567890")

class ModalCredentials(BaseModel):
    token_id : str
    token_secret : str

class RunpodCredentials(BaseModel):
    api_key : str

class CloudCredentials(BaseModel):
    modal_credentials : Optional[ModalCredentials] = None
    runpod_credentials : Optional[RunpodCredentials] = None

    @model_validator(mode="after")
    def atleast_one_credential(self):
        if not (self.modal_credentials or self.runpod_credentials):
            raise ValueError("At least one set of credentials should be specified.")
        return self

class JobSpec(BaseModel):
    job_id : str = Field(default_factory=lambda : f"job-{uuid_generator.uuid()}")
    name : str
    cloud_credentials : Optional[CloudCredentials] = None
    input_file : str
    target_duration : Optional[int] # Duration in s -1 for Cheapest
    huggingface_token : Optional[str] = None

class JobStatus(BaseModel, extra=Extra.allow):
    job_id : str
    name : str
    state : str
    submission_time : int
    input_file : str
    target_duration : int # -1 for Cheapest

class JobExecutionOptionsInput(BaseModel):
    input_token_count : int
    num_requests : int
    model : str

class JobExecutionTradeoffOption(BaseModel):
    option_name : str
    expected_cost : float
    expected_duration : int # In seconds

class MetricInput(BaseModel):
    job_id: str
    metric_name: str
    metric_value: float


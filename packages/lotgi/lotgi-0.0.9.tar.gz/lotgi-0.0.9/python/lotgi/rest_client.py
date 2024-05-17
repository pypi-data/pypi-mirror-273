from lotgi.models import rest

import logging
import requests
from typing import List, Optional
import os
import tomli
import functools

logger = logging.getLogger(__name__)

@functools.cache
def get_cloud_credentials():
    modal_credentials = None
    try:
        modal = tomli.load(open(f"{os.environ.get('HOME', '')}/.modal.toml", "rb"))
        modal_credentials = rest.ModalCredentials(
            **modal["default"]
        )
    except Exception as e:
        logger.warning(f"Couldn't read modal credentials. {e}")

    runpod_credentials = None
    try:
        runpod_credentials = rest.RunpodCredentials(
            api_key=os.environ["RUNPOD_API_KEY"]
        )
    except Exception as e:
        logger.warning(f"Couldn't read runpod credentials. {e}")

    return rest.CloudCredentials(
        modal_credentials=modal_credentials,
        runpod_credentials=runpod_credentials
    )

def get_huggingface_credentials():
    try:
        home_dir = os.environ["HOME"]
        with open(f"{home_dir}/.cache/huggingface/token", "r") as f:
            token = f.read()
            return token.strip()
    except Exception as e:
        logger.warning(f"Didn't detect huggingface credentials. Only public models with work. Run `huggingface-cli login` to set your huggingface credentials. {e}")

class RestClient:
    def __init__(self):
        """
        """
        self.endpoint = os.environ.get("LOTGI_ENDPOINT", "https://lotgi.ai/api")
        # TODO: User should specify some secret token not user id, duh.
        if "LOTGI_TOKEN" not in os.environ:
            raise KeyError(f"LOTGI_TOKEN not set.")

        self._token = os.environ["LOTGI_TOKEN"]

        self.headers = {
            "lotgi-token": self._token,
            "Content-type": "application/json",
        }

    def submit_job(self, *,
                   name : str,
                   input_file : str,
                   target_duration : int,
                   _autodetect_cloud_credentials : bool = False
                   ) -> rest.JobStatus:
        url = f"{self.endpoint}/create_job"

        if _autodetect_cloud_credentials:
            cloud_credentials = get_cloud_credentials()
        else:
            cloud_credentials = None


        if _autodetect_cloud_credentials:
            huggingface_token = get_huggingface_credentials()
        else:
            huggingface_token = ""

        job_spec = rest.JobSpec(
            cloud_credentials=cloud_credentials,
            input_file=input_file,
            name=name,
            target_duration=target_duration,
            huggingface_token=huggingface_token,
        )

        body = job_spec.dict()

        result = requests.post(url, headers=self.headers, json=body)

        if result.status_code == 401:
            raise PermissionError(f"Request authentication failed. Is your `LOTGI_TOKEN` environment variable set correctly? {result.status_code} : {result.json()['detail']}")

        if not result.ok:
            raise RuntimeError(f"Request was not successfully submitted. {result.status_code}: {result.text}")

        return rest.JobStatus.validate(result.json())

    def job_exection_options(self, *, job_execution_options_input : rest.JobExecutionOptionsInput) -> List[rest.JobExecutionTradeoffOption]:
        url = f"{self.endpoint}/job_execution_options"

        result = requests.get(url, headers=self.headers, json=job_execution_options_input.dict())

        if not result.ok:
            raise RuntimeError(f"Request was not successfully submitted. {result.status_code}: {result.text}")

        return [
            rest.JobExecutionTradeoffOption.parse_obj(result.json()[i])
            for i in range(len(result.json()))
        ]


    def list_jobs(self) -> List[rest.JobStatus]:
        url = f"{self.endpoint}/list_jobs"
        result = requests.get(url, headers=self.headers)

        if result.status_code == 401:
            raise PermissionError(f"Request authentication failed. Is your `LOTGI_TOKEN` environment variable set correctly? {result.status_code} : {result.json()['detail']}")

        if not result.ok:
            raise RuntimeError(f"Request was not successfully submitted. {result.status_code}: {result.text}")

        return [
            rest.JobStatus.validate(status)
            for status in result.json()
        ]

    def get_job_results(self, job_id : str) -> str:
        url = f"{self.endpoint}/get_job_results"
        result = requests.get(url, headers=self.headers, params={"job_id": job_id})

        if result.status_code == 401:
            raise PermissionError(f"Request authentication failed. Is your `LOTGI_TOKEN` environment variable set correctly? {result.status_code} : {result.json()['detail']}")

        if result.status_code == 404:
            raise KeyError(f"Job doesn't exist! {result.text}")

        if not result.ok:
            raise RuntimeError(f"Request was not successfully submitted. {result.status_code}: {result.text}")
        return result.json()

    def get_upload_url(self, filename : str) -> str:
        url = f"{self.endpoint}/get_upload_url"
        result = requests.get(url, headers=self.headers, params={"filename": filename})

        if result.status_code == 401:
            raise PermissionError(f"Request authentication failed. Is your `LOTGI_TOKEN` environment variable set correctly? {result.status_code} : {result.json()['detail']}")

        if not result.ok:
            raise RuntimeError(f"Request was not successfully submitted. {result.status_code}: {result.text}")
        return result.json()

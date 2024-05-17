import aiohttp
from typing import Any, Dict, Optional
from lotgi.models import rest


class RestClient(aiohttp.ClientSession):
    def __init__(self, base_url : Optional[str] = None, **kwargs : Dict[str, Any]):
        if base_url is None:
            base_url = os.environ.get("LOTGI_ENDPOINT", "https://lotgi.ai/api")

        token = os.environ["LOTGI_TOKEN"]
        kwargs.setdefault("headers", {}).update({
            "lotgi-token": token,
            "Content-type": "application/json",
        })
        super(base_url, **kwargs)

    async def submit(self, *
                   model : str,
                   input_file : str,
                   field : str,
                   target_cost : float,
                   target_deadline : int,
                   execution_tradeoff : str,
                   max_output_tokens : Optional[int],
                   regex : Optional[str],
                     _autodetect_cloud_credentials : bool = False,
                    ) -> rest.JobStatus:
        pass

import json
import requests
import traceback
from time import sleep
from .model_config import ModelConfig

__author__ = 'swliu'


def query_llm(model: ModelConfig, query: str, num_retry: int = 3,
              success_sleep: float = 0, fail_sleep: float = 1) -> str:
    for i in range(num_retry):
        try:
            payload = _compute_payload(model=model, query=query)
            headers = _compute_headers(model.access_token)
            response = requests.post(model.api_url, json=payload, headers=headers)
            response_text = response.json()['response']

            if success_sleep > 0:
                sleep(success_sleep)
            return response_text
        except Exception as e:
            print(traceback.format_exc())
            if fail_sleep > 0:
                sleep(fail_sleep)
            continue
    return ""


def query_model_info_api(access_token, url, num_retry: int = 3,
                         success_sleep: float = 1.0, fail_sleep=1.0) -> list:
    """
    :param access_token: API access token.
    :param url: API endpoint
    :param num_retry: int
    :param success_sleep: seconds to delay execution when API call successful (float)
    :param fail_sleep: seconds to delay execution when API call unsuccessful (float)
    :return: a list of large language models that are hosted by ASU
    """
    for i in range(num_retry):
        try:
            headers = _compute_headers(access_token=access_token)
            response = requests.get(url=url, headers=headers)
            models_dict = json.loads(response.content)
            models = models_dict["models"]
            if success_sleep > 0:
                sleep(success_sleep)
            return models
        except Exception as e:
            print(traceback.format_exc())
            if fail_sleep > 0:
                sleep(fail_sleep)
            continue
    return []


def model_provider_mapper(models: list) -> dict:
    mapper = {
        model["name"]: model["provider"]
        for model in models
    }
    return mapper


def model_list(models: list) -> set:
    models = {model["name"] for model in models}
    return models


def _compute_headers(access_token):
    headers = {
        "Accept": "application/json",
        "Authorization": f'Bearer {access_token}'
    }
    return headers


def _compute_payload(model: ModelConfig, query: str):
    payload = {"prompt": query}

    if model.name:
        payload["model_name"] = model.name
    if model.provider:
        payload["model_provider"] = model.provider
    if model.model_params:
        payload["model_params"] = model.model_params
    if model.enable_search:
        payload["enable_search"] = model.enable_search
    if model.search_params:
        payload["search_params"] = model.search_params
    if model.project_id:
        payload["project_id"] = model.project_id

    return payload

import uuid
from dataclasses import dataclass
from datetime import datetime

import httpx
from fastapi import HTTPException
from pydantic import BaseModel, TypeAdapter
from typing_extensions import Any


@dataclass
class MicroserviceOption:
  is_json: bool = True
  headers: dict = None


@dataclass
class ReplaceMicroserviceConfig:
  url: str


class Normailization:
  @staticmethod
  def serialize_uuid_to_str(data: Any = None):
    if data is None:
      return None

    if isinstance(data, dict):
      return {key: Normailization.serialize_uuid_to_str(value) for key, value in data.items()}

    if isinstance(data, list):
      return [Normailization.serialize_uuid_to_str(item) for item in data]

    if isinstance(data, uuid.UUID):
      return str(data)

    return data

  @staticmethod
  def strftime(data):
    if isinstance(data, dict):
      return {key: Normailization.strftime(value) for key, value in data.items()}
    elif isinstance(data, list):
      return [Normailization.strftime(item) for item in data]
    elif isinstance(data, datetime):
      return datetime.strftime(data, '%Y-%m-%d %H:%M:%S')
    else:
      return data

  @staticmethod
  def dump_pydantic_model_value(data):
    if data is None:
      return None

    if isinstance(data, dict):
      return {key: Normailization.dump_pydantic_model_value(value) for key, value in data.items()}

    elif isinstance(data, list):
      return [Normailization.dump_pydantic_model_value(item) for item in data]

    if isinstance(data, BaseModel):
      return data.model_dump()

    return data

  @staticmethod
  def normalize(data: Any):
    data = Normailization.dump_pydantic_model_value(data)
    data = Normailization.serialize_uuid_to_str(data)
    return Normailization.strftime(data)

class BaseMicroserviceClient:
  def filter_none_values(self, query_params: dict | None):
    return {key: value for key, value in query_params.items() if value is not None} if query_params else None

  async def send(
    self, url: str, query_params: dict, body_params: any, response_type: any, option: MicroserviceOption = None
  ):
    if not ReplaceMicroserviceConfig.url:
      raise Exception('Please config microservice url')

    url = ReplaceMicroserviceConfig.url + url
    if not option:
      option = MicroserviceOption()

    async with httpx.AsyncClient() as client:
      response = await client.post(
        url=url,
        headers=option.headers,
        params=self.filter_none_values(query_params),
        data=body_params if not option.is_json else None,
        json=Normailization.normalize(body_params) if option.is_json else None,
      )
      data = response.json()
      if response.status_code < 200 or response.status_code > 299:
        raise HTTPException(status_code=response.status_code, detail=data)
      if not response_type:
        return data

      return TypeAdapter(response_type).validate_python(data)

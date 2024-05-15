from collections import Counter
from typing import Literal
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, Field, validator, ValidationError, Extra

from .exceptions import raise_for_status, SyncClientSetupError, ResponseFormatError
from .clients import SyncClient
from .api_types import Message, Tag


def post_as_json(request_payload: BaseModel, api_method: str) -> httpx.Response:
    """Send a request to the Unisender Go API synchronously using a JSON payload."""
    client = SyncClient.default_client.get(None)

    if not client:
        raise SyncClientSetupError

    http_response = client.session.post(
        urljoin(client.unisender_go_api_root_url, api_method),
        headers={
            'X-API-KEY': client.token,
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        content=request_payload.json(exclude_none=True, by_alias=True).encode('utf-8'),
    )

    raise_for_status(http_response)
    return http_response


class SendRequest(BaseModel):
    """Метод для отправки писем вашим подписчикам.

    При отправке вы можете использовать подстановки переменных, шаблоны, включить отслеживание прочтений или
    переходов по ссылкам и многое другое.

    Оф.документация к методу API: https://godocs.unisender.ru/web-api-ref#email-send .
    """

    message: Message = Field(description='Объект, содержащий все свойства отправляемого сообщения.')

    class Config:
        extra = Extra.forbid
        validate_all = True
        validate_assignment = True

    def send(self) -> 'SendResponse':
        response = post_as_json(self, 'v1/email/send.json')

        with ResponseFormatError.reraise_from(
            ValidationError,
            request=response._request,
            response=response,
        ):
            return SendResponse.parse_raw(response.content)

    @validator('message')
    @classmethod
    def validate_message(cls, v: Message) -> Message:
        emails_counter = Counter(recipient.email for recipient in v.recipients)
        duplicated_emails = [item for item, count in emails_counter.items() if count > 1]
        if duplicated_emails:
            raise ValueError(f'Duplicated emails: {duplicated_emails!r}.')

        emails_number = len(emails_counter)
        if emails_number > 500:
            raise ValueError(f'Emails limit is exceeded {emails_number!r}>500.')

        return v


class SendResponse(BaseModel):
    status: Literal['success']

    job_id: str = Field(
        description='Идентификатор задания по отправке, может оказаться полезным при выяснении причин сбоев.',
    )
    emails: list[str] = Field(
        default_factory=list,
        description='Массив email-адресов, успешно принятых к отправке.',
    )
    tags: list[Tag] = Field(
        default_factory=list,
        description='Незадокументированное в API поле с тегами.',
    )
    failed_emails: dict[str, str] = Field(
        default_factory=dict,
        description='Объект с email-адресами, не принятыми к отправке. '
                    'Email представлен ключом словаря, а статус отправки - значением, '
                    'например: {"email1@gmail.com": "temporary_unavailable"}\n'
                    'Статусы failed_emails описаны в документации к API '
                    'https://godocs.unisender.ru/web-api-ref#email-send',
    )


class ErrorResponse(BaseModel):
    status: Literal['error']
    code: int = Field(
        description='API-код ошибки (не путайте с HTTP-кодом)',
    )
    message: str = Field(
        description='Сообщение об ошибке на английском.',
    )

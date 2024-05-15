# Unisender Go API

Библиотека Unisender Go API упрощает работу с веб API [Unisender Go](https://go.unisender.ru/). Библиотека предоставляет тонкую обёртку над [HTTPX](https://www.python-httpx.org/): она добавляет к обычным возможностям HTTPX свои схемы данных, а также удобные часто используемые функции, но не мешает, при необходимости, спускаться ниже на уровень HTTP-запросов.

[Документация к API Unisender Go](https://godocs.unisender.ru/web-api-ref#authentication).

## Ключевые возможности библиотеки

Ключевые возможности библиотеки Unisender Go API:

- Готовый механизм авторизации
- Поддержка синхронных и асинхронных запросов к API
- Доступ к API из любого места в коде через `contextvars`
- Строгая валидация данных перед отправкой запросов к API
- Строгая валидация данных при получении данных от API
- Наглядные схемы данных для всех типов запросов и ответов к API с цитатами из оф.документации к API
- Подробная отладочная информация по взаимодействию с API
- Возможность добавлять новые API endpoints по мере их появления в Unisender Go прямо из внешнего прикладного кода


## Пример использования

Пример использования синхронного клиента для отправки письма на адрес recepient@example.com:

```python
from unisender_go_api import SyncClient, SendRequest

with SyncClient.setup('place-your-token-here'):
    request = SendRequest(
        message={
            "recipients": [
                {"email": "recepient@example.com"},
            ],
            "body": {
                "html": "<b>Hello, username!</b>",
            },
            "subject": "Greetings to you",
            "from_email": "mailing@dvmn.org",
        },
    )
    request.send()
```


## Известные ограничения

Временные ограничения:

- Из всем методов API реализован только `send`, и то ограничениями:
    - Не поддерживается `recipients[].metadata`
    - Не поддерживается `global_metadata`
    - Не поддерживается `bypass_global`
    - Не поддерживается `bypass_unavailable`
    - Не поддерживается `bypass_unsubscribed`
    - Не поддерживается `bypass_complained`
    - Не поддерживается `headers`
    - Не поддерживается `options`
- Не реализован асинхронный клиент
- Не реализованы shortcuts для упрощённого доступа к API
- Из двух серверов Unisender Go поддерживается только один — https://go1.unisender.ru/ru/transactional/api/


## Исключения

При работе с API библиотека Unisender Go API API выкидывает несколько типов исключений:

- `UnisenderGoError` и его подтипы, см. файл unisender_go_api/exceptions.py
- [`httpx.HTTPError`](https://www.python-httpx.org/exceptions/)
- [`pydantic.ValidationError`](https://docs.pydantic.dev/latest/errors/validation_errors/) — только при подготовке данных исходящего запроса к API, но не при обработке HTTP ответа

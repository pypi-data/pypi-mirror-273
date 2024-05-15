from typing import Literal, Union, Any, cast

from pydantic import (
    BaseModel,
    ConstrainedStr,
    ConstrainedInt,
    EmailStr,
    Field,
    conint,
    constr,
    validator,
    root_validator,
    StrictStr,
    StrictFloat,
    StrictInt,
    StrictBool,
)

IntFlag: ConstrainedInt = conint(ge=0, le=1)


AttachmentType: ConstrainedStr = constr(min_length=1, strip_whitespace=True, to_lower=True)
AttachmentName: ConstrainedStr = constr(min_length=1, strip_whitespace=True)


class Attachment(BaseModel):
    type_: AttachmentType = Field(
        alias='type',
        description='Тип вложения, см. MIME https://en.wikipedia.org/wiki/MIME. '
                    'Если не уверены, используйте "application/octet-stream".',
    )
    name: AttachmentName = Field(
        description='Название вложения в формате: "имя.расширение". При передаче нескольких вложений их названия '
                    'должны быть уникальны. В названии вложений запрещен символ `/`.',
    )
    content: str = Field(
        max_length=9786710,
        description='Содержимое файла в base64 https://en.wikipedia.org/wiki/Base64. Максимальный размер '
                    'файла 7Mб (9786710 байт в base64).',
    )

    class Config:
        allow_population_by_field_name = True

    @validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if '/' in v:
            raise ValueError(f'Symbol `/` is prohibited to use inside attachment name: {v!r}.')

        return v


InlineAttachmentType: ConstrainedStr = constr(min_length=1, strip_whitespace=True, to_lower=True)
InlineAttachmentName: ConstrainedStr = constr(min_length=1, strip_whitespace=True)


class InlineAttachment(BaseModel):
    type_: InlineAttachmentType = Field(
        alias='type',
        description='Тип вложения, см. MIME https://en.wikipedia.org/wiki/MIME. '
                    'Если не уверены, используйте "application/octet-stream".',
    )
    name: InlineAttachmentName = Field(
        description='Идентификатор вложения. Если, например, name="IMAGECID", то для вывода картинки из '
                    'этого вложения в HTML тексте письма надо указать <img src="cid:IMAGECID">.',
    )
    content: str = Field(
        max_length=9786710,
        description='Содержимое файла в base64 https://en.wikipedia.org/wiki/Base64. Максимальный размер '
                    'файла 7Mб (9786710 байт в base64).',
    )

    class Config:
        allow_population_by_field_name = True


SubstitutionName: ConstrainedStr = constr(regex=r'^[a-zA-Z][a-zA-Z0-9\_]*$', strict=True)
SubstitutionValue = Union[StrictStr | StrictFloat | StrictInt | StrictBool | None, 'Substitutions']


class Substitutions(BaseModel):
    __root__: dict[SubstitutionName, SubstitutionValue]


class Recipient(BaseModel):
    email: EmailStr = Field(description='Email-адрес получателя')

    substitutions: Substitutions = Field(
        default_factory=dict,
        description='Объект, описывающий подстановки для конкретного получателя. Например, имя, товар для '
                    'показа именно данному получателю - см. Шаблонизаторы '
                    'https://godocs.unisender.ru/template-engines. Подстановки работают в параметрах: \n'
                    '- body.html\n'
                    '- body.plaintext\n'
                    '- body.amp\n'
                    '- subject\n'
                    '- from_name\n'
                    '- headers["List-Unsubscribe"]\n'
                    '- options.unsubscribe_url\n'
                    'Названия переменных могут содержать буквы латинского алфавита, цифры, символ "_". '
                    'Первым символом может быть только буква, использование пробелов не допускается. '
                    'Есть специальная переменная "to_name", позволяющая задать имя получателя. '
                    'Длина переменной "to_name" ограничена 78 символами. '
                    'При подстановке туда "Имя Фамилия" SMTP-заголовок "To" будет выглядеть как '
                    '"Имя Фамилия <email@example.com>".',
    )

    @validator('substitutions')
    @classmethod
    def validate_to_name_substitution_variable(cls, v: Substitutions) -> Substitutions:
        if 'to_name' not in v.__root__:
            return v

        to_name_value = cast(str, v.__root__['to_name'])

        if len(to_name_value) > 78:
            raise ValueError('Too long to_name value. Should be less than or equal to 78.')

        return v


class EmailBody(BaseModel):
    html: str = ''
    plaintext: str = ''
    amp: str = ''

    @root_validator
    @classmethod
    def validate_content(cls, values: dict[str, Any]) -> dict[str, Any]:
        if not values['html'] and not values['plaintext']:
            raise ValueError(
                'At least one of attributes `html` or `plaintext` should be specified.',
            )

        return values


Tag: ConstrainedStr = constr(max_length=50, min_length=1, strip_whitespace=True)
TemplateId: ConstrainedStr = constr(min_length=1, strip_whitespace=True)


class Message(BaseModel):
    recipients: list[Recipient] = Field(min_items=1)

    template_id: TemplateId | None = Field(
        default=None,
        description='Идентификатор шаблона, созданного ранее методом template/set. Если '
                    'указан, то поля шаблона подставляются вместо пропущенных полей email/send. '
                    'Например, если в email/send не указан body - берётся тело письма из шаблона, '
                    'а если не указан subject - берётся тема из шаблона.',
    )

    tags: list[Tag] = Field(
        default_factory=list,
        max_items=4,
        unique_items=True,
        description='Список уникальных меток, максимум 4 штуки. Метки могут использоваться для '
                    'категоризации писем по выбранным вами критериям. Метки передаются '
                    'при вызове вебхуков и методов event-dump. '
                    'Для каждого аккаунта/проекта разрешено не более 10 000 меток, при превышении '
                    'метод email/send будет возвращать ошибку.',
    )

    skip_unsubscribe: IntFlag = Field(
        default=False,
        description='Пропустить или не пропускать добавление стандартного блока со ссылкой отписки к HTML-части '
                    'письма. Для использования skip_unsubscribe=True вам надо попросить техподдержку включить '
                    'такую возможность.',
    )
    global_language: Literal[
        'be',
        'de',
        'en',
        'es',
        'fr',
        'it',
        'pl',
        'pt',
        'ru',
        'ua',
        'kz',
    ] | None = Field(
        default=None,
        description='Заголовок для выбора языка ссылки и страницы отписки.',
    )

    template_engine: Literal['simple', 'velocity', 'none'] = Field(
        default='simple',
        description='Параметр для выбора шаблонизатора. '
                    'Шаблонизатор `none` доступен только для писем с отключенными `track_links`, '
                    '`track_read` и отключенным блоком отписки.',
    )

    global_substitutions: Substitutions = Field(
        default_factory=dict,
        description='Объект для передачи глобальных подстановок (например, название компании). Если названия '
                    'переменных повторяются в объекте пользовательских подстановок "substitutions", значения '
                    'переменных будут взяты из объекта "substitutions" Подстановки работают в параметрах:\n'
                    '- body.html\n'
                    '- body.plaintext\n'
                    '- body.amp\n'
                    '- subject\n'
                    '- from_name\n'
                    '- options.unsubscribe_url\n'
                    'Названия переменных могут содержать буквы латинского алфавита, цифры, символ "_". '
                    'Первым символом может быть только буква, использование пробелов не допускается.',
    )

    body: EmailBody = Field(
        description='Объект, который содержит в себе html, plaintext и amp части письма. Либо html, либо plaintext '
                    'часть должна присутствовать обязательно.',
    )

    subject: str = Field(
        description='Тема письма.',
    )

    from_email: EmailStr | None = Field(
        default=None,
        description='Email-адрес отправителя. Если значение не указано, то берётся из шаблона.'
                    'Поле обязательно для заполнения только при пустом `template_id`.',
    )
    from_name: str | None = Field(
        default=None,
        description='Имя отправителя. Если значение не указано, то берётся из шаблона.',
    )

    reply_to: EmailStr | None = Field(
        default=None,
        description='Необязательный email-адрес для ответов — на случай, если отличается от адреса отправителя.',
    )
    reply_to_name: str | None = Field(
        default=None,
        description='Необязательное имя для ответов (если указан email reply_to и вы хотите, чтобы отображался '
                    'не только этот email, но и имя).',
    )

    track_links: IntFlag = Field(
        default=True,
        description='Включает/выключает отслеживание переходов по ссылкам.',
    )
    track_read: IntFlag = Field(
        default=True,
        description='Включает/выключает отслеживание прочтений письма.',
    )

    attachments: list[Attachment] = Field(
        default_factory=list,
        description='Вложения к письму',
    )
    inline_attachments: list[InlineAttachment] = Field(
        default_factory=list,
        description='Inline-вложения к письму, например, для включения изображений в письмо вместо '
                    'загрузки их по ссылке.',
    )

    @root_validator
    @classmethod
    def validate_template_engine(cls, values: dict[str, Any]) -> dict[str, Any]:
        none_template_allowed = all([
            not values['track_links'],
            not values['track_read'],
            values['skip_unsubscribe'],
        ])

        if values['template_engine'] == 'none' and not none_template_allowed:
            raise ValueError(
                'Template engine `none` requires options `track_links`, `track_read`'
                'be disabled and option `skip_unsubscribe` be enabled.',
            )

        return values

    @root_validator()
    @classmethod
    def validate_required_tags_if_template_not_specified(cls, values: dict[str, Any]) -> dict[str, Any]:
        if 'template_id' in values:
            return values

        if not values['from_email']:
            raise ValueError('Value `from_email` is required because of empty `template_id`.')

        return values

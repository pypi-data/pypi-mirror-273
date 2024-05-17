import os
from datetime import datetime
from typing import Any, Callable, Type, TypedDict, TypeVar

import fuzzy_json
import openai
import pydantic
from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI, OpenAI

from .exceptions import CompletionIncompleteError
from .utils import signature

T = TypeVar("T", bound=pydantic.BaseModel)


class Message(TypedDict):
    role: str
    content: str


class FunctionMessage(Message):
    name: str


def infer_api_type() -> str | None:
    """
    Infers the API type based on environment variables and sets the api_type attribute accordingly.

    Raises:
        ValueError: If the API type cannot be determined.
    """
    if os.environ.get("OPENAI_API_KEY"):
        return "open_ai"
    elif os.environ.get("AZURE_OPENAI_API_KEY"):
        return "azure"
    else:
        return openai.api_type


class APISettings(pydantic.BaseModel):
    api_key: str = pydantic.Field(default_factory=lambda: openai.api_key)
    api_base: str = pydantic.Field(default_factory=lambda: openai.azure_endpoint)
    api_version: str | None = pydantic.Field(default_factory=lambda: openai.api_version)
    api_type: str | None = pydantic.Field(default_factory=infer_api_type)

    def check_functions_required(self) -> bool:
        if self.api_version is None:
            assert self.api_type != "azure", "api_version is required for azure"
            return False
        if self.api_type == "azure" and datetime.strptime(str(self.api_version)[:10], "%Y-%m-%d") >= datetime(2023, 12, 1):
            return False
        return True


def get_sync_client(model: str, api_settings: APISettings = APISettings()) -> OpenAI:
    if api_settings.api_type == "open_ai":
        return OpenAI(api_key=api_settings.api_key)
    elif api_settings.api_type == "azure":
        return AzureOpenAI(
            azure_endpoint=api_settings.api_base,
            api_key=api_settings.api_key,
            api_version=api_settings.api_version,
            azure_deployment=model,
        )

    raise ValueError(f"Unknown api_type {api_settings.api_type}")


def get_async_client(model: str, api_settings: APISettings = APISettings()) -> AsyncOpenAI:
    if api_settings.api_type == "open_ai":
        return AsyncOpenAI(api_key=api_settings.api_key)
    elif api_settings.api_type == "azure":
        return AsyncAzureOpenAI(
            azure_endpoint=api_settings.api_base,
            api_key=api_settings.api_key,
            api_version=api_settings.api_version,
            azure_deployment=model,
        )
    raise ValueError(f"Unknown api_type {api_settings.api_type}")


"""
The currently applied Azure OpenAI API version is 2023-07-01-preview,
which is about to expire on July, 1,
and the parameters `functions` and `function_call` have been deprecated for the OpenAI API
and since the 2023-12-01-preview version for the Azure OpenAI API version.
Therefore, the Azure OpenAI API version should be upgraded to either 2023-10-01-preview or versions later than and excluding 2023-12-01-preview.
The parameters should also be updated to `tools` and `tool_choice` for OpenAI API and Azure OpenAI API with version starting from 2023-12-01-preview.
"""


def function_completion(
    messages: list[Message],
    max_tokens: int | None = None,
    model: str = "gpt-3.5-turbo-0613",
    temperature: float = 1.0,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop: list[str] = [],
    user: str = "",
    functions: list[Callable[..., Any]] = [],
    function_call: str | dict[str, Any] = "auto",
    api_settings: APISettings = APISettings(),
) -> dict[str, Any] | None:
    assert functions, "functions must be a non-empty list of functions"

    kwargs: dict[str, Any] = dict(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        user=user,
        stop=stop or None,
    )
    client: OpenAI = get_sync_client(model, api_settings)

    functions_are_required = api_settings.check_functions_required()

    kwargs_ = dict(tools=[{"type": "function", "function": signature.FunctionSignature(f).schema()} for f in functions], tool_choice={"type": "function", "function": function_call} if type(function_call) != str else function_call)

    if functions_are_required:
        kwargs_ = dict(functions=[signature.FunctionSignature(f).schema() for f in functions], function_call=function_call)

    kwargs.update(kwargs_)

    if max_tokens is not None:
        kwargs.update(max_tokens=max_tokens)

    response = client.chat.completions.create(**kwargs)

    output = response.choices[0]
    message = output.message
    finish_reason = output.finish_reason

    if functions_are_required and message.function_call is not None and finish_reason in ["stop", "function_call"]:
        return message.function_call

    elif message.tool_calls is not None and finish_reason in ["stop", "tool_calls"]:
        return message.tool_calls[0].function

    raise CompletionIncompleteError(
        f"Incomplete response. Max tokens: {max_tokens}, Finish reason: {finish_reason} Message:{message.content}",
        response=response,
        request=kwargs,
    )


async def afunction_completion(
    messages: list[Message],
    max_tokens: int | None = None,
    model: str = "gpt-3.5-turbo-0613",
    temperature: float = 1.0,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop: list[str] = [],
    user: str = "",
    functions: list[Callable[..., Any]] = [],
    function_call: str | dict[str, Any] = "auto",
    api_settings: APISettings = APISettings(),
) -> dict[str, Any] | None:
    assert functions, "functions must be a non-empty list of functions"

    kwargs: dict[str, Any] = dict(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        user=user,
        stop=stop or None,
    )
    client: AsyncOpenAI = get_async_client(model, api_settings)

    functions_are_required = api_settings.check_functions_required()

    kwargs_ = dict(tools=[{"type": "function", "function": signature.FunctionSignature(f).schema()} for f in functions], tool_choice={"type": "function", "function": function_call} if type(function_call) != str else function_call)

    if functions_are_required:
        kwargs_ = dict(functions=[signature.FunctionSignature(f).schema() for f in functions], function_call=function_call)

    kwargs.update(kwargs_)

    if max_tokens is not None:
        kwargs.update(max_tokens=max_tokens)

    response = await client.chat.completions.create(**kwargs)
    output = response.choices[0]
    message = output.message
    finish_reason = output.finish_reason

    if functions_are_required and message.function_call is not None and finish_reason in ["stop", "function_call"]:
        return message.function_call

    elif message.tool_calls is not None and finish_reason in ["stop", "tool_calls"]:
        return message.tool_calls[0].function

    raise CompletionIncompleteError(
        f"Incomplete response. Max tokens: {max_tokens}, Finish reason: {finish_reason} Message:{message.content}",
        response=response,
        request=kwargs,
    )


def structural_completion(
    structure: Type[T],
    messages: list[Message],
    max_tokens: int | None = None,
    model: str = "gpt-3.5-turbo-0613",
    temperature: float = 1.0,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    user: str = "",
    auto_repair: bool = True,
    api_settings: APISettings = APISettings(),
) -> T:

    kwargs: dict[str, Any] = dict(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        user=user,
    )
    client: OpenAI = get_sync_client(model, api_settings)

    functions_are_required = api_settings.check_functions_required()

    function_call = {"name": "structural_response"}
    function = function_call | {
        "description": "Response to user in a structural way.",
        "parameters": structure.schema(),
    }

    kwargs_ = dict(
        tools=[{"type": "function", "function": function}],
        tool_choice={"type": "function", "function": function_call},
    )

    if functions_are_required:
        kwargs_ = dict(
            functions=[function],
            function_call=function_call,
        )
    kwargs.update(kwargs_)

    if max_tokens is not None:
        kwargs.update(max_tokens=max_tokens)

    response = client.chat.completions.create(**kwargs)

    output = response.choices[0]
    message = output.message
    finish_reason = output.finish_reason

    if finish_reason == "stop":
        if functions_are_required and message.function_call is not None:
            args = message.function_call.arguments
        elif message.tool_calls is not None:
            args = message.tool_calls[0].function.arguments

        parsed_json = fuzzy_json.loads(args, auto_repair)
        return pydantic.parse_obj_as(structure, parsed_json)

    raise CompletionIncompleteError(
        f"Incomplete response. Max tokens: {max_tokens}, Finish reason: {finish_reason} Message:{message.content}",
        response=response,
        request=kwargs,
    )


async def astructural_completion(
    structure: Type[T],
    messages: list[Message],
    max_tokens: int | None = None,
    model: str = "gpt-3.5-turbo-0613",
    temperature: float = 1.0,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    user: str = "",
    auto_repair: bool = True,
    api_settings: APISettings = APISettings(),
) -> T:

    kwargs: dict[str, Any] = dict(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        user=user,
    )
    client: AsyncOpenAI = get_async_client(model, api_settings)

    functions_are_required = api_settings.check_functions_required()

    function_call = {"name": "structural_response"}
    function = function_call | {
        "description": "Response to user in a structural way.",
        "parameters": structure.schema(),
    }

    kwargs_ = dict(
        tools=[{"type": "function", "function": function}],
        tool_choice={"type": "function", "function": function_call},
    )

    if functions_are_required:
        kwargs_ = dict(
            functions=[function],
            function_call=function_call,
        )
    kwargs.update(kwargs_)

    if max_tokens is not None:
        kwargs.update(max_tokens=max_tokens)

    response = await client.chat.completions.create(**kwargs)

    output = response.choices[0]
    message = output.message
    finish_reason = output.finish_reason

    if finish_reason == "stop":
        if functions_are_required and message.function_call is not None:
            args = message.function_call.arguments
        elif message.tool_calls is not None:
            args = message.tool_calls[0].function.arguments

        parsed_json = fuzzy_json.loads(args, auto_repair)
        return pydantic.parse_obj_as(structure, parsed_json)

    raise CompletionIncompleteError(
        f"Incomplete response. Max tokens: {max_tokens}, Finish reason: {finish_reason} Message:{message.content}",
        response=response,
        request=kwargs,
    )


def chat_completion(
    messages: list[Message],
    max_tokens: int | None = None,
    model: str = "gpt-3.5-turbo",
    temperature: float = 1.0,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop: list[str] = [],
    user: str = "",
    api_settings: APISettings = APISettings(),
) -> str:

    kwargs: dict[str, Any] = dict(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        user=user,
        stop=stop or None,
    )

    client: OpenAI = get_sync_client(model, api_settings)

    if max_tokens is not None:
        kwargs.update(max_tokens=max_tokens)

    response = client.chat.completions.create(**kwargs)

    output = response.choices[0]
    output_message = output.message.content.strip()

    if output.finish_reason != "stop":
        raise CompletionIncompleteError(
            f"Incomplete response. Max tokens: {max_tokens}, Finish reason: {output.finish_reason}",
            response=response,
            request=kwargs,
        )

    return output_message


async def achat_completion(
    messages: list[Message],
    max_tokens: int | None = None,
    model: str = "gpt-3.5-turbo",
    temperature: float = 1.0,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop: list[str] = [],
    user: str = "",
    api_settings: APISettings = APISettings(),
) -> str:

    kwargs: dict[str, Any] = dict(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        user=user,
        stop=stop or None,
    )

    client: AsyncOpenAI = get_async_client(model, api_settings)

    if max_tokens is not None:
        kwargs.update(max_tokens=max_tokens)

    response = await client.chat.completions.create(**kwargs)

    output = response.choices[0]
    output_message = output.message.content.strip()

    if output.finish_reason != "stop":
        raise CompletionIncompleteError(
            f"Incomplete response. Max tokens: {max_tokens}, Finish reason: {output.finish_reason}",
            response=response,
            request=kwargs,
        )

    return output_message

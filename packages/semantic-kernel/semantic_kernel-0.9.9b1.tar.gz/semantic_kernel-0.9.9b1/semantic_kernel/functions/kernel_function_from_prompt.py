# Copyright (c) Microsoft. All rights reserved.
from __future__ import annotations

import logging
import os
from html import unescape
from typing import TYPE_CHECKING, Any, AsyncGenerator

import yaml
from pydantic import Field, ValidationError, model_validator

from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.connectors.ai.text_completion_client_base import TextCompletionClientBase
from semantic_kernel.const import METADATA_EXCEPTION_KEY
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.streaming_chat_message_content import StreamingChatMessageContent
from semantic_kernel.contents.streaming_content_mixin import StreamingContentMixin
from semantic_kernel.contents.streaming_text_content import StreamingTextContent
from semantic_kernel.contents.text_content import TextContent
from semantic_kernel.exceptions import FunctionExecutionException, FunctionInitializationError
from semantic_kernel.functions.function_result import FunctionResult
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.functions.kernel_function import TEMPLATE_FORMAT_MAP, KernelFunction
from semantic_kernel.functions.kernel_function_metadata import KernelFunctionMetadata
from semantic_kernel.functions.kernel_parameter_metadata import KernelParameterMetadata
from semantic_kernel.prompt_template.const import KERNEL_TEMPLATE_FORMAT_NAME, TEMPLATE_FORMAT_TYPES
from semantic_kernel.prompt_template.prompt_template_base import PromptTemplateBase
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig

if TYPE_CHECKING:
    from semantic_kernel.kernel import Kernel

logger: logging.Logger = logging.getLogger(__name__)

PROMPT_FILE_NAME = "skprompt.txt"
CONFIG_FILE_NAME = "config.json"
PROMPT_RETURN_PARAM = KernelParameterMetadata(
    name="return",
    description="The completion result",
    default_value=None,
    type="FunctionResult",  # type: ignore
    is_required=True,
)


class KernelFunctionFromPrompt(KernelFunction):
    """Semantic Kernel Function from a prompt."""

    prompt_template: PromptTemplateBase
    prompt_execution_settings: dict[str, PromptExecutionSettings] = Field(default_factory=dict)

    def __init__(
        self,
        function_name: str,
        plugin_name: str | None = None,
        description: str | None = None,
        prompt: str | None = None,
        template_format: TEMPLATE_FORMAT_TYPES = KERNEL_TEMPLATE_FORMAT_NAME,
        prompt_template: PromptTemplateBase | None = None,
        prompt_template_config: PromptTemplateConfig | None = None,
        prompt_execution_settings: None | (
            PromptExecutionSettings | list[PromptExecutionSettings] | dict[str, PromptExecutionSettings]
        ) = None,
    ) -> None:
        """
        Initializes a new instance of the KernelFunctionFromPrompt class

        Args:
            function_name (str): The name of the function
            plugin_name (str): The name of the plugin
            description (str): The description for the function

            prompt (Optional[str]): The prompt
            template_format (Optional[str]): The template format, default is "semantic-kernel"
            prompt_template (Optional[KernelPromptTemplate]): The prompt template
            prompt_template_config (Optional[PromptTemplateConfig]): The prompt template configuration
            prompt_execution_settings (Optional): instance, list or dict of PromptExecutionSettings to be used
                by the function, can also be supplied through prompt_template_config,
                but the supplied one is used if both are present.
                prompt_template_config (Optional[PromptTemplateConfig]): the prompt template config.
        """
        if not prompt and not prompt_template_config and not prompt_template:
            raise FunctionInitializationError(
                "The prompt cannot be empty, must be supplied directly, \
through prompt_template_config or in the prompt_template."
            )

        if not prompt_template:
            if not prompt_template_config:
                # prompt must be there if prompt_template and prompt_template_config is not supplied
                prompt_template_config = PromptTemplateConfig(
                    name=function_name,
                    description=description,
                    template=prompt,
                    template_format=template_format,
                )
            prompt_template = TEMPLATE_FORMAT_MAP[template_format](prompt_template_config=prompt_template_config)  # type: ignore

        try:
            metadata = KernelFunctionMetadata(
                name=function_name,
                plugin_name=plugin_name,
                description=description,
                parameters=prompt_template.prompt_template_config.get_kernel_parameter_metadata(),
                is_prompt=True,
                is_asynchronous=True,
                return_parameter=PROMPT_RETURN_PARAM,
            )
        except ValidationError as exc:
            raise FunctionInitializationError("Failed to create KernelFunctionMetadata") from exc
        super().__init__(
            metadata=metadata,
            prompt_template=prompt_template,
            prompt_execution_settings=prompt_execution_settings,
        )

    @model_validator(mode="before")
    @classmethod
    def rewrite_execution_settings(
        cls,
        data: dict[str, Any],
    ) -> dict[str, PromptExecutionSettings]:
        """Rewrite execution settings to a dictionary.

        If the prompt_execution_settings is not a dictionary, it is converted to a dictionary.
        If it is not supplied, but prompt_template is, the prompt_template's execution settings are used.
        """
        prompt_execution_settings = data.get("prompt_execution_settings")
        prompt_template = data.get("prompt_template")
        if not prompt_execution_settings:
            if prompt_template:
                prompt_execution_settings = prompt_template.prompt_template_config.execution_settings
                data["prompt_execution_settings"] = prompt_execution_settings
            if not prompt_execution_settings:
                return data
        if isinstance(prompt_execution_settings, PromptExecutionSettings):
            data["prompt_execution_settings"] = {
                prompt_execution_settings.service_id or "default": prompt_execution_settings
            }
        if isinstance(prompt_execution_settings, list):
            data["prompt_execution_settings"] = {s.service_id or "default": s for s in prompt_execution_settings}
        return data

    async def _invoke_internal(
        self,
        kernel: Kernel,
        arguments: KernelArguments,
    ) -> FunctionResult:
        """Invokes the function with the given arguments."""
        arguments = self.add_default_values(arguments)
        service, execution_settings = kernel.select_ai_service(self, arguments)
        prompt = await self.prompt_template.render(kernel, arguments)

        if isinstance(service, ChatCompletionClientBase):
            return await self._handle_complete_chat(
                kernel=kernel,
                service=service,
                execution_settings=execution_settings,
                prompt=prompt,
                arguments=arguments,
            )

        if isinstance(service, TextCompletionClientBase):
            return await self._handle_text_complete(
                service=service,
                execution_settings=execution_settings,
                prompt=prompt,
                arguments=arguments,
            )

        raise ValueError(f"Service `{type(service).__name__}` is not a valid AI service")

    async def _handle_complete_chat(
        self,
        kernel: Kernel,
        service: ChatCompletionClientBase,
        execution_settings: PromptExecutionSettings,
        prompt: str,
        arguments: KernelArguments,
    ) -> FunctionResult:
        """Handles the chat service call."""
        chat_history = ChatHistory.from_rendered_prompt(prompt)

        # pass the kernel in for auto function calling
        kwargs: dict[str, Any] = {}
        if hasattr(execution_settings, "function_call_behavior"):
            kwargs["kernel"] = kernel
            kwargs["arguments"] = arguments

        try:
            completions = await service.get_chat_message_contents(
                chat_history=chat_history,
                settings=execution_settings,
                **kwargs,
            )
            if not completions:
                raise FunctionExecutionException(f"No completions returned while invoking function {self.name}")

            return self._create_function_result(completions=completions, chat_history=chat_history, arguments=arguments)
        except Exception as exc:
            raise FunctionExecutionException(f"Error occurred while invoking function {self.name}: {exc}") from exc

    async def _handle_text_complete(
        self,
        service: TextCompletionClientBase,
        execution_settings: PromptExecutionSettings,
        prompt: str,
        arguments: KernelArguments,
    ) -> FunctionResult:
        """Handles the text service call."""
        try:
            completions = await service.get_text_contents(unescape(prompt), execution_settings)
            return self._create_function_result(completions=completions, arguments=arguments, prompt=prompt)
        except Exception as exc:
            raise FunctionExecutionException(f"Error occurred while invoking function {self.name}: {exc}") from exc

    def _create_function_result(
        self,
        completions: list[ChatMessageContent] | list[TextContent],
        arguments: KernelArguments,
        chat_history: ChatHistory | None = None,
        prompt: str | None = None,
    ) -> FunctionResult:
        """Creates a function result with the given completions."""
        metadata: dict[str, Any] = {
            "arguments": arguments,
            "metadata": [completion.metadata for completion in completions],
        }
        if chat_history:
            metadata["messages"] = chat_history
        if prompt:
            metadata["prompt"] = prompt
        return FunctionResult(
            function=self.metadata,
            value=completions,
            metadata=metadata,
        )

    async def _invoke_internal_stream(
        self,
        kernel: Kernel,
        arguments: KernelArguments,
    ) -> AsyncGenerator[FunctionResult | list[StreamingContentMixin], Any]:
        """Invokes the function stream with the given arguments."""
        arguments = self.add_default_values(arguments)
        service, execution_settings = kernel.select_ai_service(self, arguments)
        prompt = await self.prompt_template.render(kernel, arguments)

        if isinstance(service, ChatCompletionClientBase):
            async for content in self._handle_complete_chat_stream(
                kernel=kernel,
                service=service,
                execution_settings=execution_settings,
                prompt=prompt,
                arguments=arguments,
            ):
                yield content  # type: ignore
            return

        if isinstance(service, TextCompletionClientBase):
            async for content in self._handle_complete_text_stream(  # type: ignore
                service=service,
                execution_settings=execution_settings,
                prompt=prompt,
            ):
                yield content  # type: ignore
            return

        raise FunctionExecutionException(f"Service `{type(service)}` is not a valid AI service")  # pragma: no cover

    async def _handle_complete_chat_stream(
        self,
        kernel: Kernel,
        service: ChatCompletionClientBase,
        execution_settings: PromptExecutionSettings,
        prompt: str,
        arguments: KernelArguments,
    ) -> AsyncGenerator[FunctionResult | list[StreamingChatMessageContent], Any]:
        """Handles the chat service call."""

        # pass the kernel in for auto function calling
        kwargs: dict[str, Any] = {}
        if hasattr(execution_settings, "function_call_behavior"):
            kwargs["kernel"] = kernel
            kwargs["arguments"] = arguments

        chat_history = ChatHistory.from_rendered_prompt(prompt)
        try:
            async for partial_content in service.get_streaming_chat_message_contents(
                chat_history=chat_history,
                settings=execution_settings,
                **kwargs,
            ):
                yield partial_content

            return  # Exit after processing all iterations
        except Exception as e:
            logger.error(f"Error occurred while invoking function {self.name}: {e}")
            yield FunctionResult(function=self.metadata, value=None, metadata={METADATA_EXCEPTION_KEY: e})

    async def _handle_complete_text_stream(
        self,
        service: TextCompletionClientBase,
        execution_settings: PromptExecutionSettings,
        prompt: str,
    ) -> AsyncGenerator[FunctionResult | list[StreamingTextContent], Any]:
        """Handles the text service call."""
        try:
            async for partial_content in service.get_streaming_text_contents(
                prompt=prompt, settings=execution_settings
            ):
                yield partial_content
            return
        except Exception as e:
            logger.error(f"Error occurred while invoking function {self.name}: {e}")
            yield FunctionResult(function=self.metadata, value=None, metadata={METADATA_EXCEPTION_KEY: e})

    def add_default_values(self, arguments: KernelArguments) -> KernelArguments:
        """Gathers the function parameters from the arguments."""
        for parameter in self.prompt_template.prompt_template_config.input_variables:
            if parameter.name not in arguments and parameter.default not in {None, "", False, 0}:
                arguments[parameter.name] = parameter.default
        return arguments

    @classmethod
    def from_yaml(cls, yaml_str: str, plugin_name: str | None = None) -> KernelFunctionFromPrompt:
        """Creates a new instance of the KernelFunctionFromPrompt class from a YAML string."""
        try:
            data = yaml.safe_load(yaml_str)
        except yaml.YAMLError as exc:  # pragma: no cover
            raise FunctionInitializationError(f"Invalid YAML content: {yaml_str}, error: {exc}") from exc

        if not isinstance(data, dict):
            raise FunctionInitializationError(f"The YAML content must represent a dictionary, got {yaml_str}")

        try:
            prompt_template_config = PromptTemplateConfig(**data)
        except ValidationError as exc:
            raise FunctionInitializationError(
                f"Error initializing PromptTemplateConfig: {exc} from yaml data: {data}"
            ) from exc
        return cls(
            function_name=prompt_template_config.name,
            plugin_name=plugin_name,
            description=prompt_template_config.description,
            prompt_template_config=prompt_template_config,
            template_format=prompt_template_config.template_format,
        )

    @classmethod
    def from_directory(cls, path: str, plugin_name: str | None = None) -> KernelFunctionFromPrompt:
        """Creates a new instance of the KernelFunctionFromPrompt class from a directory.

        The directory needs to contain:
        - A prompt file named `skprompt.txt`
        - A config file named `config.json`

        Returns:
            KernelFunctionFromPrompt: The kernel function from prompt
        """
        prompt_path = os.path.join(path, PROMPT_FILE_NAME)
        config_path = os.path.join(path, CONFIG_FILE_NAME)
        prompt_exists = os.path.exists(prompt_path)
        config_exists = os.path.exists(config_path)
        if not config_exists and not prompt_exists:
            raise FunctionInitializationError(
                f"{PROMPT_FILE_NAME} and {CONFIG_FILE_NAME} files are required to create a "
                f"function from a directory, path: {str(path)}."
            )
        elif not config_exists:
            raise FunctionInitializationError(
                f"{CONFIG_FILE_NAME} files are required to create a function from a directory, "
                f"path: {str(path)}, prompt file is there."
            )
        elif not prompt_exists:
            raise FunctionInitializationError(
                f"{PROMPT_FILE_NAME} files are required to create a function from a directory, "
                f"path: {str(path)}, config file is there."
            )

        function_name = os.path.basename(path)

        with open(config_path) as config_file:
            prompt_template_config = PromptTemplateConfig.from_json(config_file.read())
        prompt_template_config.name = function_name

        with open(prompt_path) as prompt_file:
            prompt_template_config.template = prompt_file.read()

        prompt_template = TEMPLATE_FORMAT_MAP[prompt_template_config.template_format](  # type: ignore
            prompt_template_config=prompt_template_config
        )
        return cls(
            function_name=function_name,
            plugin_name=plugin_name,
            prompt_template=prompt_template,
            prompt_template_config=prompt_template_config,
            template_format=prompt_template_config.template_format,
            description=prompt_template_config.description,
        )

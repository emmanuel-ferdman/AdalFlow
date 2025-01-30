__version__ = "1.0.0.beta.2"

from adalflow.core.component import (
    Component,
    DataComponent,
    FuncComponent,
    FuncDataComponent,
    func_to_data_component,
    func_to_component,
)
from adalflow.core.container import Sequential, ComponentList
from adalflow.core.base_data_class import DataClass, DataClassFormatType, required_field

from adalflow.optim.grad_component import GradComponent
from adalflow.core.generator import Generator

from adalflow.core.types import (
    GeneratorOutput,
    EmbedderOutput,
    RetrieverOutput,
    Document,
)
from adalflow.core.model_client import ModelClient
from adalflow.core.embedder import Embedder

# parser
from adalflow.core.string_parser import (
    YamlParser,
    JsonParser,
    IntParser,
    FloatParser,
    ListParser,
    BooleanParser,
)
from adalflow.core.retriever import Retriever
from adalflow.components.output_parsers import (
    YamlOutputParser,
    JsonOutputParser,
    ListOutputParser,
)
from adalflow.components.output_parsers.dataclass_parser import DataClassParser

from adalflow.core.prompt_builder import Prompt

# optimization
from adalflow.optim import (
    Optimizer,
    DemoOptimizer,
    TextOptimizer,
    Parameter,
    AdalComponent,
    Trainer,
    BootstrapFewShot,
    TGDOptimizer,
    EvalFnToTextLoss,
    LLMAsTextLoss,
)

from adalflow.optim.types import ParameterType
from adalflow.utils import setup_env, get_logger

from adalflow.components.model_client import (
    OpenAIClient,
    GoogleGenAIClient,
    GroqAPIClient,
    OllamaClient,
    TransformersClient,
    AnthropicAPIClient,
    CohereAPIClient,
    BedrockAPIClient,
)

# data pipeline
from adalflow.components.data_process.text_splitter import TextSplitter
from adalflow.components.data_process.data_components import ToEmbeddings

__all__ = [
    "Component",
    "DataComponent",
    "FuncComponent",
    "FuncDataComponent",
    "func_to_data_component",
    "func_to_component",
    # dataclass
    "DataClass",
    "DataClassFormatType",
    "required_field",
    # Container
    "Sequential",
    "ComponentList",
    # Grad Component
    "GradComponent",
    # Functional Component
    "ModelClient",
    "Generator",
    "Embedder",
    "Retriever",
    "Parameter",
    "AdalComponent",
    "Trainer",
    "BootstrapFewShot",
    "TGDOptimizer",
    "EvalFnToTextLoss",
    "LLMAsTextLoss",
    "setup_env",
    "get_logger",
    "Prompt",
    # Parsers
    "YamlParser",
    "JsonParser",
    "IntParser",
    "FloatParser",
    "ListParser",
    "BooleanParser",
    "Parser",
    "FuncParser",
    # Output Parsers with dataclass formatting
    "YamlOutputParser",
    "JsonOutputParser",
    "ListOutputParser",
    "DataClassParser",
    # Data Pipeline
    "TextSplitter",
    "ToEmbeddings",
    # Types
    "GeneratorOutput",
    "EmbedderOutput",
    "RetrieverOutput",
    "Document",
    # Optimizer types
    "Optimizer",
    "DemoOptimizer",
    "TextOptimizer",
    # parameter types
    "ParameterType",
    # model clients
    "OpenAIClient",
    "GoogleGenAIClient",
    "GroqAPIClient",
    "OllamaClient",
    "TransformersClient",
    "AnthropicAPIClient",
    "CohereAPIClient",
    "BedrockAPIClient",
]

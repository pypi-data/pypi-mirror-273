import importlib
from typing import Any

_module_lookup = {
    "Document": "nchuchain.utils.data",
    "QAResult": "nchuchain.utils.data",
    "QAModelConfig": "nchuchain.utils.config",
    "QAConfig": "nchuchain.utils.config",
    "PromptTemplate": "nchuchain.utils.template",
    "MessageTemplate": "nchuchain.utils.template",
}


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module = importlib.import_module(_module_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = list(_module_lookup.keys())
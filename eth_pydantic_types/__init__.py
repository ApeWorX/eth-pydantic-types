def __getattr__(name: str):
    import eth_pydantic_types._main as module

    return getattr(module, name)

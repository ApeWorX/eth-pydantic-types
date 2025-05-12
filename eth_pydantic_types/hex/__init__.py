def __getattr__(name: str):
    if "str" in name.lower():
        import eth_pydantic_types.hex.str

        return getattr(eth_pydantic_types.hex.str, name)

    elif "int" in name.lower():
        import eth_pydantic_types.hex.int

        return getattr(eth_pydantic_types.hex.int, name)

    # bytes.
    import eth_pydantic_types.hex.bytes

    return getattr(eth_pydantic_types.hex.bytes, name)

def remove_nones_helper(data):
    """
    Recursive helper returns the parameter dictionary with None key:values removed
    from top level and all nested dictionaries
    """
    if isinstance(data, dict):
        return {
            key: remove_nones_helper(value)
            for key, value in data.items()
            if value is not None and remove_nones_helper(value) is not None
        }
    return data

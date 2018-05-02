def splat_listed_dict_values(vals) -> list:
    """Flattens out a nest of dict.values()"""
    capture = []
    for v in vals:
        if isinstance(v, list):
            for x in v:
                capture.append(x)
    if len(capture) > 0:
        return capture
    else:
        return


def raw_cocodict() -> dict:
    """
    Return an empty dictionnary for COCO basic keys.

    Returns:
        ``Dict[str, List]``:
            - Empty COCO dictionnary.
    """
    return {"categories": [], "images": [], "annotations": []}

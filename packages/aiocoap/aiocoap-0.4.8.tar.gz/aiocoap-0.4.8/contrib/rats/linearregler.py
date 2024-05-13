@rats.pure
def ausgang(eingang: float,
        x0: float, x1: float,
        y0: float, y1: float) -> float:
    if eingang < x0:
        return y0
    if eingang > x1:
        return y1
    return y0 + (y1 - y0) / ((eingang - x0) / (x1 - x0))

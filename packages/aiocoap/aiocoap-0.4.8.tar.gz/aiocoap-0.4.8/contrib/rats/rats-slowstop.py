def output(switch: bool, last_change: int, now: int) -> float:
    if switch == True:
        return 1
    if now - last_on > 10:
        return 0
    return 0.2

def last_change(switch: WithHistory[bool]) -> int:
    return switch.times[-1]

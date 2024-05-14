import datetime


def convert_nanoseconds_to_string(nanoseconds: int) -> str:
    epoch = datetime.datetime(1970, 1, 1)
    time = epoch + datetime.timedelta(microseconds=nanoseconds // 1000)
    return time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def decide_export(trace_id: int, rate: float) -> bool:
    if rate < 0.0 or rate > 1.0:
        raise ValueError("Probability must be in range [0.0, 1.0].")

    TRACE_ID_LIMIT = (1 << 64) - 1

    def get_bound_for_rate(rate: float) -> int:
        return round(rate * (TRACE_ID_LIMIT + 1))

    bound = get_bound_for_rate(rate)
    return trace_id & TRACE_ID_LIMIT < bound

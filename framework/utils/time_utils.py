from datetime import datetime


def time_stamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

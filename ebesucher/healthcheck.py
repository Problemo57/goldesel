from time import time
from datetime import datetime
from os import environ


def unhealthy() -> bool:
    surfads_logs = open("surfads.log").read()
    surfads = []
    surfads_lines = surfads_logs.splitlines()
    for i in range(len(surfads_lines)//2):
        surfads.append({
            'timestamp': datetime.strptime(surfads_lines[i*2].split(':')[0], "%Y%m%d_%H%M%S").timestamp(),
            'viewtime': int(surfads_lines[i*2].split(':')[-1]),
            'credits': float(surfads_lines[i*2+1].split(':')[-1])
        })

    if not surfads_lines:
        return True

    last_ten_earnings = sum([e['credits'] for e in surfads[-30:]])
    if last_ten_earnings <= 0:
        return True

    if not [True for surfad in surfads if surfad['timestamp'] + surfad['viewtime']*5 + 10 > time()]:
        return True

    return False


if __name__ == '__main__':
    if 'SURFBAR_NAME' not in environ:
        print("SURFBAR_NAME not set. Exiting.")
        exit(1)

    if unhealthy():
        print("Healthcheck failed. Exiting.")
        exit(1)

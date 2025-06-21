from time import sleep
from os import environ
from subprocess import Popen, run
from healthcheck import unhealthy

username = environ['SURFBAR_NAME']
device_name = environ['DEVICE_NAME']
logs = open("firefox.logs", "w")


def start_browser(surfbar_name: str):
    run(["killall", "-9", "firefox-esr"])
    Popen(["firefox-esr", "-start-debugger-server", "6080", "-P", "ebesucher", "-headless", f'https://www.ebesucher.de/surfbar/{surfbar_name}'], stdout=logs, stderr=logs)
    Popen(["""tail -f firefox.logs | awk -F, '{
      for (i = 1; i <= NF; i++) {
        if ($i ~ /EarnableCredits:/ || $i ~ /ViewTime:/) {
          cmd = "date +%Y%m%d_%H%M%S"
          cmd | getline ts
          close(cmd)
          print ts ":" $i
        }
      }
    }' | tee surfads.log"""], shell=True)


def main():
    surfbar_name = username
    if device_name:
        surfbar_name += f".{device_name}"

    start_browser(surfbar_name)
    sleep(60)

    while not unhealthy():
        sleep(10)

    print("Unhealthy. Exiting.")
    exit(1)


if __name__ == '__main__':
    main()

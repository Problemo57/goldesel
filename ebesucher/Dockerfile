FROM python:3.12

ENV SURFBAR_NAME="Problemo1"
ENV DEVICE_NAME=""

ENV TZ="Europe/Berlin"
ENV MOZ_HEADLESS_WIDTH=1920
ENV MOZ_HEADLESS_HEIGHT=1080
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y firefox-esr firefox-esr-l10n-de psmisc wget unzip zip socat
RUN apt-get install -y fontconfig fontconfig-config fonts-cantarell fonts-dejavu fonts-dejavu-core fonts-dejavu-extra fonts-droid-fallback fonts-firacode fonts-font-awesome fonts-freefont-ttf fonts-hack fonts-lato fonts-liberation fonts-lmodern fonts-lyx fonts-mathjax fonts-noto-color-emoji fonts-noto-mono fonts-quicksand fonts-texgyre fonts-urw-base35 fonts-wine lmodern tex-gyre texlive-fonts-recommended toilet-fonts xfonts-100dpi xfonts-75dpi xfonts-base xfonts-encodings xfonts-scalable

RUN rm /usr/lib/python3*/EXTERNALLY-MANAGED
RUN pip3 install requests Flask cryptography

COPY ebesucher.py prepare_firefox.sh healthcheck.py start.sh patch_webgl.js /

ENTRYPOINT exec sh /start.sh
HEALTHCHECK --start-period=120s CMD python3 /healthcheck.py

# Upstream LedFx image (Python 3.12, LedFx in /app/.venv), pinned by digest.
# Bump: update the tag and digest together, and the version in config.yaml.
FROM ghcr.io/ledfx/ledfx:2.2.1@sha256:fda3622040f6fb207440575f232826f31ded4bc5900a3d650c3ce4f31235beeb

# The upstream entrypoint starts PulseAudio and its healthcheck queries it. The add-on takes its
# audio from Music Assistant via Sendspin, so neither is needed. LedFx runs as root to own /data.
USER root
HEALTHCHECK NONE

COPY run.sh /run.sh
RUN chmod 755 /run.sh

ENTRYPOINT ["/run.sh"]

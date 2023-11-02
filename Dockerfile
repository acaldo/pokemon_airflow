FROM quay.io/astronomer/astro-runtime:9.4.0

RUN python -m venv poke_venv && source poke_venv/bin/activate && \
    pip install --no-cache-dir requests && \
    pip install --no-cache-dir pandas && \
    pip install --no-cache-dir aiohttp && deactivate
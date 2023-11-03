FROM quay.io/astronomer/astro-runtime:9.4.0

RUN python -m venv poke_venv && source poke_venv/bin/activate && \
    pip install --no-cache-dir requests && \
    pip install --no-cache-dir pandas && \
    pip install --no-cache-dir aiohttp && deactivate

# install soda into a virtual environment
RUN python -m venv soda_venv && source soda_venv/bin/activate && \
    pip install --no-cache-dir soda-core-bigquery==3.0.45 &&\
    pip install --no-cache-dir soda-core-scientific==3.0.45 && deactivate
FROM python:3.12.15-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY requirements.lock ./
RUN python -m pip install --no-cache-dir --index-url https://pypi.org/simple --require-hashes -r requirements.lock
COPY coworking_nearby/*.py ./coworking_nearby/
COPY data/coworkings.json ./data/coworkings.json
RUN chmod 0555 /app /app/coworking_nearby /app/data && chmod 0444 /app/coworking_nearby/*.py /app/data/coworkings.json /app/requirements.lock
USER 10001:10001
CMD ["python", "-m", "coworking_nearby"]

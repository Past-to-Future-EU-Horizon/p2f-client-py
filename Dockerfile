FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /p2f/p2f-client-py

RUN apk update
RUN apk upgrade
RUN apk add git

ADD . .

ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/ uv sync --all-extras && uv build

RUN uv pip install .

ENV PATH="/p2f/p2f-client-py/.venv/bin/:$PATH"

CMD ["/p2f/p2f-client-py/.venv/bin/python", "tests/test_0sequence.py"]
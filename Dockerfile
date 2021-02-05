FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH "$PATH:/root/.poetry/bin"
RUN poetry config virtualenvs.create false

# Location of source code
ENV PROJECT_ROOT /opt/flipt
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

# Copying dependencies
COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN poetry install -E rest

# Copying source files
COPY . .

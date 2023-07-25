FROM python:3.10 as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
ARG INSTALL_DEV=false
ENV PIPENV_VENV_IN_PROJECT=1
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pipenv install --dev ; else pipenv install ; fi"

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /code

COPY . /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

FROM python:3.12
ENV WORKDIR="/app"
WORKDIR ${WORKDIR}

RUN mkdir golynx
COPY pyproject.toml pdm.lock ${WORKDIR}
RUN pip install pdm && pdm install && pdm install -G supabase
COPY golynx ${WORKDIR}/golynx

CMD [ "pdm", "run", "uvicorn", "golynx.main:app", "--host", "0.0.0.0" ]

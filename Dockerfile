FROM python:3.12
ENV WORKDIR="/app"
WORKDIR ${WORKDIR}

RUN mkdir golynx
COPY pyproject.toml ${WORKDIR}
RUN pip install '.'
COPY golynx ${WORKDIR}/golynx

CMD [ "uvicorn", "golynx.main:app", "--host", "0.0.0.0" ]
FROM python:3.12
ENV WORKDIR="/app"
WORKDIR ${WORKDIR}

RUN mkdir golinks
COPY pyproject.toml ${WORKDIR}
RUN pip install '.'
COPY golinks ${WORKDIR}/golinks

CMD [ "uvicorn", "golinks.main:app", "--host", "0.0.0.0" ]
FROM python:3.6.5-alpine3.7

WORKDIR /usr/src/app
RUN pip install pytest

COPY . .
RUN rm -Rf __pycache__

CMD [ "pytest" ]

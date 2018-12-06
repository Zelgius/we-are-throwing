FROM python:3.7

RUN pip3 install pipenv

EXPOSE 8000

WORKDIR /opt/talon

COPY Pipfile* /opt/talon/

COPY dist/*.whl /opt/talon/

COPY gunicorn_config.py /opt/talon/

RUN pipenv install --deploy --system

RUN pip3 install *.whl

RUN rm -rf /opt/talon/*.whl

CMD gunicorn --config gunicorn_config.py "we_are_throwing:create_app()"

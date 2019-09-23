FROM python:3.6-slim

MAINTAINER "data-bazaar-team" <Your email>
ARG pypi_url

RUN groupadd -r dbzr-projects-audit-user && useradd -u 1000 -r -g dbzr-projects-audit-user dbzr-projects-audit-user

RUN apt-get update && apt-get install -y software-properties-common gcc libpq-dev python3-dev supervisor

ADD ./requirements.txt /opt/babylon/dbzr-projects-audit/requirements.txt

WORKDIR /opt/babylon/dbzr-projects-audit

RUN pip3 install -r requirements.txt uWSGI==2.0.15 --extra-index-url $pypi_url
ADD . /opt/babylon/dbzr-projects-audit

EXPOSE 8000

USER dbzr-projects-audit-user
CMD ["bash", "run.sh", "--uwsgi"]

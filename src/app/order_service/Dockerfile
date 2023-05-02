###############
# Build Stage #
###############
FROM python:3.8.9 as build

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /opt/venv

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV="/opt/venv"

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir pipenv

# Copy dependency files and install
# Every code change should not trigger reinstalling
# of dependencies
COPY Pipfile Pipfile.lock /opt/venv/

RUN pipenv install --system --deploy --ignore-pipfile --clear

#####################
# Production Stage #
#####################
FROM python:3.8-slim

WORKDIR /opt/venv

COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV="/opt/venv"

RUN apt autoremove -y

WORKDIR /order_service

# Finally copying application code
COPY . /order_service/

ENTRYPOINT ["sh", "-c"," python3 grpcserver.py & python3 wsgi.py"]
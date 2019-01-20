FROM python:3.7-slim
RUN apt update
RUN apt install -y python3-dev python3-pip
COPY requirements.txt /usr/local/src/rabbitmq_agents/
RUN pip3 install -r requirements.txt
COPY . /usr/local/src/rabbitmq_agents
ENV PYTHONPATH=/usr/local/src/rabbitmq_agents
WORKDIR /usr/local/src/rabbitmq_agents
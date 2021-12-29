FROM python:3.7-slim

RUN apt-get update
RUN apt-get --assume-yes install git gcc

RUN pip install --upgrade pip

WORKDIR "/tmp"

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pip install coverage
RUN pip install pytest
RUN pip install pytest-cov
RUN pip install pytest-bdd
RUN pip install google-api-python-client
RUN pip install google-cloud-resource-manager
RUN pip install google-cloud-storage
RUN pip install google-cloud-bigquery
RUN pip install google-cloud-firestore
RUN pip install jsonschema
RUN pip install PyYAML
RUN pip install google-cloud-workflows
RUN pip install google-api-python-client
RUN pip install google-cloud-pubsub
RUN pip install apache-beam
RUN pip install google_apitools

RUN apt-get update
RUN apt-get install curl -y
# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

RUN apt-get install jq -y

RUN pip install apache-beam[gcp]
RUN pip install apache_beam[dataframe]

CMD /bin/bash
# Docker

This is an  agent based check, which wil monitor Docker.

## Requirements
You must install Python package docker with
pip install docker.

## Configuration
Standard interval for quering Docker is 2 minutes. If you change this interval to 5 minutes for example,
then you should switch the update interval for services to 5 minutes, too. This can be done with rule
"Normal check interval for service checks".

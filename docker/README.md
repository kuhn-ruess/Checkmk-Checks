# Docker

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p25-blue)
<!-- compatibility-badges:end -->

This is an  agent based check, which wil monitor Docker.

## Requirements
You must install Python package docker with
pip install docker.

## Configuration
Standard interval for quering Docker is 2 minutes. If you change this interval to 5 minutes for example,
then you should switch the update interval for services to 5 minutes, too. This can be done with rule
"Normal check interval for service checks".

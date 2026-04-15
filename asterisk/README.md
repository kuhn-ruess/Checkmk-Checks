# Asterisk call notification

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p20-blue)
<!-- compatibility-badges:end -->

This notification script will use Asterisk to make a call to a defined phone number.
It is configurable with parameters to match the local environment.

## Requirements
Python package asterisk.ami must be installed in version >= 0.1.7.

It can be installed as siteuser with `pip3 install asterisk-ami`

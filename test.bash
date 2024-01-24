#!/usr/bin/env bash

set -e
set -x

ENV_STATE=test pytest --cov app --cov-report term-missing
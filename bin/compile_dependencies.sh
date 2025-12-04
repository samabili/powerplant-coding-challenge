#!/bin/bash

uv pip compile --output-file requirements/requirements.txt requirements/requirements.in 

uv pip compile --output-file requirements/dev_requirements.txt requirements/requirements.txt requirements/dev_requirements.in
# Variables
VENV := $(CURDIR)/venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

# Activate the virtual environment: source venv/bin/activate

# Main Scripts:
auto_metric_script: $(VENV)
	clear; time $(PYTHON) ./AutoMetric.py $(args)

# Define the main target that runs the scripts in the specified order and waits for the previous one to finish before starting the next one
all: dependencies auto_metric_script

# Setup Virtual Environment and Install Dependencies
$(VENV): dependencies

# Install the project dependencies in a virtual environment
dependencies:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Generate requirements.txt from the current venv
generate_requirements:
	$(PIP) freeze > requirements.txt

# Utility rule for cleaning the project
clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: clean auto_metric_scrip dependencies generate_requirements

SHELL := /bin/bash
SITE ?= secure.login.gov
PYLINT ?= $(shell which pylint pylint3 true 2>/dev/null | head -n 1)
PYTHON ?= $(shell which python3 python false 2>/dev/null | head -n 1)
all: totp.pylint totp.run
%.run: %.py
	$(PYTHON) $< $(SITE)
%.pylint: %.py
	$(PYLINT) $<

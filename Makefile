PROJECT_NAME=thermal-cam
PYTHON=python3

###############################################################################
# ENV SETUP                                                                   #
###############################################################################

.PHONY: env-create
env-create:
	$(PYTHON) -m venv .venv --prompt $(PROJECT_NAME)
	make env-update
	#
	# Don't forget to activate the environment before proceeding! You can run:
	# source .venv/bin/activate


.PHONY: env-update
env-update:
	bash -c "\
                . .venv/bin/activate && \
                pip install wheel && \
                CFLAGS=-fcommon pip install --upgrade -r requirements.txt \
        "


.PHONY: env-delete
env-delete:
	rm -rf .venv


###############################################################################
# START WEB SERVER                                                            #
###############################################################################

.PHONY: start_server
start_server:
	. .venv/bin/activate && PYTHONPATH=. python examples/web_server.py > logs/thermal_out.txt 2>logs/thermal_err.txt

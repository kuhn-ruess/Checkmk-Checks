# Publish plugin versions to the Checkmk Exchange.
#
#   make exchange-dry PLUGIN=apc_netbotz
#   make exchange PLUGIN=apc_netbotz DESC="New checks for smoke sensors"
#
# PLUGIN takes a comma list; without PLUGIN every outdated package is uploaded.
# Credentials: EXCHANGE_USER / EXCHANGE_PASSWORD from the environment or from
# EXCHANGE_ENV (default ~/.claude/exchange.env), otherwise the script prompts.
# The login form needs a CAPTCHA: log in with the browser and pass the cookie
# checkmk_exchange_session as EXCHANGE_SESSION=<value>.

EXCHANGE_ENV ?= $(HOME)/.claude/exchange.env
PLUGIN ?=
DESC ?= Update to version {ver}.
export EXCHANGE_SESSION

EXCHANGE_CMD = set -a; [ -f "$(EXCHANGE_ENV)" ] && . "$(EXCHANGE_ENV)"; set +a; \
	python3 cmk_api_scripts/exchange_publish.py --repo "$(CURDIR)" \
	$(if $(PLUGIN),--only "$(PLUGIN)") --description "$(DESC)"

.PHONY: exchange exchange-dry

exchange-dry:
	@$(EXCHANGE_CMD) --dry-run

exchange:
	@$(EXCHANGE_CMD)

#!/bin/sh

# This script acts as a wrapper.
# "$@" represents the arguments passed from the 'docker run' command.

# We place "$@" BEFORE the test path (tests/unitest) so flags are parsed correctly,
# but AFTER the base flags so user arguments can override defaults if needed.

exec python -m pytest -sv --alluredir=reports/allure-results  "$@" tests/unitest
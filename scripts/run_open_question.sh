#!/usr/bin/env bash
# Section 5 - Open question: recurring director-actor collaborations (silver -> gold).
#
# Usage (inside the spark container): bash scripts/run_open_question.sh
#
# Reads the silver layer only (no external request). Writes the gold tables to
# data/gold/open_question/ and the tables to outputs/open_question/.

source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

submit "open_question/collaborations.py"

log "open question finished, reports are in outputs/open_question/"

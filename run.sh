#!/usr/bin/env bash

set -e

export SERVICE_PORT="${SERVICE_PORT:-8000}"
export GEVENT_GREENLETS="${GEVENT_GREENLETS:-128}"

run_simple() {
  python app.py
}

run_uwsgi() {
  uwsgi --ini uwsgi.ini -w app:application
}

parse_args() {
  mode=simple
  while  [[ $# -gt 0 ]]; do
    case $1 in
      --uwsgi) mode=uwsgi ;;
      *) ;;
    esac
    shift
  done
}

main() {
  parse_args "$@"
  case "${mode}" in
    simple) run_simple ;;
    uwsgi) run_uwsgi ;;
    *) ;;
  esac
}

main "$@"

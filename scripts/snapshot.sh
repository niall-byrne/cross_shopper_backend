#!/bin/bash

set -eo pipefail

PROJECT_FOLDER="cross_shopper"
DJANGO_MANAGE_SHIM_PATH="${PROJECT_FOLDER}/manage.py"
SNAPSHOTS_PATH=".snapshots"

_snapshot_git_root() {
  cd "$(git rev-parse --show-toplevel)"
  mkdir -p "${SNAPSHOTS_PATH}"
}

_snapshot_django_command() {
  DJANGO_SETTINGS_MODULE="config.${ENVIRONMENT_NAME}" poetry run "${DJANGO_MANAGE_SHIM_PATH}" "${@}"
}

_snapshot_create() {
  local source_file="${PROJECT_FOLDER}/db.${1}.sqlite"
  local output_file="${SNAPSHOTS_PATH}/${2}"

  _snapshot_git_root
  _snapshot_create_args "${@}"

  truncate -s 0 "${output_file}"

  ENVIRONMENT_NAME="${1}" _snapshot_django_command dumpdata --format json --exclude contenttypes --all > "${output_file}"

  echo "Data dumped to ${output_file}"
}

_snapshot_create_args() {
  if [[ "${#@}" -ne 2 ]]; then
    echo "Usage: snapshot.sh create [environment_name] [snapshot_file]"
    exit 127
  fi

  if [[ ! -f "${source_file}" ]]; then
    echo "The specified database (${source_file}) does not exist."
    exit 127
  fi

  if [[ -f "${output_file}" ]]; then
    echo "The specified snapshot (${output_file}) already exists, are you sure you want to do this?"
    exit 127
  fi
}

_snapshot_load() {
  local output_file="${PROJECT_FOLDER}/db.${2}.sqlite"
  local source_file="${SNAPSHOTS_PATH}/${1}"

  _snapshot_git_root
  _snapshot_load_args "${@}"

  truncate -s 0 "${output_file}"

  ENVIRONMENT_NAME="${2}" _snapshot_django_command migrate
  ENVIRONMENT_NAME="${2}" _snapshot_django_command loaddata --format json - < "${source_file}"

  echo "Data restored to ${output_file}"
}

_snapshot_load_args() {
  if [[ "${#@}" -ne 2 ]]; then
    echo "Usage: snapshot.sh load [snapshot_file] [environment_name] "
    exit 127
  fi

  if [[ ! -f "${source_file}" ]]; then
    echo "The specified snapshot (${source_file}) does not exist."
    exit 127
  fi

  if [[ ! -f "${output_file}" ]]; then
    echo "The specified database (${output_file}) does not exist."
    exit 127
  fi
}

_snapshot_list() {
  _snapshot_git_root
  ls -lath "${SNAPSHOTS_PATH}"
}

main() {
  local command="${1}"

  shift || true

  case "${command}" in
    create)
      _snapshot_create "${@}"
      ;;
    load)
      _snapshot_load "${@}"
      ;;
    list)
      _snapshot_list "${@}"
      ;;
    *)
      main_help
      ;;
  esac
}

main_help() {
  echo "Valid Commands:"
  echo " create     -- Extract database data and export to a json snapshot file."
  echo " load       -- Rebuild database data from a json snapshot file."
  echo " list       -- List all json snapshot files."
  exit 127
}

main "${@}"

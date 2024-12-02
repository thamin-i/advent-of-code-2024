#!/usr/bin/env bash

PERMITTED_HOOKS="pre-commit;commit-msg"
PATH_HOOKS="$(
  cd "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"
PATH_ROOT="${PATH_HOOKS%/*}"
PRE_COMMIT_BIN="${PATH_ROOT}/.venv/bin/pre-commit"

installFunction() {
  for CONFIGFILE in $(ls -a "${PATH_HOOKS}"); do
    if [[ "${CONFIGFILE}" =~ ^[\.].*-config.yaml$ ]]; then
      echo "Configuration file ${CONFIGFILE} found."
      HOOK_TYPE=$(echo "${CONFIGFILE}" | cut -d"." -f2 | sed 's/-config//')
      if [[ "$PERMITTED_HOOKS" =~ .*$HOOK_TYPE.* ]]; then
        printf 'HOOK_TYPE %s is valid.\nInstalling:\n' "${HOOK_TYPE}"
        "${PRE_COMMIT_BIN}" install -t "$HOOK_TYPE" --config "${PATH_HOOKS}/${CONFIGFILE}"
        printf '\n\n'
      else
        printf 'HOOK_TYPE %s is invalid.\nAborting.\n\n' "${HOOK_TYPE}"
      fi
    else
      printf 'Filename %s not matching the regex.\nSkipping.\n\n' "${CONFIGFILE}"
    fi
  done
  exit 0
}

uninstallFunction() {
  HOOKS_TO_DELETE=$1
  INSTALLED_HOOKS=""
  for HOOK in $(ls -a "${PATH_HOOKS}/../.git/hooks/"); do
    if ! [[ "${HOOK}" =~ (.*sample$|^[\.]*$) ]]; then
      INSTALLED_HOOKS="${INSTALLED_HOOKS}${HOOK};"
    fi
  done
  printf 'Currently installed hooks are: %s\n\n' "$(echo ${INSTALLED_HOOKS} | tr ";" " ")"
  if [[ "${HOOKS_TO_DELETE}" == "all" ]]; then
    for HOOK in $(echo "${INSTALLED_HOOKS}" | tr ";" "\n"); do
      "${PRE_COMMIT_BIN}" uninstall -t "${HOOK}"
    done
  else
    for HOOK in $(echo "${HOOKS_TO_DELETE}" | tr "," "\n"); do
      if [[ "${INSTALLED_HOOKS}" =~ .*${HOOK}.* ]]; then
        "${PRE_COMMIT_BIN}" uninstall -t "${HOOK}"
      fi
    done
  fi
}

helpFunction() {
  echo ""
  echo "Usage: [-i|u] [ARGS]"
  echo -e "\tARGS Names of hooks to uninstall seperated by a ,"
  echo -e "\t-i Installs hooks based on the config files found in ${PATH_HOOKS}"
  echo -e "\t-u Uninstalls hooks specified in ARGS"
  echo -e "\t-h prints help"
  exit 1
}

while getopts "u:ih" opt; do
  case $opt in
  i) installFunction ;;
  u)
    HOOKS_TO_REMOVE="${OPTARG}"
    uninstallFunction "${HOOKS_TO_REMOVE}"
    ;;
  h) helpFunction ;;
  \?) helpFunction ;;
  esac
done

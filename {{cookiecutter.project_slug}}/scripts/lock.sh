#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
cd "${PROJECT_ROOT}"

set -x
poetry lock
# Without development dependencies:
poetry export -f requirements.txt >requirements_tmp.txt
# With development dependencies:
# poetry export --dev -f requirements.txt >requirements_tmp.txt
mv requirements_tmp.txt requirements.txt


# Also generate a version without hashes for use by static tools that don't handle hashes well
poetry export -f requirements.txt --without-hashes >requirements_tmp.txt
mv requirements_tmp.txt requirements-no-hash.txt

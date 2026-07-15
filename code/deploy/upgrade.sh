#!/usr/bin/env bash
set -euo pipefail

prefix="${MIOS_PREFIX:-/opt/mayos-reachy}"
wheel="${1:?usage: upgrade.sh WHEEL SHA256_FILE}"
sha_file="${2:?usage: upgrade.sh WHEEL SHA256_FILE}"
[[ -f "$wheel" && -f "$sha_file" ]] || { echo "artifact or digest missing" >&2; exit 2; }
sha256sum --check "$sha_file"
previous="$(readlink -f "$prefix/current")"
"$prefix/venv/bin/pip" install --no-index "$wheel"
release="$(basename "$wheel" .whl)"
release_dir="$prefix/releases/$release"
install -d -m 0755 "$release_dir"
install -m 0644 "$wheel" "$release_dir/"
ln -sfn "$release_dir" "$prefix/current"
if ! "$prefix/venv/bin/python" -c 'import app; print("package import ok")'; then
  ln -sfn "$previous" "$prefix/current"
  echo "health check failed; restored $previous" >&2
  exit 1
fi
echo "upgraded to $release"

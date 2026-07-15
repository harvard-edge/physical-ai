#!/usr/bin/env bash
set -euo pipefail

prefix="${MIOS_PREFIX:-/opt/mayos-reachy}"
wheel="${1:?usage: install.sh WHEEL [SHA256_FILE]}"
sha_file="${2:-}"

[[ -f "$wheel" ]] || { echo "wheel not found: $wheel" >&2; exit 2; }
if [[ -n "$sha_file" ]]; then
  sha256sum --check "$sha_file"
fi
install -d -m 0755 "$prefix/releases" "$prefix/venv" "$prefix/data"
release="$(basename "$wheel" .whl)"
release_dir="$prefix/releases/$release"
install -d -m 0755 "$release_dir"
install -m 0644 "$wheel" "$release_dir/"
python3 -m venv "$prefix/venv"
"$prefix/venv/bin/pip" install --no-index "$release_dir/$(basename "$wheel")"
ln -sfn "$release_dir" "$prefix/current"
echo "installed $release; service activation remains an operator action"

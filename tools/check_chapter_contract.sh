#!/usr/bin/env bash

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

chapters=(
  book/chapters/01-frame/01-frame.qmd
  book/chapters/02-costs/02-costs.qmd
  book/chapters/03-measure/03-measure.qmd
  book/chapters/04-runtime/04-runtime.qmd
  book/chapters/05-perception/05-perception.qmd
  book/chapters/06-state/06-state.qmd
  book/chapters/07-intent/07-intent.qmd
  book/chapters/08-limits/08-limits.qmd
  book/chapters/09-placement/09-placement.qmd
  book/chapters/10-assurance/10-assurance.qmd
  book/chapters/11-authority/11-authority.qmd
  book/chapters/12-learning/12-learning.qmd
  book/chapters/13-deploy/13-deploy.qmd
)

if (( $# > 0 )); then
  chapters=("$@")
fi

failures=0

fail() {
  printf 'FAIL  %s  %s\n' "$1" "$2" >&2
  failures=$((failures + 1))
}

count_pattern() {
  local pattern="$1"
  local file="$2"
  awk -v pattern="$pattern" '$0 == pattern { count++ } END { print count + 0 }' "$file"
}

for relative in "${chapters[@]}"; do
  file="$root/$relative"

  if [[ ! -f "$file" ]]; then
    fail "$relative" "file does not exist"
    continue
  fi

  objective_count="$(count_pattern '::: {.callout-objective}' "$file")"
  decision_count="$(count_pattern '::: {.callout-decision}' "$file")"
  lab_count="$(count_pattern '::: {.callout-lab}' "$file")"

  [[ "$objective_count" == 1 ]] || fail "$relative" "expected one objective callout"
  [[ "$decision_count" == 1 ]] || fail "$relative" "expected one decision callout"
  [[ "$lab_count" == 1 ]] || fail "$relative" "expected one lab callout"

  objective_line="$(awk '$0 == "::: {.callout-objective}" { print NR; exit }' "$file")"
  first_h2_line="$(awk '/^## / { print NR; exit }' "$file")"

  if [[ -z "$objective_line" || -z "$first_h2_line" || "$objective_line" -ge "$first_h2_line" ]]; then
    fail "$relative" "objective callout must appear before the first H2"
  fi

  if rg -q '^## (Learning Objective|Opening Question|Entering State|Misconception|Crux|Owned Concepts|Borrowed Concepts|Deferred Concepts|Engineering Decision|Dossier Delta|What This Chapter Adds|Transfer Task|Downstream Dependency|Acceptance Test)$' "$file"; then
    fail "$relative" "editorial metadata appears as a manuscript heading"
  fi

  lab_end_line="$({
    awk '
      $0 == "::: {.callout-lab}" { in_lab = 1; next }
      in_lab && $0 == ":::" { print NR; exit }
    ' "$file"
  })"

  if [[ -z "$lab_end_line" ]]; then
    fail "$relative" "lab callout is not closed"
  elif tail -n "+$((lab_end_line + 1))" "$file" | rg -q '[^[:space:]]'; then
    fail "$relative" "reader-facing content follows the lab"
  fi

  if [[ "$objective_count" == 1 && "$decision_count" == 1 && "$lab_count" == 1 ]]; then
    printf 'PASS  %s\n' "$relative"
  fi
done

if (( failures > 0 )); then
  printf '\n%s chapter-contract check(s) failed.\n' "$failures" >&2
  exit 1
fi

printf '\nAll %s chapter contracts pass.\n' "${#chapters[@]}"

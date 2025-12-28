#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:-walmart-2025-12-27.json}"
OUTPUT="${2:-walmart-2025-12-27.normalized.json}"

if [[ ! -f "$INPUT" ]]; then
  echo "Fichier introuvable: $INPUT" >&2
  exit 1
fi

./normalize_walmart.py --input "$INPUT" --output "$OUTPUT"

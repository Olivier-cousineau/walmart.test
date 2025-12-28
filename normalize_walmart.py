#!/usr/bin/env python3
"""Normalize Walmart product export data into a consistent schema."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

PRICE_RE = re.compile(r"(\d+[\d\s]*[,\.]\d+)")
RATING_RE = re.compile(r"([\d.,]+)\s*sur\s*5", re.IGNORECASE)
REVIEWS_RE = re.compile(r"(\d+)\s*avis", re.IGNORECASE)


@dataclass
class Variant:
    url: Optional[str]
    image_url: Optional[str]


@dataclass
class NormalizedProduct:
    url: Optional[str]
    title: Optional[str]
    brand: Optional[str]
    badge: Optional[str]
    image_url: Optional[str]
    price_current: Optional[float]
    price_original: Optional[float]
    savings: Optional[float]
    rating: Optional[float]
    review_count: Optional[int]
    delivery_text: Optional[str]
    delivery_eta: Optional[str]
    options_text: Optional[str]
    variants: List[Variant]
    raw: Dict[str, Any]


def parse_decimal(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    match = PRICE_RE.search(value)
    if not match:
        return None
    number = match.group(1)
    number = number.replace(" ", "").replace(",", ".")
    try:
        return float(number)
    except ValueError:
        return None


def parse_rating(text: Optional[str]) -> Optional[float]:
    if not text:
        return None
    match = RATING_RE.search(text)
    if not match:
        return None
    value = match.group(1).replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return None


def parse_review_count(text: Optional[str], fallback: Optional[str]) -> Optional[int]:
    if text:
        match = REVIEWS_RE.search(text)
        if match:
            return int(match.group(1))
    if fallback and fallback.isdigit():
        return int(fallback)
    return None


def collect_variants(item: Dict[str, Any]) -> List[Variant]:
    variants: List[Variant] = []
    for index in range(1, 6):
        suffix = "" if index == 1 else f" ({index})"
        url = item.get(f"z-2 href{suffix}")
        image_url = item.get(f"br-100 src{suffix}")
        if url or image_url:
            variants.append(Variant(url=url, image_url=image_url))
    return variants


def normalize_item(item: Dict[str, Any]) -> NormalizedProduct:
    rating_text = item.get("w_q67L (4)")
    return NormalizedProduct(
        url=item.get("w-100 href"),
        title=item.get("normal") or item.get("w_q67L"),
        brand=item.get("mb1"),
        badge=item.get("w_SrYk"),
        image_url=item.get("absolute src"),
        price_current=parse_decimal(item.get("mr1")),
        price_original=parse_decimal(item.get("strike")),
        savings=parse_decimal(item.get("lh-copy")),
        rating=parse_rating(rating_text),
        review_count=parse_review_count(rating_text, item.get("sans-serif")),
        delivery_text=item.get("ff-text-wrapper"),
        delivery_eta=item.get("b"),
        options_text=item.get("f7"),
        variants=collect_variants(item),
        raw=item,
    )


def normalize_data(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [asdict(normalize_item(item)) for item in items]


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize Walmart product export data.")
    parser.add_argument(
        "--input",
        default="walmart-2025-12-27.json",
        help="Path to input JSON file",
    )
    parser.add_argument(
        "--output",
        default="walmart-2025-12-27.normalized.json",
        help="Path to output JSON file",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    with input_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    normalized = normalize_data(data)

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(normalized, handle, ensure_ascii=False, indent=2)

    print(f"Normalized {len(normalized)} items -> {output_path}")


if __name__ == "__main__":
    main()

# Workflow de normalisation Walmart

Ce workflow standardise les données en français en exposant un schéma stable avec :

- `image` (alias de l'image principale)
- `prix_reduit` (prix actuel)
- `prix_regulier` (prix avant réduction)

## Étapes

1. **Préparer le fichier source**
   - Placez le fichier JSON brut (ex. `walmart-2025-12-27.json`) dans le même dossier.

2. **Lancer la normalisation**
   - **Option A (workflow manuel prêt à lancer)** :
     ```bash
     ./workflow_normalisation.sh walmart-2025-12-27.json \
       walmart-2025-12-27.normalized.json
     ```
   - **Option B (appel direct du script)** :
   ```bash
   ./normalize_walmart.py --input walmart-2025-12-27.json \
     --output walmart-2025-12-27.normalized.json
   ```

3. **Valider le résultat (optionnel)**
   ```bash
   python - <<'PY'
   import json
   from pathlib import Path

   data = json.loads(Path("walmart-2025-12-27.normalized.json").read_text())
   sample = data[0]
   for key in ("image", "prix_reduit", "prix_regulier"):
       print(key, "=>", sample.get(key))
   PY
   ```

## Schéma normalisé (extrait)

```json
{
  "url": "https://www.walmart.ca/...",
  "title": "Haut à capuchon...",
  "brand": "George",
  "badge": "Liquidation",
  "image_url": "https://i5.walmartimages.ca/...jpg",
  "image": "https://i5.walmartimages.ca/...jpg",
  "price_current": 5.0,
  "price_original": 7.0,
  "prix_reduit": 5.0,
  "prix_regulier": 7.0,
  "savings": 2.0,
  "rating": 4.3,
  "review_count": 20
}
```

## Notes

- `prix_reduit` et `prix_regulier` sont des alias français de `price_current` et
  `price_original` pour faciliter l'export.
- `image` est un alias de `image_url`.

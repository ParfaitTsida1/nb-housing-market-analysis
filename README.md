# data-analysis

Projet d'analyse de données.

## Structure

```
data/raw/         Données brutes (jamais modifiées)
data/processed/   Données nettoyées et transformées
notebooks/        Notebooks Jupyter d'exploration
src/              Code réutilisable (nettoyage, analyse)
reports/figures/  Graphiques et rapports produits
```

## Démarrage

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
jupyter lab
```

## Notes

- Les fichiers de données ne sont pas versionnés (voir `.gitignore`).
  Seuls les dossiers sont conservés grâce aux fichiers `.gitkeep`.

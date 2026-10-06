"""Fonctions réutilisables pour l'analyse de données."""
from pathlib import Path

import pandas as pd

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
DATA_PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"


def load_csv(name: str) -> pd.DataFrame:
    """Charge un fichier CSV depuis data/raw."""
    return pd.read_csv(DATA_RAW / name)


def save_processed(df: pd.DataFrame, name: str) -> Path:
    """Enregistre un DataFrame nettoyé dans data/processed."""
    path = DATA_PROCESSED / name
    df.to_csv(path, index=False)
    return path

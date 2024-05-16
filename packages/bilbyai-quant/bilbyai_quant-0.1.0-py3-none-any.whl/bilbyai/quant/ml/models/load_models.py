from os import path

from joblib import load

MODELS_DIR = path.dirname(__file__)


def load_demandsupply_impact_model():
    return load(path.join(MODELS_DIR, "impact_model_v3.joblib"))


def load_demandsupply_model():
    return load(path.join(MODELS_DIR, "demand_supply_model_v3.joblib"))

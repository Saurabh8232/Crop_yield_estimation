import math

from backend.config import CATEGORICAL_FEATURES, FEATURES, NUMERIC_FEATURES


def validate_inputs(payload: object) -> tuple[dict | None, list[str]]:
    if not isinstance(payload, dict):
        return None, ["Request body must be a JSON object."]

    errors = []
    missing = [name for name in FEATURES if name not in payload]
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}.")

    for name in NUMERIC_FEATURES:
        if name not in payload:
            continue
        value = payload[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{name} must be a number.")
        elif not math.isfinite(value):
            errors.append(f"{name} must be finite.")

    for name in CATEGORICAL_FEATURES:
        if name not in payload:
            continue
        if not isinstance(payload[name], str) or not payload[name].strip():
            errors.append(f"{name} must be a non-empty string.")

    return (payload, errors) if errors else (payload, [])

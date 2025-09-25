from typing import Dict, Any, Tuple


REQUIRED_METRIC_FIELDS = ("serverId", "cpu_usage", "ram_usage", "disk_space", "temperature")


def validate_metric_payload(payload: Dict[str, Any]) -> Tuple[bool, str | None]:
    if not isinstance(payload, dict):
        return False, "Payload inválido"
    for f in REQUIRED_METRIC_FIELDS:
        if f not in payload:
            return False, f"Falta el campo requerido: {f}"
    numeric_fields = ("cpu_usage", "ram_usage", "disk_space", "temperature")
    for f in numeric_fields:
        try:
            float(payload[f])
        except Exception:
            return False, f"El campo {f} debe ser numérico"
    for f in ("cpu_usage", "ram_usage", "disk_space"):
        v = float(payload[f])
        if v < 0 or v > 100:
            return False, f"El campo {f} debe estar entre 0 y 100"
    return True, None


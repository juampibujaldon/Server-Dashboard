from typing import Dict, Any, Tuple


REQUIRED_METRIC_FIELDS = ("server_id", "cpu_usage", "ram_usage", "disk_space", "temperature")
ALLOWED_METRIC_UPDATE_FIELDS = (
    "server_id",
    "cpu_usage",
    "ram_usage",
    "disk_space",
    "temperature",
    "sent_at",
)


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


def validate_metric_update_payload(payload: Dict[str, Any]) -> Tuple[bool, str | None]:
    if not isinstance(payload, dict):
        return False, "Payload inválido"
    if not payload:
        return False, "No hay campos para actualizar"
    for field in payload:
        if field not in ALLOWED_METRIC_UPDATE_FIELDS:
            return False, f"Campo no permitido: {field}"

    numeric_fields = ("cpu_usage", "ram_usage", "disk_space", "temperature")
    for field in numeric_fields:
        if field in payload:
            try:
                float(payload[field])
            except Exception:
                return False, f"El campo {field} debe ser numérico"
            if field in ("cpu_usage", "ram_usage", "disk_space"):
                value = float(payload[field])
                if value < 0 or value > 100:
                    return False, f"El campo {field} debe estar entre 0 y 100"

    if "server_id" in payload and not payload["server_id"]:
        return False, "El campo server_id no puede estar vacío"

    return True, None

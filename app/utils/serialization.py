from typing import Dict, Any


def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    out = {k: v for k, v in doc.items() if k != "_id"}
    if "_id" in doc:
        out["id"] = str(doc["_id"])  # JSON-safe id
    return out


def serialize_many(docs: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    return [serialize_doc(d) for d in docs]


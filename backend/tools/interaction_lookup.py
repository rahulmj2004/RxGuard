from itertools import combinations

from django.db import DatabaseError

from apps.interactions.models import Drug, DrugInteraction


DEFAULT_KB_VERSION = "test-v1"


def get_interaction(
    drug_a_id: int,
    drug_b_id: int,
    kb_version: str = DEFAULT_KB_VERSION,
):
    """
    Look up one drug-drug interaction.

    Drug order does not matter.

    Returns a structured result and never interprets
    absence of a database row as clinical safety.
    """

    # Validate IDs
    if not isinstance(drug_a_id, int) or not isinstance(drug_b_id, int):
        return {
            "status": "INVALID_DRUG_ID",
            "found": False,
            "drug_a_id": drug_a_id,
            "drug_b_id": drug_b_id,
            "message": "Drug IDs must be integers.",
            "interaction": None,
        }

    if drug_a_id <= 0 or drug_b_id <= 0:
        return {
            "status": "INVALID_DRUG_ID",
            "found": False,
            "drug_a_id": drug_a_id,
            "drug_b_id": drug_b_id,
            "message": "Drug IDs must be positive integers.",
            "interaction": None,
        }

    # Canonicalize pair order.
    drug_a_id, drug_b_id = sorted([drug_a_id, drug_b_id])

    pair_key = f"{drug_a_id}:{drug_b_id}"

    try:
        interaction = (
            DrugInteraction.objects
            .select_related("drug_a", "drug_b")
            .filter(
                pair_key=pair_key,
                is_active=True,
            )
            .first()
        )

    except DatabaseError:
        # Fail closed if the database lookup itself fails.
        return {
            "status": "LOOKUP_FAILED",
            "found": False,
            "drug_a_id": drug_a_id,
            "drug_b_id": drug_b_id,
            "message": "Interaction lookup failed.",
            "interaction": None,
        }

    if interaction is None:
        return {
            "status": "NO_RECORDED_INTERACTION",
            "found": False,
            "drug_a_id": drug_a_id,
            "drug_b_id": drug_b_id,
            "message": f"No interaction recorded in DDInter {kb_version}.",
            "interaction": None,
        }

    return {
        "status": "INTERACTION_RECORDED",
        "found": True,
        "drug_a_id": drug_a_id,
        "drug_b_id": drug_b_id,
        "message": None,
        "interaction": {
            "interaction_id": interaction.interaction_id,
            "drug_a": {
                "id": interaction.drug_a.id,
                "molecule_id": interaction.drug_a.molecule_id,
                "generic_name": interaction.drug_a.generic_name,
            },
            "drug_b": {
                "id": interaction.drug_b.id,
                "molecule_id": interaction.drug_b.molecule_id,
                "generic_name": interaction.drug_b.generic_name,
            },
            "severity": interaction.severity,
            "description": interaction.description,
            "source": interaction.source,
            "source_record_id": interaction.source_record_id,
            "kb_version": interaction.kb_version,
        },
    }


def check_all_pairs(
    drug_ids: list[int],
    kb_version: str = DEFAULT_KB_VERSION,
):
    """
    Check every unique drug pair.

    Duplicate drug IDs are removed before generating pairs.
    Drug pair ordering does not matter.
    """

    if not isinstance(drug_ids, list):
        return {
            "status": "INVALID_DRUG_LIST",
            "found": False,
            "message": "drug_ids must be a list of integers.",
            "results": [],
        }

    if not all(isinstance(drug_id, int) for drug_id in drug_ids):
        return {
            "status": "INVALID_DRUG_LIST",
            "found": False,
            "message": "All drug IDs must be integers.",
            "results": [],
        }

    unique_drug_ids = sorted(set(drug_ids))

    results = []

    for drug_a_id, drug_b_id in combinations(unique_drug_ids, 2):
        result = get_interaction(
            drug_a_id,
            drug_b_id,
            kb_version=kb_version,
        )
        results.append(result)

    return results
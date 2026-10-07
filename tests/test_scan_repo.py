"""Run: python tests/test_scan_repo.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/kenya-data-protection/scripts"))
from scan_repo import field_category, scan  # noqa: E402

# Kenya-specific sensitive data, and code words that must not match.
assert field_category("maritalStatus") == "sensitive: marital status"
assert field_category("next_of_kin") == "sensitive: family details"
assert field_category("parentPhone") == "sensitive: family details"
assert field_category("medicalNotes") == "sensitive: health"
assert field_category("dateOfBirth") == "children"
assert field_category("nationalIdNumber") == "identity numbers"
for code_word in ["children", "parentNode", "parent_id", "isMobile", "message", "page", "trace"]:
    assert field_category(code_word) is None, code_word

fields, services, regions, notices = scan(ROOT / "evals/files/acorns-parent-app")
assert "allergies" in fields["sensitive: health"]
assert "maritalStatus" in fields["sensitive: marital status"]
assert {"AWS", "Firebase / Google Cloud", "Mixpanel", "Sentry", "Africa's Talking"} <= set(services)
assert "infra/main.tf" in services["AWS"]
assert "eu-west-1" in regions
assert notices == []
print("ok")

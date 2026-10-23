"""Run official lint + SDK schema validation with a checkout-local cache."""
from pathlib import Path
import json
import os
import sys
from genvm_linter.lint import lint_contract
from genvm_linter.validate import artifacts
from genvm_linter.validate.validator import validate_contract

ROOT = Path(__file__).resolve().parents[1]
artifacts.CACHE_DIR = Path(os.environ.get("GLTEST_SDK_CACHE", ROOT / ".cache" / "gltest-direct"))
os.environ["GENVM_VERSION"] = "v0.2.16"
contract = ROOT / "contracts" / "translation_gate.py"
lint = lint_contract(contract)
validation = validate_contract(contract)
result = {"lint": lint.to_dict(), "validation": validation.to_dict()}
print(json.dumps(result, indent=2, ensure_ascii=True))
if lint.ok and validation.ok:
    target = ROOT / "docs" / "contract-schema.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(validation.schema, indent=2) + "\n", encoding="utf-8")
    sys.exit(0)
sys.exit(1)

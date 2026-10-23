# Threat model

## Boundaries

The client chooses terms before submission. The named translator accepts those terms by submitting. Neither party gets a privileged override of an evaluated decision. Any caller can trigger evaluation of the current submitted attempt. There is no administrator and no fund custody.

The contract is an acceptance signal, not a complete marketplace. Sybil resistance, work deadlines, collateral, refunds and commercial enforcement are outside its scope.

## Controls and residual risks

| Threat | Control | Residual risk |
| --- | --- | --- |
| Client changes criteria after delivery | No update method; source and rules fixed at creation | Client may publish unreasonable terms initially; translator must review them |
| Attacker submits someone else's work | Exact sender-address check against nominated translator | A compromised translator account can still submit |
| Client refuses to evaluate | Permissionless evaluation | Someone still needs to pay applicable fees; no automatic scheduling |
| Repeated reroll until a favorable result | Submitted delivery locked; terminal outcomes fixed; changed revisions limited to 1–3 attempts | Cosmetic edits still consume a new permitted attempt; consensus rotations are protocol behavior |
| Leader returns valid JSON with a false decision | Validator independently evaluates original evidence and compares all decision flags | Correlated models can agree on the same mistake |
| Model invents prose reasoning | No model prose is persisted; reason codes derive from validated booleans | Flags provide coarse diagnostics, not sentence-level explanations |
| Missing or invented output fields | Exact IDs and flag keys, actual booleans, strict duplicate-key rejection | Well-formed output can still be substantively wrong |
| Empty/missing delivery or literal term violation | Deterministic gate before AI | Normalized substring matching can overmatch or underrepresent linguistic intent |
| Prompt injection in source/delivery/rules | JSON-encoded data boundary, fixed rubric, explicit instruction/data separation, independent validators | This is defense in depth, not demonstrated injection immunity; shared model failures remain possible |
| Unbounded execution workload | Per-field, segment, glossary and retry limits; lexical failures skip LLM | Provider latency and current network resource pricing vary |
| Provider failure or unresolved consensus | No writes before successful result; pending attempt retained | Liveness is not guaranteed |
| Consumer accepts provisional state | Integration instructions require network finality | Integrator can still use the wrong network, job or transaction stage |

## Consensus choice

Exact agreement is required for all four booleans for every segment. This avoids numeric tolerances crossing an acceptance threshold, and avoids comparing free-form explanations that are expected to differ. The tradeoff is availability: borderline style or adequacy judgments can lead to unresolved consensus.

The validator is intentionally more than a schema check. It receives the original immutable evidence, runs its own assessment, validates that assessment's structure, and compares the resulting flags. The tests explicitly simulate a dissenting validator for each flag and reject a forged but correctly shaped leader result.

## Tests are not an audit

Direct Mode exercises actual SDK storage and calldata with synthetic provider responses. It cannot establish real model quality, provider diversity, production consensus performance, execution fees or prompt-injection resistance. Those require live multi-validator evaluations and adversarial multilingual datasets. No security audit is claimed.

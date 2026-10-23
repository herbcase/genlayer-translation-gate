# Validation evidence

## Local checks

- **41 tests passed** with `genlayer-test==0.29.2` Direct Mode and the declared GenLayer SDK runner, using Python 3.12.14.
- Official `genvm-linter==0.11.0` AST lint: **passed**, three checks.
- Official SDK schema validation: **passed**, eight public methods (five write, three view), no constructor arguments.
- Hosted Studionet schema extraction accepted the same source and exposed the same public methods.

Tests cover lifecycle and address permissions, immutable evaluated history, bounded revisions, prevention of identical resubmission, structural and literal checks, strict model-response parsing, unchanged state on malformed output, independent-validator disagreement on every decision flag, and rejection of a forged but correctly formatted leader answer.

The prompt-injection fixture tests data handling and decision wiring with a mocked response. It does not establish that real models resist injection.

## Live hosted Studio run

Network: **Studionet**, chain ID **61999**, RPC `https://studio.genlayer.com/api`.

Contract: `0xAFc70827e216828a2b5a7Bc72A3edB30306724B4`

Source SHA-256: `4ae36782d08ea7030a791e9bc74a8de43717d7971c5a403d45c15284f8d10b28`

A dedicated disposable development account deployed the contract. It is not the user's Portal-linked wallet. This demonstrates runtime execution and is not a claim of a wallet-attributed Portal deployment reward.

All six transactions below reached **FINALIZED**. The full public snapshot, selected execution results, validator votes and historical readbacks are in [deployments/studionet.json](../deployments/studionet.json). `leaderOnly` was false; LLM calls in this hosted run were not locally mocked.

| Step | Transaction | Observed outcome |
| --- | --- | --- |
| Deploy | `0xf6ffd62e409e2c48f34dfc9937065a601ed01124e6cd75ee774ba94cf49edf04` | Successful deployment; `get_next_id()` returned 1 |
| Create job 1 | `0xc964190240ca05a6a83d53ca254ac97e93b9f387baf9ca9f63ffc68077d93258` | Fixed English→Korean product-copy task |
| Submit attempt 1 | `0xe8ea940174d821f96d58494c8645750feda64b75e272813f19cdc4527d446e52` | Translation incorrectly changed 24 hours to 48 hours |
| Evaluate attempt 1 | `0x06a5bda955236844e4be4fe4d459c9d169c7c2f99df2a48e19bbeac991c23ca5` | `REVISION_REQUIRED`, `headline.meaning=false`, reason `AI_MEANING_FAILED` |
| Submit attempt 2 | `0x4579de1fda424f5642b1fcc460ab51e72a8dabbc13f7511a0f1628dcaa80aca9` | Corrected to 24 hours |
| Evaluate attempt 2 | `0xe50664c7bb6f51d70cfe599891f9aa5292b8240326a8e6e3c22bc287cb7389b0` | `ACCEPTED`, all semantic flags true |

Readback retained both attempt 1 (`REVISION_REQUIRED`) and attempt 2 (`ACCEPTED`) without overwriting the first report. The deployed source was fetched back from the RPC and its hash matched the local source.

### Disagreement was observed

The first AI evaluation's last-round votes were **3 AGREE, 1 DISAGREE, 1 IDLE**. The corrected evaluation's were **3 AGREE, 2 IDLE**. Both reached the network's majority-agreement outcome and finalized. This is not unanimous agreement and should not be presented as such. The result illustrates an actual hosted test, not a guarantee of accuracy or availability on other examples.

Studionet is a hosted development environment. This is not a Bradbury or mainnet deployment, and hosted state may be reset.

## Independently read it back

Optional Node.js verification (no wallet required):

```bash
pnpm install --frozen-lockfile
node scripts/verify_deployment.mjs
```

This checks the live chain ID, deployed-source hash against both evidence and the local contract, final job status, and both historical attempts. If Studio resets, the script should fail rather than imply the recorded deployment still exists.

## Not established by these checks

Production throughput or fees, general translation accuracy, adversarial prompt-injection resistance, maximum-sized real-model workloads, mainnet compatibility, or the success of protocol-level appeals. No production audit is claimed.

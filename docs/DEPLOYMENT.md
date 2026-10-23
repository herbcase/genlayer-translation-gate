# Deployment and manual verification

## Prepare

1. Run `python -m pytest -q` and `python scripts/check_contract.py`.
2. Open the official [GenLayer Studio](https://studio.genlayer.com/).
3. Select the intended development network and an appropriate test wallet. Obtain test GEN through the network's official faucet if required.
4. Load `contracts/translation_gate.py`. Deploy with **no constructor arguments**. Preserve the runner declaration in the first line.
5. Wait for a successful deployment outcome and read `get_next_id()`: it must return `1`. Record the network, address and transaction receipt before claiming a deployment.

Stable Studionet, Studio development previews and Bradbury are different deployments. A runner accepted on one may not be installed on another. Check the official [network configuration](https://docs.genlayer.com/developers/intelligent-contracts/deploying/network-configuration) rather than changing endpoints blindly.

## Run the sample

Use two test accounts: client A and translator B. The sample payloads are in `examples/product-copy.json`.

1. As A, call `create_job(B, JSON.stringify(sample.source), JSON.stringify(sample.rules), 2)`. Record its returned ID.
2. As B, call `submit(id, JSON.stringify(sample.material_error_delivery))`.
3. As either account, call `evaluate(id)`. Wait for the network's decided outcome; inspect the actual execution result as well as lifecycle status. `get_job(id)` should report `REVISION_REQUIRED` if independent validators agree the 48-hour claim is a material error.
4. As B, call `submit(id, JSON.stringify(sample.good_delivery))`.
5. Evaluate again. If validators agree all flags pass, `get_job(id)` becomes `ACCEPTED`.
6. Read `get_attempt(id, 1)` and `get_attempt(id, 2)` to verify the first delivery and result were retained.
7. Attempt another `evaluate(id)` or `submit(...)`: each must fail because the job is terminal.

For a literal-only check, create another job and submit `literal_error_delivery`. Evaluation should request revision for `MISSING_GLOSSARY_TERM` without making an LLM call.

If evaluation cannot reach consensus, do not describe it as a translation rejection. The current attempt must remain `SUBMITTED`; inspect network receipts/logs and report that result honestly.

## Evidence to retain

- Network and chain ID
- Contract address and source SHA-256
- Deployment transaction and successful execution receipt
- `create_job`, `submit` and `evaluate` transaction identifiers
- Finalized state readback and both historical attempts
- Actual validator outcomes, including disagreements or provider errors

No private keys, seed phrases or access tokens belong in repository evidence.

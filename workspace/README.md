# Translation Gate workspace

A testnet web interface for the existing Translation Gate Intelligent Contract. It supports creating a one-segment assignment, reading assignments, submitting and revising translations, requesting evaluation, and reading evaluated history. The source, rules, translator and maximum attempts are fixed in the contract. The client and translator must be different wallet addresses. This app does not hold keys or pay fees on a visitor's behalf.

The updated contract is deployed on GenLayer Studionet at `0x2e1C4151d932a8d74854B86dEb03f7191F2332d8`. Studionet state can reset. The app imports `genlayer-js@1.1.8` from esm.sh at runtime and requires browser access to that service and the Studionet RPC. A previous version was submitted as an Intelligent Contract; this project adds the interface and changes the contract to request structured JSON responses from the model.

## Review path

1. Open assignment 1 without connecting a wallet. It may no longer exist after a testnet reset. The job contains the updated contract's live test: “Keep refrigerated after opening” was translated into Korean and accepted after independent AI consensus.
2. With two separate test wallets on Studionet, connect the client wallet. Enter the other wallet as translator, fill the brief and create the assignment. Wait for consensus and inspect the transaction in the explorer for its job ID.
3. Connect the translator wallet, open the assignment and submit a translation. Wait for transaction confirmation and reload the job.
4. Request evaluation and wait for consensus. Reload to see the result. If revision is required, the translator can submit a changed version, then request another evaluation. Evaluated attempts are retained in the history.

Wallet confirmations, RPC and consensus can fail independently. A transaction submission is not a successful execution. Always inspect the transaction and refresh the on-chain job. The app does not claim an economic payout, production availability or human-level translation accuracy. Do not submit private source material.

The updated contract passed 41 local tests and a hosted Studionet lifecycle using separate disposable test accounts. Transaction hashes and the result are in [v2-test-evidence.json](v2-test-evidence.json). The hosted lifecycle used a script, not a browser wallet; the browser wallet write path still needs independent verification. The original contract's historical test is documented at https://github.com/herbcase/genlayer-translation-gate/blob/main/docs/VALIDATION.md and uses a different contract address.


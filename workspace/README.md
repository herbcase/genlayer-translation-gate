# Translation Gate workspace

A testnet web interface for the existing Translation Gate Intelligent Contract. It supports creating a one-segment assignment, reading assignments, submitting and revising translations, requesting evaluation, and reading evaluated history. The source, rules, translator and maximum attempts are fixed in the contract. The client and translator must be different wallet addresses. This app does not hold keys or pay fees on a visitor's behalf.

The contract is deployed on GenLayer Studionet at `0xAFc70827e216828a2b5a7Bc72A3edB30306724B4`. Studionet state can reset. The app imports `genlayer-js@1.1.8` from esm.sh at runtime and requires browser access to that service and the Studionet RPC. The contract was previously submitted as an Intelligent Contract; this project adds the interactive interface and workflow.

## Review path

1. Open assignment 1 without connecting a wallet. It may no longer exist after a testnet reset. Compare its report and history with [the recorded test](https://github.com/herbcase/genlayer-translation-gate/blob/main/docs/VALIDATION.md).
2. With two separate test wallets on Studionet, connect the client wallet. Enter the other wallet as translator, fill the brief and create the assignment. Wait for consensus and inspect the transaction in the explorer for its job ID.
3. Connect the translator wallet, open the assignment and submit a translation. Wait for transaction confirmation and reload the job.
4. Request evaluation and wait for consensus. Reload to see the result. If revision is required, the translator can submit a changed version, then request another evaluation. Evaluated attempts are retained in the history.

Wallet confirmations, RPC and consensus can fail independently. A transaction submission is not a successful execution. Always inspect the transaction and refresh the on-chain job. The app does not claim an economic payout, production availability or human-level translation accuracy. Do not submit private source material.

Contract code and prior test evidence: https://github.com/herbcase/genlayer-translation-gate. The previous test used two separate disposable test accounts, 41 local tests, and a hosted Studio lifecycle; that historical evidence does not verify this web UI.

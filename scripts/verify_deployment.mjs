// Read-only verification. No wallet, private key or transaction signing required.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';

const root = new URL('../', import.meta.url);
const evidence = JSON.parse(readFileSync(new URL('deployments/studionet.json',root),'utf8'));
const client = createClient({chain:studionet});
const watchdog = setTimeout(() => {console.error('Network verification timed out');process.exit(1);},55000);
try {
  assert.equal(await client.getChainId(), evidence.chainId);
  const deployedCode = await client.getContractCode(evidence.contractAddress);
  const hash = createHash('sha256').update(deployedCode).digest('hex');
  assert.equal(hash,evidence.sourceSha256,'Deployed source differs from evidence');
  const localCode = readFileSync(new URL('contracts/translation_gate.py',root));
  assert.equal(createHash('sha256').update(localCode).digest('hex'),hash,'Local source differs from deployment');
  const job = JSON.parse(await client.readContract({address:evidence.contractAddress,functionName:'get_job',args:[1n]}));
  const attempts = [];
  for(const n of [1n,2n]) attempts.push(JSON.parse(await client.readContract({address:evidence.contractAddress,functionName:'get_attempt',args:[1n,n]})));
  assert.equal(job.status,'ACCEPTED');
  assert.equal(attempts[0].status,'REVISION_REQUIRED');
  assert.equal(attempts[0].report.assessment.headline.meaning,false);
  assert.equal(attempts[1].status,'ACCEPTED');
  assert.equal(attempts[1].report.passed,true);
  console.log(JSON.stringify({network:evidence.network,contract:evidence.contractAddress,sourceSha256:hash,jobStatus:job.status,attemptStatuses:attempts.map(a=>a.status)},null,2));
} finally {clearTimeout(watchdog);}

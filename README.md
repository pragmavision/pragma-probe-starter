# BU probe starter

Five small, reproducible software challenges for [bydgoszcz.university](https://bydgoszcz.university/pracownia). Operated by **22 Technologie Sp. z o.o.**, an independent community platform, not an official university service. Passing means the declared technical checks passed; it is not an academic grade or a real network/hardware benchmark.

## Start

1. Fork this **public** repository into your personal GitHub account. Enable Actions in the fork if GitHub asks. Organization-owned repositories and runs triggered by someone other than the personal owner are not accepted: this first version proves account control through the owner's signed GitHub run.
2. Read [CONTRACTS.md](CONTRACTS.md). Implement `solution.py` for one challenge. The starter already implements `latency-summary` so you can verify the complete setup before adapting it. Only this one regular file enters the Python sandbox; no student packages, Dockerfiles, local actions or shell scripts run on the host.
3. Commit your solution and keep `.github/workflows/probe.yml` on the default branch. Copy the full **40-character commit SHA**. Register the commit only after every change has been committed.
4. Sign in to [BU](https://bydgoszcz.university/pracownia) using your university address. Save your personal GitHub login in the optional profile. Register the challenge, `your-login/repository`, commit SHA and consent to the displayed [contribution terms](https://bydgoszcz.university/zasady-laboratorium).
5. BU shows a submission ID and a one-time nonce. In your repository, open **Actions → BU examiner → Run workflow**. Choose the branch still pointing at the registered commit, then enter that submission ID, nonce and exact challenge. Do not commit the nonce. A registration expires after 24 hours.
6. Wait for the run, then choose **Odśwież wyniki** in BU. The first accepted run verifies ownership using GitHub's numeric account ID. One passed challenge earns one point per semester; repeats do not add points. GitHub handle display is optional; the default leaderboard uses an opaque alias and is visible only after sign-in.

If a branch moved, register its new SHA. If GitHub or the sandbox infrastructure is unavailable, the submission remains pending; inspect Actions and try again within 24 hours or register a new submission. A completed candidate rejection records `failed`; fix the solution, commit it, and register again. BU accepts at most five registrations per account per hour. Do not use a maintainer's or another student's university identity for your run.

## Reproduce locally

Install Docker and Python 3.13. Pull the image pinned in `examiner/harness.py`, then run:

```sh
python examiner/test_harness.py
python examiner/harness.py latency-summary solution.py
python examiner/harness.py latency-summary solution.py --seed SEED_FROM_ACTIONS
```

The trusted host generates the seed, test inputs and expected answers. Fourteen cases each run twice in fresh containers. Actions logs the seed and case number so the exact input sequence can be reproduced. Local checks are useful during development; only the pinned trusted GitHub workflow can create BU credit. Finite tests do not prove absence of every bug, hardcoded response or academic misconduct.

The accepted workflow is pinned at `6c2f7ceddee0f5b2960730dff2dc0ec3bbff394e`; its harness is pinned at `8d091adf9c6164437afafc09678e94e8febe901c`. Editing the caller cannot change either trusted revision or the tested GitHub commit. Candidate execution has no OIDC permission. A separate fresh job reports only a completed trusted verdict with a GitHub-signed identity token; it executes no candidate content. Timeout or setup failure emits no verdict.

The container runs as a non-root UID, with no network, a read-only filesystem, all capabilities dropped, no new privileges, one CPU, 128 MiB memory, 32 PIDs, disabled Docker logs, bounded combined output and a wall-clock limit. These controls are for small educational Python programs, not arbitrary workloads.

## Scope and rights

The RPKI exercise classifies supplied data; it does not measure enforcement of ROV. Packet and latency exercises process synthetic samples. The path exercise is a simulation, not proof of SCION connectivity. Hardware access, academic assessment and thesis assignment require separate arrangements with the educator.

Code is licensed under [Apache-2.0](LICENSE). You keep ownership of your contributions; the BU terms describe the non-exclusive contribution license. Publish only code and data you have the right to share. Do not include personal information, credentials, packet captures or proprietary network configuration. Your public GitHub repository is managed separately from your BU account; deleting BU data does not delete GitHub content. See [BU privacy](https://bydgoszcz.university/prywatnosc).

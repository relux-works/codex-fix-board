# TASK-261007-3v81ko — fix-exec-tmpdir-cleanup: integration completion log

Integration attempted under leak-complete-note.md (tb-R144). No repository files were edited, no builds or tests ran, and no temporary directories were created. Previously attached hosted precheck 3 is existing evidence; this run independently verified only the landing checks below.

### `git fetch origin relux/main`

Exit code: 0

```text
From github.com:ivanopcode/codex
 * branch                relux/main -> FETCH_HEAD
```
### `git merge-base --is-ancestor e0eff057620104a416080da616256ee7f32bda1b origin/relux/main`

Exit code: 0

```text
(no output)
```

### `git diff --name-only 2f7ec5e30babb9dff4f00132ad9fd384663930b0 e0eff057620104a416080da616256ee7f32bda1b`

Exit code: 0

```text
.github/workflows/relux-ci.yml
```

### `git verify-commit e0eff057620104a416080da616256ee7f32bda1b`

Exit code: 0

```text
Good "git" signature for oparin@me.com with ED25519 key SHA256:PBVcYk4kqzAPUBpSyIYS8ODWX8Nqd7a5fuzGD2F8hqs
```

### `task-board worktree complete STORY-261007-1cpzdo --cr TASK-261007-3v81ko --revision 3 --landed-commit e0eff057620104a416080da616256ee7f32bda1b`

Exit code: 1

```text
code_landing_tree_mismatch: the landed tree differs from the accepted candidate; historical caller bases cannot authorize a different tree; use worktree prepare-landed-review, normal producer handoff and a new exact-tree accept_cr
  candidate_tree: 2f7ec5e30babb9dff4f00132ad9fd384663930b0
  cr_id: CR-TASK-261007-3v81ko-3
  declared_commit: e0eff057620104a416080da616256ee7f32bda1b
  landed_tree: bde782b85ddbc8536536d0747b3917d0f24e1951
  protected_oid: e0eff057620104a416080da616256ee7f32bda1b
  protected_ref: refs/heads/relux/main
  remote_url: ssh://git@github.com/ivanopcode/codex
  resolved_commit: e0eff057620104a416080da616256ee7f32bda1b
```

Result: completion refused (code_landing_tree_mismatch). All three landing checks passed; the candidate-to-landing diff lists only .github/workflows/relux-ci.yml. The completion gate nevertheless requires an exact accepted tree and refused the CI-only tree difference. No retry: the refusal does not report a resumable phase. No handoff, integrate, checkpoint, or further status mutation was invoked. The task remains integrating; no done status is claimed.

# TASK-260929-36bvsc integration preconditions — CR rev 2 (RUN-261006-09d07d)

## Top finding

Accepted candidate rev 2 is intact and landable: the worktree tree is byte-identical to the
accepted candidate tree `cf567d98480d05428ed9dea58f66306dbf030ff6` (TREE_MATCH via temp index),
on the unchanged Story tip `812b8037a8`, with exactly the 12 accepted candidate paths
uncommitted. Review verdict rev 2 is accept (3/3 panels accept, 3/3 surface rows held, empty
findings, recording confirmed). Checklist is 17/17. Hosted precheck 3 (run 37473988733, all
four lanes success; 5/5 narrowing mutants killed, 0 survivors) is reused bound to this
unchanged tree identity. No file was changed in this run. Landing act is runner-owned; this
run performed no `checkpoint`/`integrate` invocation.

## Landing preconditions confirmed

| # | Precondition | Evidence | Result |
|---|---|---|---|
| 1 | CR rev 2 accepted, board at `integrating` | `worktree status`: `TASK-260929-36bvsc rev 2 accepted (repository_delta=present, 12 changed path(s))`; `get`: `status=integrating` | PASS |
| 2 | Worktree tree equals accepted candidate tree | temp index (`git read-tree HEAD`, `git add -A`, `git write-tree`) → `cf567d98480d05428ed9dea58f66306dbf030ff6`, identical to handoff pin and review-verdict candidate | PASS (TREE_MATCH) |
| 3 | No producer commit; candidate UNCOMMITTED on recorded tip | `git rev-parse HEAD` → `812b8037a8a62bac3ce80f7035c9d9142ffea75b`; branch `task-board/story/STORY-260929-qvqmw2`; `git log` tip unchanged | PASS |
| 4 | Exactly the 12 accepted paths, no stray files | `git status --short`: 8 modified + 4 untracked, matching results.md file list; `diff --stat` 273+/34− plus 1015 new-file lines = 1288/34 as the verdict cites | PASS |
| 5 | Checklist complete | `get checklist`: 17/17 done | PASS |
| 6 | Review accepted with every surface row held | `TASK-260929-36bvsc_review-verdict-rev2.md`: verdict accept; panels 3otf1a/3oqq04/2gtrze all accept; findings []; surface 3/3 held; free hunts nonblocking; recording reviewer confirmed merge (RUN-261006-6631b1) | PASS |
| 7 | Hosted evidence green on this exact tree | Precheck 3 base run 37473988733 (snapshot 9ac368c5): core/app-server/lint/small success; mutants 37474019570, 37474048117, 37474077806, 37474108222, 37474137228 killed, 0 survivors; rev-2 handoff validation log green (fmt-check, clippy, 244 small tests) | PASS (reused, tree unchanged) |
| 8 | Landing route unambiguous | Sibling TASK-260929-2snjbb is `backlog` → non-final leaf; `worktree obligations`: rev 2 accepted, NEEDS checkpoint. Runner performs the bound landing synchronously after this run exits | NOTED (runner-owned) |
| 9 | Run write boundary respected | No worktree file modified (tree still matches); no control-root edits; only `/tmp` scratch reads and board mutations (status already `integrating`, this outcome, one note) | PASS |
| 10 | No pending directives | `spawn directives RUN-261006-09d07d`: none; run not goal-bound | PASS |

## Commands executed (this run, exit codes)

- `task-board m 'set_status(TASK-260929-36bvsc, status=integrating)'` → exit 0 (already integrating, no-op)
- `git rev-parse HEAD` / `git branch --show-current` / `git status --short` → exit 0
- temp-index tree computation → `cf567d98480d05428ed9dea58f66306dbf030ff6`, exit 0
- `git diff HEAD --stat`, `git log --oneline -3` → exit 0
- `wc -l` on 4 new files → 1015 total; `1288 = 273 + 1015` reconciled with verdict count
- Board reads: `get` (status/checklist/notes/outcomeResources/review/children), `worktree status`,
  `worktree obligations`, `worktree integrating`, `spawn directives` → all exit 0
- `task-board resource get` × 7 (results, handoff, verdict-rev2, recording-review-rev2,
  verdict-recorded-rev2, rev2-validation.log, mutants) → exit 0 each

## Not run, and why

- No `cargo`/`just` build or test in this run, by design: the tree must remain byte-identical
  to the accepted candidate, and hosted precheck 3 already ran the full core/app-server suites
  plus all 5 mutants on this exact tree (all green, 0 survivors). Re-running the fast lane
  would add no information and risks touching the tree. Evidence is reused bound to the
  verified-unchanged tree identity `cf567d98…`.
- `worktree integrating` classification is `indeterminate` here
  (`worktree_protected_authority_unavailable`: no SSH access to the authorized remote from
  this sandbox). This affects only the read-only trunk-comparison view, not the local
  preconditions above; the runner resolves authority at landing time.
- No `checkpoint`/`integrate` invoked: the bound landing is performed synchronously by the
  runner after this run exits, per the integration assignment.

## Out of contract (unchanged from handoff)

The consuming goal waiting policy (TASK-260929-2snjbb, E2) — explicitly out of scope per the
task description. All 5 AC rows and 3/3 surface rows covered with killed mutants each.

## Review notes carried forward (nonblocking, for E2 / stage 2e)

From the accepted rev-2 verdict; no action for this landing: snapshot contents/revision are
not proven linearly coherent (consumers must not treat revision equality as content equality);
AC4 fixture overlap is bounded (request a cross-thread latch-controlled provider read before
E2 relies on it); terminal-stdin/cancellation mailbox interplay needs integration tests when
stage 2e wires watcher→mailbox; `acknowledge_submitted` interrupt window is an unverified
robustness note. Change size 1288/34 exceeds the 800-line guideline (reviewability note only).

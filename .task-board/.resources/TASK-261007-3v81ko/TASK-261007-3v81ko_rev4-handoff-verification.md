# TASK-261007-3v81ko — fix-exec-tmpdir-cleanup: rev4 handoff verification

Followed leak-handoff-rev4-note.md. No repository files changed, no builds or local tests run.

Candidate tree: bde782b85ddbc8536536d0747b3917d0f24e1951, exactly the required landed tree.

## Commands run in this run

- mini-hosted-gate.sh: exit 0.
- Temporary-index git read-tree HEAD: exit 0.
- Temporary-index git add -A: exit 0.
- Temporary-index git write-tree: exit 0.
- Tree comparison: matched; verification script exit 0.
- git status --short: exit 0; existing candidate changes remain uncommitted.

Gate output:
```text
mini-hosted-gate: tree bde782b85ddbc8536536d0747b3917d0f24e1951 equals green tree 2f7ec5e30babb9dff4f00132ad9fd384663930b0 except .github/ only: 38038510297 ivanopcode TASK-261007-3v81ko/wip-3 (precheck 3, 5/5 mutants killed)
```

Tree verification output:
```text
git read-tree HEAD: exit 0
git add -A: exit 0
git write-tree: exit 0
bde782b85ddbc8536536d0747b3917d0f24e1951
Expected tree: bde782b85ddbc8536536d0747b3917d0f24e1951
Tree matches: True
Temporary index directory deleted.
```

## Evidence accepted from prior runs

TASK-261007-3v81ko_hosted-precheck-3.md: hosted relux-ci run 38038510297, lint/small/core/app-server all green, 932 small-lane tests passed, 5/5 mutants killed. This run did not rerun those tests. The mini gate accepts the current landed tree as differing from the recorded green candidate only under .github/.

AC2 bound remains explicit: Ctrl-C uses graceful shutdown but was not covered by a signal regression test. SIGTERM, SIGKILL and abort do not guarantee TempDir cleanup.

Temporary index directory was deleted before handoff. No real CODEX_HOME copied and no installed codex binary run. Existing checklist items left unchanged as instructed.

# TASK-260929-csyzcj (G1): review rev5 changes_requested. Prove a hard sub-1K bound on the interrupted item, then request precheck 16

The verdict is `TASK-260929-csyzcj_review-verdict-rev5.md`: one P0 finding, `interrupted-item-token-threshold-unreviewed`
(delta reviewer). Panels A and B accepted rev5; every earlier fix (resume of legacy over-cap paths, shared parser caps,
routing identities) is closed and must stay exactly as it is.

The defect: the model-visible interrupted item is author + recipient (each `AgentPath::truncated_for_display`, up to
256 bytes + marker) plus the body from `core/src/context/inter_agent_interrupted_message.rs`, which repeats both paths
(again up to 256 bytes + marker each). Dense legacy or newly allocated paths reach about 1.2 KB and 1050+ tokens
(cl100k / o200k measured). Your results claimed about 306 tokens from bytes/4, which is a lower-bound heuristic, not a bound.

## Required (orchestrator decision: fix the bound, do not route to manual review)

1. The bound argument is: for byte-level BPE tokenizers, token count <= UTF-8 byte count. So make the WHOLE model-visible
   item (author display + recipient display + every content text of the interrupted item) <= 1000 bytes by construction.
2. Do it inside the interrupted fragment only: lower `INTERRUPTED_PATH_MAX_BYTES` for the BODY copies (64 bytes is enough;
   the full routing identity already rides in author/recipient). Do NOT change `AgentPath::MODEL_DISPLAY_MAX_BYTES`,
   `truncated_for_display`, the MESSAGE/NEW_TASK envelopes, stored routing identities, the parser caps or resume behavior.
3. Add a const for the full-item bound (e.g. `INTERRUPTED_ITEM_MAX_BYTES = 1000`) with a doc comment stating the
   tokens <= bytes argument, and make the existing `INTERRUPTED_MESSAGE_MAX_BYTES` arithmetic plus the two display caps
   provably fit under it (a `const _: () = assert!(...)` is fine).
4. Tests:
   - unit (in `inter_agent_interrupted_message_tests.rs` or the protocol tests next to `to_model_input_item`): build the
     interrupted communication exactly as delivery does, with the reviewer's dense fixtures (restored legacy parent
     `/root/` + `a1` x150 with child `/worker`, and a new `/root/<a1 x64>/<b2 x64>` parent with a `/worker` child), call
     `to_model_input_item`, sum the bytes of author + recipient + all content texts, assert <= 1000. Also assert short
     paths render byte-identical to rev5 (no context churn for normal names).
   - integration: in `core/tests/suite/goal_native_wait.rs`, add `goal_wait_dense_paths_interrupted_item_bound` (name must
     contain `goal_wait`): with `agent_max_depth >= 3`, spawn 128-char alternating letter/digit segments, interrupt the
     child while the parent goal waits, capture the outbound request, and assert the delivered agent message's
     author + recipient + content bytes <= 1000. Reuse the existing interrupt test helpers in that file.
5. Mutant (add to the mutants JSON, keep all previous mutants applying to the final tree): restore the body path cap to 256;
   killer = the new unit test (and the integration test).
6. Correct the results: replace the bytes/4 estimate with the byte bound and the measured worst-case bytes.

`mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item` then `--check` must exit 0; no other
cargo; no CODEX_HOME copies; delete temp dirs. Watch for redundant closures, uninlined format args, `vec!` where an array
works, and `/*param*/` comments on positional literals. Leave everything UNCOMMITTED, report the final tree id after fmt,
add the note `HOSTED-PRECHECK-REQUESTED: precheck 16`, and end your turn without handing off.

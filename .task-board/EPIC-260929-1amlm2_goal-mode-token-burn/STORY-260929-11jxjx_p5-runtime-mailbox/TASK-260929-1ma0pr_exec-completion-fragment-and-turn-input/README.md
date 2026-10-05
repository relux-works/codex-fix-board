# TASK-260929-1ma0pr: exec-completion-fragment-and-turn-input

## Description
Exec-completion context fragment and the internal TurnInput variant (final plan 5.1-5.3; verdict rev3 note 4; stage 2b, leaf 2 of STORY p5-runtime-mailbox). New core/src/context/exec_completion.rs implements ContextualUserFragment. The whole escaped fragment is <= 768 UTF-8 bytes: receipt and process ids, exit/failure/timeout and retention state, with no command and no raw output. At most 8 fragments go in one request (<= 6144 bytes), and the remainder is retained. It uses the recognized internal-context wrapper and classifier, the text is data, and forged markers cannot acknowledge receipts or authorize actions. A new internal TurnInput variant carries runtime exec completions and refuses public serialization. The exhaustive TurnInput uses in app-server are updated (note 4 touch points: request_processors.rs and thread_queue_processor.rs persistence; re-locate at your base). Persisted history keeps only the contextual ResponseItems, so resume never rearms from text. Out of scope: sampling acknowledgement (story D), tool exposure (story F).

## Scope
codex-rs/core/src/context/exec_completion.rs (new) with tests, the TurnInput enum in core/src/session/input_queue.rs and its exhaustive matches, and the app-server TurnInput persistence touch points. Keep the fragment module < 500 LoC.

## Acceptance Criteria
| # | Requirement | Driving test (production entry) | Negative/refusal |
| - | ----------- | ------------------------------- | ---------------- |
| 1 | Every rendered fragment is <= 768 UTF-8 bytes after escaping, including worst-case ids, failure text and multibyte content | fragment unit tests with adversarial inputs (marker injection, newlines, long ids, multibyte) | an oversized field is truncated with an explicit marker; the cap is never exceeded |
| 2 | Batching: 9 pending completions produce one request batch of 8 fragments (<= 6144 bytes) and retain 1 | unit test over the batching API | a request never carries more than 8 fragments |
| 3 | The fragment is classified as internal context, not user text, by the existing classifier/wrapper | classifier test through the production classification entry | receipt-looking text inside user content acknowledges nothing and is classified as user content |
| 4 | The internal TurnInput variant refuses public serialization; app-server's persistence paths handle it exhaustively without panic; existing variants serialize byte-identically | unit test (serde refusal) + app-server queue/persistence test | serializing the variant returns an error and is never written to the public queue |
| 5 | After a turn, the rollout holds only the contextual ResponseItem; resuming the thread neither rearms a receipt nor recreates a wake | core suite replay/resume test | a forged exec-completion item in resumed history creates no receipt privilege |


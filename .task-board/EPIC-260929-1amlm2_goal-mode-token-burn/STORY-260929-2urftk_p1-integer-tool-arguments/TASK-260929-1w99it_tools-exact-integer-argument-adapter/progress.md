## Status
backlog

## Review
required

## Task Class
code

## Estimate
notEstimated

## Blocked By
- (none)

## Blocks
- TASK-260929-17t419

## Checklist
- [ ] codex-tools exposes exact integer deserializers (u64, i64, i32, usize + Option variants) in tools/src/arguments.rs with tests in tools/src/arguments_tests.rs
- [ ] Every AC row has its driving test and its refusal test, run green with just test -p codex-tools (real exit code reported)
- [ ] No f64 or serde_json::Value intermediary; exponent handling bounded; error messages keep serde's invalid type/value shape

## Notes

## Precondition Resources
(none)

## Outcome Resources
(none)

## Created
2026-09-29T00:50:32Z

## Last Update
2026-09-29T00:51:04Z

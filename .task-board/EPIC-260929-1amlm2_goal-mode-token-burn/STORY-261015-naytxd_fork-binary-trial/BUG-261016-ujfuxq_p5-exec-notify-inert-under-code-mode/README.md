# BUG-261016-ujfuxq: p5-exec-notify-inert-under-code-mode

## Description
Live A/B (TASK-261015-xgmuju, f52f28f, gpt-6-astra medium, TUI source cli) shows P5 notify_on_exit never activates: goal guidance says This session cannot promise an exec completion wake and the model polls with clock.sleep. The model reaches exec_command/write_stdin only through the code-mode exec tool, and core/src/tools/waiting_capabilities.rs is_directly_visible (~line 219) deliberately excludes nested code-mode tools, so stdin and exec_notify derive false even though AsyncNotificationSupport is Available. Expected: on a capable host with code mode on, either exec_notify activates for code-mode exec_command (notify_on_exit present in the nested schema and the wake delivered after the cell/turn ends), or the limitation is an explicit documented decision. Evidence: TASK-261015-xgmuju_ab-results.md. Needs a design decision on code-mode semantics before implementation.

## Scope
(define bug scope / affected area)

## Acceptance Criteria
(define fix acceptance criteria)

# Surface table — TASK-260929-3r7peh notify-on-exit-and-exec-notification-tool

| Row | Invariant | Attack families |
|---|---|---|
| host capability | AsyncNotificationSupport defaults to Unavailable; only verified persistent hosts enable it; headless exec and all descendants stay Unavailable through explicit inheritance; on Unavailable hosts neither notify_on_exit nor exec_notification is advertised, opt-in is refused before execution, and no wake is promised in descriptions | deriving the capability from "not Exec"; a child of a headless parent; accepting opt-in on an Unavailable host; description promising a wake; advertisement on an Unavailable host |
| opt-in and receipts | notify_on_exit defaults to false and a default launch creates no receipt, slot or wake; opt-in reserves one of 64 receipt slots before launch, and the 65th is refused before execution; the process cap is unchanged; no automatic arming on yield or stdin polls | arm by default; handler dropping the opt-in; capacity off-by-one; launch before reservation; arming on poll |
| exec_notification read and release | read returns retained terminal output within the token bound with truncation indicated, never blocks, and rejects stale, foreign and unknown receipts; release disarms without killing the process, frees the slot, cancels any pending wake, and drops retained output; a later exit yields no wake | owner verification skipped; release skipping the mailbox cancel; release killing the process; ghost retention after disarm; read as a liveness poll |
| activation | the P4a background-wait policy is enabled exactly where the host is Available; with pending opted-in work, goal continuation is gated while user and follow-up input is admitted; the end-to-end receipt -> mailbox -> wake -> fragment path works in the activated configuration | goal never or always enables; gating user input; wake without fragment; activation on an Unavailable host |

```surface-table
{"rows": ["host capability", "opt-in and receipts", "exec_notification read and release", "activation"]}
```

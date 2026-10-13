# TASK-260929-3ld28o rev3: merge correction after recording-review-refusal-rev3

The refusal was right: r141-merge.py flattened note-severity findings into notes, which dropped invariant, reproductions, severity
and repeat-of (the same loss as refusal rev1/rev2). The script now keeps note findings as complete structured findings; findings with
the same row, severity and repeat-of collapse into one, keeping `collapsed_ids`, `collapsed_mechanisms`, every source reproduction
and `also_reported_by`. Only non-note findings block.

The re-merged `TASK-260929-3ld28o_review-verdict-rev3.md` (updated in place) has one nonblocking finding B-N1 (collapsed with D-N1,
row non-resets, severity note, repeat-of rev2/B-N1, both reproductions pinned to 486ebfe5). Verdict: accept (3/3 panels accept, 7/7 rows held).

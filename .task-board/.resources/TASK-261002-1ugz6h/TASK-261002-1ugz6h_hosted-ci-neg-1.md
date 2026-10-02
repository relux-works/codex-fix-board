# relux-ci negative control: ci/relux-ci-selftest/neg-1 (never landed)

- commit: `694b0edb1aa2782f0b67c1ba8e94c0ce4cb647ac` = ea8899e (final relux-ci.yml) + one injected unused import in
  codex-rs/tools/src/lib.rs (`use std::collections::HashMap as ReluxCiGateNegativeControl;`)
- run: https://github.com/relux-works/codex/actions/runs/36974565033 (push event)
- lint lane: **failure** (expected), completed 06:46:58Z. The other lanes were cancelled on purpose after lint finished.
- lint step output:
  ```
  tools/src/lib.rs:4:5: warning: unused import: `std::collections::HashMap as ReluxCiGateNegativeControl`
  clippy warnings: 4 distinct, 3 of them upstream baseline
  ##[error]clippy warnings outside the upstream baseline:
  tools/src/lib.rs: warning: unused import: `std::collections::HashMap as ReluxCiGateNegativeControl`
  ##[error]Process completed with exit code 1.
  ```
- So the warning gate fails the lane on a warning outside the 3-line upstream-baseline list and tolerates the 3 listed
  baseline warnings, which are counted.

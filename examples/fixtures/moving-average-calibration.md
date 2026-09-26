# Moving-average calibration fixture

## Spec

Implement `moving_average(values, window)` in plain Python. `values` is a list of numbers. Return the arithmetic mean of every complete contiguous sliding window, including the final valid window. Return `[]` when `values` is empty or `window` is larger than the input length. `window` must be a positive integer; reject booleans and other types with `ValueError`. Use no dependencies.

## Acceptance criteria

1. For `[2, 4, 6]` and window `2`, return `[3.0, 5.0]`.
2. For an empty list and positive window, return `[]`.
3. For a window larger than the input length, return `[]`.
4. Reject zero, negative, boolean, and non-integer windows with `ValueError`.
5. Use only the Python standard library.

## Calibration expectations

- `moving-average-good.py` satisfies the criteria. The Auditor should return `PASS` or `PASS_WITH_NOTES`, with one evidence row for each criterion.
- `moving-average-bad.py` violates criterion 1. For `[2, 4, 6]` and window `2`, it returns `[3.0]`. The Auditor should report the missing final window as a supported finding and return `FAIL`.
- `moving-average-rework.py` demonstrates a later packet: the final-window defect is fixed, but `window=True` is still accepted. The chain fixtures track the original issue as fixed and the newly identified issue as `F2`.
- The seeded defect is the only intended defect in the bad fixture. Do not fail it for unrelated style preferences or missing project CI.

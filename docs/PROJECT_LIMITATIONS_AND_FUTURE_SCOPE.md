# Project limitations and future scope

## Current limitations

1. The physical unit and definition of `Yield` are unknown.
2. The system performs retrospective, season-level historical estimation.
3. It is not an operational pre-season or during-season forecasting system.
4. Weather aggregation and exact availability timing are undocumented.
5. Fertilizer and pesticide semantics and timing are undocumented.
6. The chronological test covers later historical records, not future
   deployment conditions.
7. Outliers and quality-flagged observations remain in the data.
8. A non-neural baseline and domain validation should be compared before
   practical use.

## Future scope

- Confirm Yield units and agricultural semantics with domain owners.
- Add a browser end-to-end test suite.
- Add deployment configuration, observability, authentication, and rate
  controls if the application becomes shared.
- Compare tree-based and simpler statistical baselines.
- Add model versioning and dataset/model compatibility checks.
- Consider ESP32 or other IoT integration only as a separately validated
  future project; this release does not claim real-time IoT functionality.

# Final Report

## Project Overview

This report is auto-generated from DM-Lab benchmark outputs.
- Run mode: `quick`
- Seed: `42`
- Tasks: classification, clustering, association, anomaly

## Datasets and Preprocessing

- Classification: tabular features with mixed-type preprocessing.
- Clustering: standardized numerical features and KMeans baseline.
- Association: transaction basket encoding and rule mining.
- Anomaly: unsupervised isolation-based scoring with thresholding.

## Method Comparison

| Task | Primary Metric | Score | Notes |
| --- | --- | ---: | --- |
| classification | f1 | 0.967033 | f1=0.967033, roc_auc=0.994969, precision=0.956522, recall=0.977778 |
| clustering | silhouette | 0.736433 | silhouette=0.736433, davies_bouldin=0.381998 |
| association | lift | 2.500000 | support=0.200000, confidence=1.000000, lift=2.500000, rule_count=30 |
| anomaly | pr_auc | 1.000000 | pr_auc=1.000000, f1=1.000000, recall_at_k=1.000000 |

### Metric Ranking

1. `association` by `lift` = `2.500000`
2. `anomaly` by `pr_auc` = `1.000000`
3. `classification` by `f1` = `0.967033`
4. `clustering` by `silhouette` = `0.736433`

## Ablation Study

This section is auto-generated as a lightweight proxy analysis from current metrics.

- Classification threshold sensitivity: |precision-recall| = `0.021256`. Consider threshold tuning or class weighting ablation.
- Clustering configuration sensitivity: silhouette `0.736433`, davies-bouldin `0.381998`. Run k-value ablation (e.g., k=3..8).
- Association rule threshold sensitivity: support `0.200000`, confidence `1.000000`, lift `2.500000`. Ablate `min_support` and `min_confidence` to balance rule volume and quality.
- Anomaly threshold sensitivity: pr_auc `1.000000`, recall_at_k `1.000000`. Ablate contamination ratio / top-k threshold.

## Error Analysis

- No major metric-level failure detected in this run.

### Recommended Next Checks

1. Re-run with a different seed to verify stability.
2. Compare quick vs full mode deltas per task.
3. Inspect top error cases for classification/anomaly tasks.

## Conclusion

The current run produced a complete baseline across four data-mining tasks. Use this report as the base for presentation, then append screenshots/plots from artifacts.

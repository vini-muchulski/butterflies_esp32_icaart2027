# Experiment notebooks

This directory collects the experiment notebooks supporting the comparison of pretrained MobileNetV2 and MobileViT-XXS under INT8 quantization and ESP32-S3 deployment.

## Contents

| Stage | Notebook | Purpose |
|---|---|---|
| Training | [MobileNetV2 baseline](01_training/mobilenetv2/mobilenetv2_training.ipynb) | Fine-tuning, test evaluation, and initial TFLite conversions. |
| Training | [MobileViT-XXS baseline](01_training/mobilevit_xxs/mobilevit_xxs_training.ipynb) | Fine-tuning, test evaluation, and initial TFLite conversions. |
| Export | [MobileNetV2 explicit pooling](02_export/mobilenetv2/mobilenetv2_average_pool_export.ipynb) | Export with explicit average pooling and host-side resolver comparisons. |
| Export | [MobileNetV2 deployment verification](02_export/mobilenetv2/mobilenetv2_export_verification.ipynb) | Training/export workflow with checks intended for ESP32-S3 deployment. |
| Export | [MobileViT-XXS deployment verification](02_export/mobilevit_xxs/mobilevit_xxs_grouped_export_verification.ipynb) | Activation diagnosis, initial structural grouping, and export checks. |
| Structural comparison | [MobileViT-XXS configuration comparison](03_structural_comparison/mobilevit_xxs_structural_comparison.ipynb) | Seventeen grouping configurations, validation-based selection, and exploratory test evaluation. |
| Statistical analysis | [Paired statistical analysis](04_statistical_analysis/paired_statistical_analysis.ipynb) | Paired TFLite predictions, Wilson intervals, bootstrap differences, exact McNemar tests, and Holm adjustment. |
| Figures | [Diagnostic and result figures](05_figures/generate_article_figures.ipynb) | Activation/weight diagnostics, grouping comparisons, and accuracy-recovery plots. |

[Separate activation-diagnosis panels](05_figures/regenerate_activation_scale_diagnosis.py) is a companion Python script. It reads saved tables and generates the two activation-diagnosis panels without loading models or recalibrating.

## Current assembly status

The files use descriptive English names; their contents remain unchanged, including stored outputs, execution counts, and metadata. [provenance.csv](provenance.csv) records the original workspace paths, destination paths relative to this directory, file sizes, and full SHA-256 hashes. Source paths document the original workspace layout; they are not dependencies to retrieve from this repository.

The copies have not been executed or adapted to this directory layout. Existing absolute paths, directory searches, and output locations may still refer to the original workspace. Review and adapt these paths before executing any cells, including paths that write results. Notebook outputs are historical records, not evidence of a new run in this repository.

Dataset files, checkpoints, exported models, result tables, and firmware have not been copied in this stage. Consequently, this directory is not yet a self-contained reproduction package. Checkpoints referenced by the notebooks include `best__model.pt` and `best_mobilevit_xx_small_v0.pt`. Analysis notebooks also require exported models and saved results from the corresponding experiments.

The companion plotting script expects `tables/block_activation_summary.csv` and `tables/estimated_effective_levels_summary.csv` alongside it. Those tables are not included yet.

## Interpretation

- Training and initial conversions establish the pretrained model baselines. Deployment-oriented exports are distinct artifacts and should not be identified solely as the original INT8 model.
- The structural comparison uses the pretrained/fine-tuned MobileViT checkpoint without retraining. The selected configuration groups blocks 1, 2, 3, and 5 into 8, 4, 4, and 4 groups, respectively.
- Selection uses validation accuracy, but the test partition had already been inspected. Recovery results remain exploratory; paired statistical tests do not provide an independent confirmation.
- Host-side LiteRT predictions and ESP32-S3 predictions must be reported separately. Export compatibility checks in notebooks are not a replacement for device execution measurements.

The next preparation step is to supply the required inputs and adapt paths in these copies. Training, export, and evaluation should only be rerun deliberately; viewing the stored notebook outputs requires no new experiment.

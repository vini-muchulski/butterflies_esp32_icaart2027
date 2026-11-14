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

## Execution requirements

Configure dataset, checkpoint, model, and output paths in the setup cells before execution. The notebooks contain environment-specific absolute paths and directory searches; verify both input locations and result destinations for your environment.

Training requires the Butterflies-Austria-20 training, validation, and test partitions. Export and structural-comparison experiments require the relevant trained checkpoints, including `best__model.pt` and `best_mobilevit_xx_small_v0.pt`. Analysis notebooks require the corresponding TFLite models and experiment records. Follow the model-specific preprocessing implemented in each notebook.

The companion plotting script reads `tables/block_activation_summary.csv` and `tables/estimated_effective_levels_summary.csv` relative to its own directory. The data tables are available as [block_activation_summary.csv](../results/diagnostics/block_activation_summary.csv) and [estimated_effective_levels_summary.csv](../results/diagnostics/estimated_effective_levels_summary.csv); place them at the script's expected locations before running it.

## Experiment records

Stored outputs, execution counts, and metadata document the recorded experiments. [provenance.csv](provenance.csv) lists experimental source identifiers, reference file sizes, and reference SHA-256 hashes identifying the source versions associated with those records.

Results are indexed in [../results/README.md](../results/README.md), and figures are presented in [../figures/README.md](../figures/README.md). Inspecting these records does not require rerunning training, export, or inference.

## Interpretation

- Training and initial conversions establish the pretrained model baselines. Deployment-oriented exports are distinct artifacts and should not be identified solely as the original INT8 model.
- The structural comparison uses the pretrained/fine-tuned MobileViT checkpoint without retraining. The selected configuration groups blocks 1, 2, 3, and 5 into 8, 4, 4, and 4 groups, respectively.
- Selection uses validation accuracy, but the test partition had already been inspected. Recovery results remain exploratory; paired statistical tests do not provide an independent confirmation.
- Host-side LiteRT predictions and ESP32-S3 predictions must be reported separately. Export compatibility checks in notebooks are not a replacement for device execution measurements.


# Empirical results

This directory contains the recorded evidence supporting the MobileNetV2 and MobileViT-XXS comparison on Butterflies-Austria-20. Existing reports were copied without modifying their values. Training and initial-conversion records were extracted from saved notebook outputs, without executing cells or recomputing metrics.

Structural recovery results are exploratory: configuration selection used validation accuracy, but the test partition had already been inspected. Statistical tests on these predictions do not provide an independent confirmation.

## Evidence index

| Directory | Contents | Related notebook |
|---|---|---|
| [training/](training/) | Saved training logs, parameter counts, PyTorch test results, and classification-report text for both baselines. | [MobileNetV2](../notebooks/01_training/mobilenetv2/mobilenetv2_training.ipynb), [MobileViT-XXS](../notebooks/01_training/mobilevit_xxs/mobilevit_xxs_training.ipynb) |
| [quantization/initial/](quantization/initial/) | Initial FP32, INT8A16, and full INT8 conversion and test records, extracted from saved outputs. | The two baseline notebooks above. |
| [quantization/mobilenetv2_average_pool/](quantization/mobilenetv2_average_pool/) | Saved explicit-pooling export and host-side resolver comparison outputs. | [Average-pool export](../notebooks/02_export/mobilenetv2/mobilenetv2_average_pool_export.ipynb) |
| [quantization/mobilevit_g8_4_4/](quantization/mobilevit_g8_4_4/) | Initial grouped-recovery reports, activation statistics, grouping, calibration manifest, FP32 comparison, and TFLite inspection. | [Grouped export verification](../notebooks/02_export/mobilevit_xxs/mobilevit_xxs_grouped_export_verification.ipynb) |
| [structural_comparison/](structural_comparison/) | Full comparison of 17 configurations, shared diagnostics, per-variant records, selection, and selected test reports. | [Configuration comparison](../notebooks/03_structural_comparison/mobilevit_xxs_structural_comparison.ipynb) |
| [block7_extension/](block7_extension/) | Earlier block-7 extension experiment, retained separately from the 17-configuration comparison. | The original block-7 notebook is identified by the provenance paths; it is not included in the current notebook selection. |
| [diagnostics/](diagnostics/) | Saved tables underlying activation, weight, grouping, recovery, and block-7 plots. | [Article figures](../notebooks/05_figures/generate_article_figures.ipynb) |
| [statistical_analysis/](statistical_analysis/) | Individual paired predictions, model accuracies, exact McNemar tests, bootstrap intervals, Holm adjustments, and experiment summary. | [Paired analysis](../notebooks/04_statistical_analysis/paired_statistical_analysis.ipynb) |
| [esp32s3/](esp32s3/) | Three device runs with predictions, telemetry, classification reports, confusion matrices, model identity, and timing/memory summaries. | See the [device-results guide](esp32s3/README.md). |

Figures are indexed in [../figures/README.md](../figures/README.md).

## Main records to inspect

- [All 17 validation configurations](structural_comparison/ablation_summary.csv).
- [Selection rule and selected configuration](structural_comparison/selection.json).
- [Final comparison summary](structural_comparison/final_summary.json).
- [Selected configuration and controls on test](structural_comparison/selected_test_results.csv).
- [Per-class report for the selected INT8 configuration](structural_comparison/selected_int8_test_report.json).
- [Per-variant validation, FP32, grouping, and inspection records](structural_comparison/variants/).
- [Ordered calibration manifest](structural_comparison/shared/calibration_manifest.csv).
- [Per-channel activation statistics](structural_comparison/shared/channel_statistics.csv).
- [Accuracy-recovery plot data](diagnostics/accuracy_recovery_comparison.csv).
- [Estimated effective levels by channel](diagnostics/estimated_effective_levels_by_channel.csv).
- [Paired test predictions](statistical_analysis/tables/paired_test_predictions.csv).
- [McNemar/bootstrap/Holm results](statistical_analysis/tables/mcnemar_results.csv).
- [Independent statsmodels calculation](statistical_analysis/tables/statsmodels_mcnemar_results.csv).

## Artifact and runtime distinctions

The initial MobileViT-XXS full INT8 conversion with 100 calibration images achieved 9.57% test accuracy. The ungrouped control with 1,000 stratified calibration images and export adaptations achieved 10.65%. They are different artifacts. Labels such as `original_int8`, `Original full INT8`, or `MobileViT-XXS original INT8` in structural-comparison and paired-analysis records identify the latter control, not the initial 100-image conversion.

The initial exports and the stratified control also differ in export adaptations; their comparison does not isolate the calibration-set change alone. The ungrouped control and structural variants within the 17-configuration comparison share the checkpoint, calibration data, quantizer, and export adaptations.

| Model | LiteRT test accuracy in the paired analysis | ESP32-S3 test accuracy |
|---|---:|---:|
| MobileViT-XXS ungrouped INT8 control | 10.65% | Not included in the three device runs |
| MobileViT-XXS INT8 with `g8_4_4` | 90.74% | 91.05% |
| MobileViT-XXS INT8 with `g8_4_4 + b3_g4` | 96.30% | 96.30% |

The paired-analysis accuracy source is [model_accuracy.csv](statistical_analysis/tables/model_accuracy.csv); device sources are the individual `summary.json` files linked in the [device guide](esp32s3/README.md). Equal accuracy does not imply identical predictions. Resolver-specific results in saved export outputs should remain separate from these sources.

## Reading saved notebook outputs

- Training: [MobileNetV2](training/mobilenetv2/recorded_outputs.json), [MobileViT-XXS](training/mobilevit_xxs/recorded_outputs.json).
- Initial conversion: [MobileNetV2](quantization/initial/mobilenetv2/recorded_outputs.json), [MobileViT-XXS](quantization/initial/mobilevit_xxs/recorded_outputs.json).
- Explicit average-pool export: [MobileNetV2](quantization/mobilenetv2_average_pool/recorded_outputs.json).

Each extracted file retains saved stream output, textual/JSON display data, execution counts, and zero-based cell/output indices. It records the source notebook and its SHA-256. Images and widget payloads were omitted from these extracts; exported figures are organized separately. No numerical values were inferred from plots or recalculated. These files are historical execution records, not new runs in this repository.

## Interpretation and units

- An FP32-equivalence check was diagnostic, not a mandatory eligibility filter. For example, `b1_g8` remained in the comparison despite failing its diagnostic threshold.
- Historical `esp32_compatible=False` inspection flags reflect the allowlist used at that stage, including its handling of `BATCH_MATMUL`. Later recorded device runs are separate execution evidence.
- Activation-scale ratios and effective-level estimates come from FP32 PyTorch activations. They are not direct measurements of internal TFLite quantization scales or observed integer values.
- Accuracy values in machine-readable tables are generally fractions; percentage formatting in figures and prose must be interpreted accordingly.
- Preserve exact `size_bytes`/`bytes` fields as the size reference. The historical `size_mb` column in [compared_int8_models.csv](diagnostics/compared_int8_models.csv) uses division by 1024 squared, so its values are MiB despite the column name. Some saved notebook messages also label binary sizes as MB. These raw records have not been relabeled or numerically altered. Decimal MB means 1,000,000 bytes.
- Device timing fields ending in `_us` are microseconds. Published inference times refer to the device's model invocation, not HTTP round-trip time or end-to-end image classification. Device memory summaries distinguish tensor-arena use from other memory fields; arena use is not total peak RAM.
- McNemar p-values adjusted with Holm and unadjusted marginal bootstrap intervals answer different inferential questions. Lack of statistical significance does not establish equivalence.

## Provenance and scope

[provenance.csv](provenance.csv) covers every empirical file in this directory, excluding documentation and the manifest itself. It records the source path relative to the original workspace, destination relative to this repository, source and destination SHA-256 hashes, destination size, and operation. `copy_unchanged` files have identical source/destination hashes. `extract_saved_text_outputs` files record the source cell indices and have their own destination hashes.

Original workspace paths, model names, run IDs, and field names inside raw reports are preserved for traceability. They are not portable input paths or instructions to contact the recorded device address. Checkpoints, TFLite model binaries, firmware builds, caches, and the partial intermediate comparison summary are outside this copy stage.

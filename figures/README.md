# Empirical figures

These are existing experiment figures copied into a categorized layout. They were not regenerated, edited, or recomputed. PNG files can be viewed below; PDF versions are included where they existed in the source directories.

[catalog.csv](catalog.csv) maps every PNG to its related notebook/script and result records. [provenance.csv](provenance.csv) records every copied PNG/PDF, its original workspace path, current path, byte size, and SHA-256. Renamed files retain the original image bytes and labels.

## Dataset and baseline examples

The same physical training, validation, and test partitions were used for both models. Each pipeline retains its own preprocessing. Corresponding MobileViT-XXS examples are available in [dataset/mobilevit_xxs/](dataset/mobilevit_xxs/).

| Training class distribution | Training examples |
|---|---|
| ![Training class distribution](dataset/mobilenetv2/class_distribution.png) | ![Training examples](dataset/mobilenetv2/training_samples.png) |

| Test examples | Validation examples |
|---|---|
| ![Test examples](dataset/mobilenetv2/test_samples.png) | ![Validation examples](dataset/mobilenetv2/validation_samples.png) |

Data and generator: the [baseline notebooks](../notebooks/README.md) and [saved training outputs](../results/training/).

## PyTorch training and test results

| MobileNetV2 | MobileViT-XXS |
|---|---|
| ![MobileNetV2 training curves](training/mobilenetv2/training_curves.png) | ![MobileViT-XXS training curves](training/mobilevit_xxs/training_curves.png) |
| ![MobileNetV2 test predictions](training/mobilenetv2/test_predictions.png) | ![MobileViT-XXS test predictions](training/mobilevit_xxs/test_predictions.png) |
| ![MobileNetV2 test confusion matrix](training/mobilenetv2/confusion_matrix.png) | ![MobileViT-XXS test confusion matrix](training/mobilevit_xxs/confusion_matrix.png) |

These are the baseline notebook figures; they are separate from the device confusion matrices below. Classification-report text and training logs are retained in [results/training/](../results/training/).

## INT8 diagnosis and recovery

| Activation-scale heterogeneity | Estimated effective INT8 levels |
|---|---|
| ![Activation-scale heterogeneity](quantization/activation_scale_heterogeneity.png) | ![Estimated effective INT8 levels](quantization/estimated_effective_int8_levels.png) |

The first panel compares the largest and smallest diagnostic channel scales per block. The second compares median effective quantization levels under the ungrouped and grouped representations. These quantities are estimated from FP32 PyTorch activations; they are not direct TFLite tensor-scale measurements. Lines at 16 and 32 levels are descriptive references.

Saved data: [block_activation_summary.csv](../results/diagnostics/block_activation_summary.csv), [estimated_effective_levels_summary.csv](../results/diagnostics/estimated_effective_levels_summary.csv), and [per-channel estimates](../results/diagnostics/estimated_effective_levels_by_channel.csv). Related script: [regenerate_activation_scale_diagnosis.py](../notebooks/05_figures/regenerate_activation_scale_diagnosis.py).

![INT8 accuracy recovery comparison](quantization/int8_accuracy_recovery_comparison.png)

[PDF](quantization/int8_accuracy_recovery_comparison.pdf) · [Plot data](../results/diagnostics/accuracy_recovery_comparison.csv)

The control labeled `Original full INT8` is the stratified, ungrouped MobileViT-XXS INT8 control, not the initial 100-image INT8 conversion. The plot's test panel follows the selected-configuration evaluation; the later paired analysis also evaluated `g8_4_4` on test. Those records are available separately in [model_accuracy.csv](../results/statistical_analysis/tables/model_accuracy.csv). Recovery remains exploratory.

| Weight distributions | Weight--activation relationship |
|---|---|
| ![Expansion-weight distributions](quantization/weight_distribution_selected_blocks.png) | ![Weight magnitude and activation scale](quantization/weight_activation_relationship.png) |

Related data: [expansion-weight statistics](../results/diagnostics/expansion_weight_channel_statistics.csv) and [weight--activation correlations](../results/diagnostics/weight_activation_correlations_by_block.csv). The latter describes association, not causality.

Additional diagnostic PNG/PDF files in [quantization/](quantization/) retain scale ratios, channel-level utilization, low-resolution channel fractions, group partitions for blocks 1/2/5, the combined diagnosis panel, and the earlier grouping-only recovery figure. Historical labels such as `codes` refer to quantization levels, not memory or image counts. The initial-grouping plot and the selected-configuration comparison represent different stages and should not be merged as if they were a single evaluation.

## Structural configuration comparison

![Validation accuracy across structural configurations](structural_comparison/ablation_validation_accuracy.png)

| Accuracy and model size | Controlled contrasts |
|---|---|
| ![Accuracy versus size](structural_comparison/ablation_accuracy_size_tradeoff.png) | ![Controlled grouping contrasts](structural_comparison/g8_4_4_controlled_contrasts.png) |

Data: [17-configuration validation summary](../results/structural_comparison/ablation_summary.csv), [controlled contrasts](../results/structural_comparison/g8_4_4_contrasts.csv), and [selection record](../results/structural_comparison/selection.json). Notebook: [structural comparison](../notebooks/03_structural_comparison/mobilevit_xxs_structural_comparison.ipynb).

The earlier block-7 extension has its own [records](../results/block7_extension/) and [incremental comparison figure](quantization/block7_incremental_accuracy_delta.png). It is kept separate from the 17-configuration run.

## Paired statistical analysis

![Paired accuracy differences](statistical_analysis/mcnemar_paired_accuracy_differences.png)

Bars show marginal, multiplicity-unadjusted bootstrap intervals; Holm adjustment applies to the McNemar p-values. Nonsignificance does not demonstrate equivalence, and the test partition's prior use limits confirmatory interpretation.

Further figures in [statistical_analysis/](statistical_analysis/) show accuracy intervals, discordant pairs, contingency tables, and adjusted p-values. Data: [paired predictions](../results/statistical_analysis/tables/paired_test_predictions.csv), [McNemar results](../results/statistical_analysis/tables/mcnemar_results.csv), and [statsmodels results](../results/statistical_analysis/tables/statsmodels_mcnemar_results.csv). Notebook: [paired analysis](../notebooks/04_statistical_analysis/paired_statistical_analysis.ipynb).

## ESP32-S3 predictions

| MobileNetV2 INT8 | MobileViT-XXS INT8 with `g8_4_4` | MobileViT-XXS INT8 with `g8_4_4 + b3_g4` |
|---|---|---|
| ![MobileNetV2 device confusion matrix](esp32s3/mobilenetv2_confusion_matrix.png) | ![MobileViT grouped device confusion matrix](esp32s3/mobilevit_g8_4_4_confusion_matrix.png) | ![MobileViT extended-grouping device confusion matrix](esp32s3/mobilevit_g8_4_4_b3_g4_confusion_matrix.png) |

These confusion matrices use predictions returned by the microcontroller. Raw predictions, invocation-time distributions, memory statistics, and deployed model hashes are linked in the [device-results guide](../results/esp32s3/README.md). No new latency or memory plot was generated in this stage.

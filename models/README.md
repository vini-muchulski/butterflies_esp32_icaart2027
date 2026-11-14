# Models

Three trained PyTorch checkpoints and 48 TFLite artifacts for the 20-class Butterflies-Austria-20 experiments.

| Directory | Contents |
|---|---|
| [checkpoints/](checkpoints/) | MobileNetV2 training and deployment checkpoints, plus the MobileViT-XXS training checkpoint. |
| [tflite/initial/](tflite/initial/) | Initial FP32, INT8A16, and INT8 conversions of both models. |
| [tflite/mobilenetv2_average_pool/](tflite/mobilenetv2_average_pool/) | Explicit-average-pooling exports associated with the training checkpoint. |
| [tflite/mobilenetv2_deployment/](tflite/mobilenetv2_deployment/) | FP32, INT8A16, and INT8 exports associated with deployment verification. |
| [tflite/mobilevit_xxs_control/](tflite/mobilevit_xxs_control/) | FP32 reference and ungrouped INT8 control for the structural comparison. |
| [tflite/structural_variants/](tflite/structural_variants/) | FP32 and INT8 artifacts for all 17 grouping configurations. |

The `.pt` files contain model state dictionaries; instantiate the corresponding 20-class architecture before loading them. `mobilenetv2_training.pt` and `mobilenetv2_deployment.pt` are distinct checkpoints associated with their respective notebooks. MobileViT-XXS control and structural variants share `mobilevit_xxs_training.pt`.

Initial quantization used 100 training samples; MobileViT structural experiments used the [1,000-file stratified calibration selection](../data/manifests/calibration_stratified_1000.csv). INT8A16 denotes INT8 weights and INT16 activations. File sizes and hashes distinguish initial conversions from deployment artifacts.

## Models executed on the ESP32-S3

| Artifact | File | SHA-256 prefix |
|---|---|---|
| MobileNetV2 INT8 | [mobilenetv2_int8.tflite](tflite/mobilenetv2_deployment/mobilenetv2_int8.tflite) | `73444df0dcd4` |
| MobileViT-XXS INT8 with `g8_4_4` | [mobilevit_xxs_int8.tflite](tflite/structural_variants/g8_4_4/mobilevit_xxs_int8.tflite) | `1c830eca3f88` |
| MobileViT-XXS INT8 with `g8_4_4 + b3_g4` | [mobilevit_xxs_int8.tflite](tflite/structural_variants/g8_4_4_b3_g4/mobilevit_xxs_int8.tflite) | `559b6c236bb3` |

These files match the model hashes in the [recorded device evaluations](../results/esp32s3/README.md). [esp32s3_artifacts.csv](esp32s3_artifacts.csv) provides their full hashes, input/output shapes, quantization parameters, and run-summary links.

## Artifact records

- [catalog.csv](catalog.csv): model paths, roles, representations, checkpoint associations, calibration counts, grouping configurations, result references, sizes, and full hashes. Calibration counts apply to quantized artifacts; blank counts mean calibration is not applicable.
- [paired_analysis_models.csv](paired_analysis_models.csv): the exact five TFLite artifacts corresponding to the paired statistical-analysis labels.
- [provenance.csv](provenance.csv): experimental source identifiers and artifact hashes.
- [checksums.sha256](checksums.sha256): full file checksums, with paths relative to this directory.

Use the model-specific preprocessing documented in [data/README.md](../data/README.md). The complete grouping results are in [results/structural_comparison/](../results/structural_comparison/).

# ESP32-S3 evaluation records

Each directory below contains one recorded evaluation of 648 test tensors on the ESP32-S3. Model names identify different artifacts; run IDs preserve the original execution identifiers.

| Model | Run and raw summary | Correct / samples | Accuracy | Mean model invocation | Arena used / reserved (bytes) |
|---|---|---:|---:|---:|---:|
| MobileNetV2 INT8, explicit average pooling | [20260916T142132Z_model_int8_avgpool](mobilenetv2/20260916T142132Z_model_int8_avgpool/summary.json) | 630 / 648 | 97.22% | 3.270 s | 2,599,136 / 5,242,880 |
| MobileViT-XXS INT8 with `g8_4_4` | [20260917T154102Z_mobilevit_int8](mobilevit_g8_4_4/20260917T154102Z_mobilevit_int8/summary.json) | 590 / 648 | 91.05% | 45.657 s | 2,881,824 / 5,242,880 |
| MobileViT-XXS INT8 with `g8_4_4 + b3_g4` | [20260919T230022Z_mobilevit_int8](mobilevit_g8_4_4_b3_g4/20260919T230022Z_mobilevit_int8/summary.json) | 624 / 648 | 96.30% | 46.284 s | 2,885,136 / 5,242,880 |

The displayed values summarize the stored `summary.json` fields `correct`, `samples`, `accuracy`, `timing_us.inference_us.mean`, and `memory_bytes.arena_used`/`arena_capacity`. Percentages and seconds are rounded for display; the raw values are preserved.

## Files in each run

- `summary.json`: aggregate metrics, model SHA-256 and size, quantization metadata, warm-up count, device status, and timing/memory statistics.
- `run.json`: recorded run configuration.
- `predictions.csv`: one row per test image, including true/predicted class, scores, hashes, timing, and memory fields.
- `telemetry.jsonl`: recorded telemetry.
- `classification_report.json` and `classification_report.txt`: per-class and aggregate prediction metrics.
- `confusion_matrix.csv`: numerical confusion matrix.
- `terminal.txt`: saved terminal output.

The three original confusion-matrix images are in [../../figures/esp32s3/](../../figures/esp32s3/).

## Measurement boundary

The host prepared model-specific image inputs and transmitted quantized NCHW INT8 tensors over HTTP. Device inference timing surrounds `MicroInterpreter::Invoke()` and excludes image acquisition, host preprocessing, communication, input copying, and postprocessing. Other timing fields in the raw records describe different parts of the protocol and must not be substituted for the invocation measurement.

Arena occupancy measures only the tensors' arena allocation. It is not total firmware RAM or peak memory. The three graphs also differ in input resolution and operator composition; these records do not isolate a single architectural cause of the latency difference.

The model SHA-256 values recorded in each summary identify the deployed files. The binaries are not included in this stage. Saved host paths and device addresses describe the original experiment environment.

All files were copied unchanged. No device evaluation was rerun.

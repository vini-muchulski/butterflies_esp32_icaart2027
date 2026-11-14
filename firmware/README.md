# ESP32-S3 firmware

Three PlatformIO/ESP-IDF projects for the ESP32-S3 DevKitC-1 N16R8: 240 MHz CPU, 16 MB flash, 8 MB octal PSRAM, and a 5,242,880-byte tensor arena.

| Project | Deployed model | Input shape | Evaluation warm-ups |
|---|---|---|---:|
| [mobilenetv2/](mobilenetv2/) | MobileNetV2 INT8 | [1,3,224,224] | 3 |
| [mobilevit_g844/](mobilevit_g844/) | MobileViT-XXS INT8, `g8_4_4` | [1,3,256,256] | 1 |
| [mobilevit_g844_b3g4/](mobilevit_g844_b3g4/) | MobileViT-XXS INT8, `g8_4_4 + b3_g4` | [1,3,256,256] | 1 |

The projects use Espressif32 platform 6.12.0, ESP-IDF 5.5.0, and LittleFS 1.14.8. Shared dependencies are official Git submodules: [ESP-NN v1.1.2](components/esp-nn/) and [ESP-TFLite-Micro v1.3.2](components/esp-tflite-micro/), pinned to commits in the repository. The manifests select the local ESP-NN submodule instead of a registry download. These upstream sources omit the local runtime adaptations used in the recorded experiments; firmware execution with these revisions has not been validated.

## Build and flash

From the repository root, initialize the dependencies:

```bash
git submodule update --init --recursive
```

Set `ssid` and `password` in the selected project's `src/main.cpp`. Its `data/` directory contains the exact deployed model, identified in [project_models.csv](project_models.csv). From that project directory, run:

```bash
pio run -e esp32s3
pio run -e esp32s3 -t upload
pio run -e esp32s3 -t uploadfs
pio device monitor -b 115200
```

## Evaluate

Set the environment variables `DATASET_ROOT` to the external directory containing `train/`, `val/`, and `test/`, and `ESP32_IP` to the address printed by the device. From the repository root:

```bash
python -m pip install -r firmware/requirements.txt
python firmware/mobilenetv2/python/evaluate_device.py
```

Use the corresponding project path for either MobileViT model. The evaluator writes timestamped reports under the project's `python/results_esp/evaluation/`; `RESULTS_DIR` overrides the output directory. `evaluate_host.py` runs the LiteRT comparison, and `inference_client.py` provides preprocessing and single-image device inference.

`GET /status` reports model metadata; `POST /predict_bin` accepts preprocessed NCHW INT8 tensors. The host performs image resizing, normalization, and input quantization. Device inference time covers `MicroInterpreter::Invoke()` only; arena use is not total RAM.

[Recorded device results](../results/esp32s3/README.md) contain per-image predictions, telemetry, and timing summaries. [provenance.csv](provenance.csv) records project file hashes and packaging adjustments. Model identities match [models/esp32s3_artifacts.csv](../models/esp32s3_artifacts.csv).

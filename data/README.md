# Butterflies-Austria-20

The dataset contains 6,479 images across 20 classes. It is available from [Kaggle, version 8702901](https://www.kaggle.com/dsv/8702901), published by Christian Menard in 2024 ([DOI](https://doi.org/10.34740/KAGGLE/DSV/8702901)). Dataset images are not included in this repository.

## Partitions

| Partition | Images | Manifest |
|---|---:|---|
| Training | 5,183 | [train.csv](manifests/train.csv) |
| Validation | 648 | [val.csv](manifests/val.csv) |
| Test | 648 | [test.csv](manifests/test.csv) |

Both models use the same stratified 80/10/10 split with seed 42. The manifests define exact membership, image order, class labels, file sizes, and SHA-256 checksums. Image paths are relative to the dataset root and follow `partition/class_name/image.jpg`.

## Supporting manifests

- [class_mapping.csv](manifests/class_mapping.csv): 20 zero-based class indices, matching the models.
- [class_distribution.csv](manifests/class_distribution.csv): image counts per class and partition.
- [calibration_stratified_1000.csv](manifests/calibration_stratified_1000.csv): ordered calibration selection for the structural experiments.
- [dataset_metadata.json](manifests/dataset_metadata.json): dataset reference, split and calibration protocols, and preprocessing.
- [duplicate_files.csv](manifests/duplicate_files.csv): two identical-content pairs within training; no exact-content duplicates cross partitions.
- [integrity_report.json](manifests/integrity_report.json): membership, checksum, and prediction-alignment checks.
- [provenance.csv](manifests/provenance.csv): checksums and derivation methods for the manifest files.

## Calibration

Initial exports used 100 training samples selected with seed 42; their selection procedure is implemented in the [training notebooks](../notebooks/README.md).

The structural experiments used 1,000 training files, 50 per class, with no validation or test samples. The calibration manifest preserves their recorded order. These files contain 999 distinct contents because one identical-content pair is included. This selection is separate from the initial 100-sample calibration.

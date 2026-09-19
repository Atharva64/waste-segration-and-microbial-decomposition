# Model Comparison

## MobileNetV3Small vs EfficientNetV2B0

Both models were evaluated using the same test dataset and preprocessing
pipeline.

| Metric | MobileNetV3Small | EfficientNetV2B0 |
|---|---:|---:|
| Accuracy | 76.99% | 84.48% |
| Precision | 77.45% | 84.49% |
| Recall | 76.99% | 84.48% |
| F1 Score | 76.77% | 84.43% |
| Approx. inference time / image | 8.54 ms | 16.62 ms |
| Saved model size | 4.17 MB | 23.58 MB |

## Experimental Conditions

Both models used:

- The same six waste classes
- The same train/validation/test dataset split
- 224 × 224 RGB images
- The same normalization pipeline
- The same training augmentation
- ImageNet pretrained weights
- Frozen feature-extraction base
- Adam optimizer
- Sparse categorical cross-entropy loss
- Early stopping
- Learning-rate reduction
- Best validation checkpoint for final evaluation

## Interpretation

The two architectures should be compared using multiple factors rather than
accuracy alone.

Important considerations include:

- Test accuracy
- Precision
- Recall
- F1-score
- Inference speed
- Saved model size
- Future deployment requirements

MobileNetV3Small is designed as a lightweight architecture, while
EfficientNetV2B0 provides a different accuracy/efficiency trade-off.

The measured results above should be used when deciding which architecture
is more appropriate for later deployment in this project.

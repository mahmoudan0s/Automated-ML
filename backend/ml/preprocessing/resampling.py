from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd


class RandomOverSamplerCustom:
    """Simple random oversampler for imbalanced targets (never undersamples)."""

    def __init__(self, random_state: int = 42) -> None:
        self.random_state = random_state

    def fit_resample(self, X: np.ndarray, y: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        rng = np.random.default_rng(self.random_state)
        y_series = pd.Series(y).reset_index(drop=True)
        X_arr = np.asarray(X)

        counts = y_series.value_counts()
        if counts.empty:
            return X_arr, y_series.to_numpy()

        max_count = int(counts.max())
        resampled_indices: List[int] = []

        for cls in counts.index:
            cls_indices = np.where(y_series.to_numpy() == cls)[0]
            if len(cls_indices) == 0:
                continue

            if len(cls_indices) < max_count:
                extra = rng.choice(cls_indices, size=max_count - len(cls_indices), replace=True)
                final_idx = np.concatenate([cls_indices, extra])
            else:
                final_idx = cls_indices

            resampled_indices.extend(final_idx.tolist())

        rng.shuffle(resampled_indices)
        idx = np.asarray(resampled_indices, dtype=int)
        return X_arr[idx], y_series.to_numpy()[idx]


def is_target_imbalanced(y: pd.Series, minority_majority_ratio_threshold: float = 0.67) -> bool:
    value_counts = y.value_counts(dropna=False)
    if value_counts.empty or len(value_counts) < 2:
        return False

    minority = float(value_counts.min())
    majority = float(value_counts.max())
    return (minority / majority) < minority_majority_ratio_threshold


def choose_sampler(preferred: str = "random", random_state: int = 42) -> Tuple[Optional[RandomOverSamplerCustom], Optional[str]]:
    # Keeps behavior deterministic and avoids undersampling by design.
    if preferred.lower() in {"none", "off", "disable"}:
        return None, None
    return RandomOverSamplerCustom(random_state=random_state), "RandomOverSamplerCustom"

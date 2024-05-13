"""Histogram for single Value Features."""

import multiprocessing as mp
from typing import Any

import numpy as np
from datasets import Features
from numpy.typing import NDArray

from hyped.common.feature_checks import (
    FLOAT_TYPES,
    INT_TYPES,
    UINT_TYPES,
    raise_feature_equals,
)
from hyped.common.feature_key import FeatureKey
from hyped.data.processors.statistics.base import (
    BaseDataStatistic,
    BaseDataStatisticConfig,
)
from hyped.data.processors.statistics.report import StatisticsReportStorage


class HistogramConfig(BaseDataStatisticConfig):
    """Histogram Data Statistic Config.

    Build a histogram of a given value feature.

    Attributes:
        statistic_key (str):
            key under which the statistic is stored in reports.
            See `StatisticsReport` for more information.
        feature_key (FeatureKey):
            key to the dataset feature of which to build the
            histogram
        low (float): lower end of the range of the histogram
        high (float): upper end of the range of the histogram
        num_bins (int): number of bins of the histogram
    """

    feature_key: FeatureKey
    # histogram range and number of bins
    low: float
    high: float
    num_bins: int


class Histogram(BaseDataStatistic[HistogramConfig, list[int]]):
    """Histogram Data Statistic Config.

    Build a histogram of a given value feature.
    """

    def _compute_histogram(self, x: NDArray) -> tuple[NDArray, NDArray]:
        # clip values in valid range
        x = np.clip(x, self.config.low, self.config.high)
        # find bin to each value
        bin_size = (self.config.high - self.config.low) / (
            self.config.num_bins - 1
        )
        bins = ((x - self.config.low) // bin_size).astype(np.int32)
        # build histogram for current examples from bins
        return np.unique(bins, return_counts=True)

    def initial_value(
        self, features: Features, manager: mp.Manager
    ) -> list[int]:
        """Initial histogram of all zeros.

        The return value is a list proxy to allow to share
        it between processes instead of copying the whole
        histogram to each process.

        Arguments:
            features (Features): input dataset features
            manager (mp.Manager): multiprocessing manager

        Returns:
            init_val (list[int]): inital histogram of all zeros
        """
        return manager.list([0] * self.config.num_bins)

    def check_features(self, features: Features) -> None:
        """Check input features.

        Makes sure the feature key specified in the configuration is present
        in the features and the feature type is a scalar value.

        Arguments:
            features (Features): input dataset features
        """
        raise_feature_equals(
            self.config.feature_key,
            self.config.feature_key.index_features(features),
            INT_TYPES + UINT_TYPES + FLOAT_TYPES,
        )

    def extract(
        self,
        examples: dict[str, list[Any]],
        index: list[int],
        rank: int,
    ) -> tuple[NDArray, NDArray]:
        """Compute the histogram for the given batch of examples.

        Arguments:
            examples (dict[str, list[Any]]): batch of examples
            index (list[int]): dataset indices of the batch of examples
            rank (int): execution process rank

        Returns:
            bin_ids (NDArray): array of integers containing the bin ids
            bin_counts (NDArray): array of integers containing the bin counts
        """
        x = self.config.feature_key.index_batch(examples)
        return self._compute_histogram(np.asarray(x))

    def compute(
        self,
        val: list[int],
        ext: tuple[NDArray, NDArray],
    ) -> tuple[NDArray, NDArray]:
        """Compute the total sub-histogram for the current batch of examples.

        The total sub-histogram is the sub-histogram computed by the `extract`
        function with the counts being the total counts computed by adding the
        values of the current histogram.

        Arguments:
            val (list[int]): current histogram
            ext (tuple[NDArray, NDArray]): extracted sub-histogram

        Returns:
            bin_ids (NDArray): array of integers containing the bin ids
            total_bin_counts (NDArray):
                array of integers containing the total bin counts
        """
        # add values of original histogram
        bin_ids, bin_counts = ext
        return bin_ids, bin_counts + np.asarray([val[i] for i in bin_ids])

    def update(
        self, report: StatisticsReportStorage, val: tuple[NDArray, NDArray]
    ) -> None:
        """Write the new histogram values to the report.

        Arguments:
            report (StatisticsReportStorage):
                report storage to update the statistic in
            val (tuple[NDArray, NDArray]): total sub-histogram
        """
        # get histogram
        hist = report.get(self.config.statistic_key)
        # write new values to histogram
        bin_ids, bin_counts = val
        for i, c in zip(bin_ids, bin_counts):
            hist[i] = c

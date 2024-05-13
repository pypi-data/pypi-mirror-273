"""Apply Index Spans Data Processor."""
from typing import Any

import numpy as np
from datasets import Features

from hyped.common.feature_checks import (
    INDEX_TYPES,
    check_feature_equals,
    check_feature_is_sequence,
    raise_feature_is_sequence,
    raise_features_align,
)
from hyped.common.feature_key import FeatureKey
from hyped.data.processors.base import (
    BaseDataProcessor,
    BaseDataProcessorConfig,
)

from .common import SpansOutputs, make_spans_exclusive


class ApplyIndexSpansConfig(BaseDataProcessorConfig):
    """Apply Index Spans Data Processor Config.

    Let (i, j) be an index span over the span sequence A=[(b_k, e_k)]_k.
    Then the data processor computes the following output span:

        (b, e) = ((A_i)_0, (A_(j-1))_1)

    That is it computes the span (b, e) represented by (i, j)
    in the domain of A.

    Note that this is effectively the inverse operation to
    the `hyped.data.processors.spans.idx_spans.CoveredIndexSpans`
    data processor.

    Attributes:
        idx_spans_begin (FeatureKey):
            input feature containing the begin value(s) of the index span(s)
            span. Can be either a single value or a sequence of values.
        idx_spans_end (FeatureKey):
            input feature containing the end value(s) of the index span(s)
            span. Can be either a single value or a sequence of values.
        spans_begin (FeatureKey):
            input feature containing the begin values of the span sequence A.
        spans_end (FeatureKey):
            input feature containing the end values of the span sequence A.
        is_idx_spans_inclusive (bool):
            whether the end coordinates of the index span(s) are
            inclusive or exclusive. Defaults to false.
        is_spans_inclusive (bool):
            whether the end coordinates of the spans in the sequence A are
            inclusive or exclusive. Defaults to false.
    """

    # index spans
    idx_spans_begin: FeatureKey
    idx_spans_end: FeatureKey
    # span sequence
    spans_begin: FeatureKey
    spans_end: FeatureKey
    # whether the end coordinates are inclusive of exclusive
    is_idx_spans_inclusive: bool = False
    is_spans_inclusive: bool = False


class ApplyIndexSpans(BaseDataProcessor[ApplyIndexSpansConfig]):
    """Apply Index Spans Data Processor Config.

    Let (i, j) be an index span over the span sequence A=[(b_k, e_k)]_k.
    Then the data processor computes the following output span:

        (b, e) = ((A_i)_0, (A_(j-1))_1)

    That is it computes the span (b, e) represented by (i, j)
    in the domain of A.

    Note that this is effectively the inverse operation to
    the `hyped.data.processors.spans.idx_spans.CoveredIndexSpans`
    data processor.
    """

    def map_features(self, features: Features) -> Features:
        """Map dataset features.

        Check input features and return feature mapping
        for token-level span annotations.

        Arguments:
            features (Features): input dataset features

        Returns:
            out (Features): token-level span annotation features
        """
        # get all input features
        idx_spans_begin = self.config.idx_spans_begin.index_features(features)
        idx_spans_end = self.config.idx_spans_end.index_features(features)
        spans_begin = self.config.spans_begin.index_features(features)
        spans_end = self.config.spans_end.index_features(features)

        # index spans must either be a sequence of
        # integers or an integer value
        for key, feature in [
            (self.config.idx_spans_begin, idx_spans_begin),
            (self.config.idx_spans_end, idx_spans_end),
        ]:
            if not (
                check_feature_is_sequence(feature, INDEX_TYPES)
                or check_feature_equals(feature, INDEX_TYPES)
            ):
                raise TypeError(
                    "Expected `%s` to be an integer value or a sequence "
                    "of integers, got %s" % (key, feature)
                )

        # index spans begin and end features must align
        raise_features_align(
            self.config.idx_spans_begin,
            self.config.idx_spans_end,
            idx_spans_begin,
            idx_spans_end,
        )

        # spans must be sequence of integers
        raise_feature_is_sequence(
            self.config.spans_begin,
            spans_begin,
            INDEX_TYPES,
        )
        raise_feature_is_sequence(
            self.config.spans_begin,
            spans_end,
            INDEX_TYPES,
        )
        # and they must align excatly
        raise_features_align(
            self.config.spans_begin,
            self.config.spans_end,
            spans_begin,
            spans_end,
        )

        return Features(
            {
                SpansOutputs.BEGINS.value: idx_spans_begin,
                SpansOutputs.ENDS.value: idx_spans_end,
            }
        )

    def process(
        self, example: dict[str, Any], index: int, rank: int
    ) -> dict[str, Any]:
        """Process example.

        Arguments:
            example (dict[str, Any]): example to process
            index (int): dataset index of the example
            rank (int): execution process rank

        Returns:
            out (dict[str, Any]): processed example
        """
        # get index span values
        idx_spans_begin = self.config.idx_spans_begin.index_example(example)
        idx_spans_end = self.config.idx_spans_end.index_example(example)
        # check if it is a single value
        is_value = isinstance(idx_spans_begin, int)

        if is_value:
            idx_spans_begin = [idx_spans_begin]
            idx_spans_end = [idx_spans_end]

        # get spans and offsets
        idx_spans = zip(idx_spans_begin, idx_spans_end)
        spans = zip(
            self.config.spans_begin.index_example(example),
            self.config.spans_end.index_example(example),
        )
        # make spans exclusive
        idx_spans = make_spans_exclusive(
            idx_spans, self.config.is_idx_spans_inclusive
        )
        spans = make_spans_exclusive(spans, self.config.is_spans_inclusive)

        # convert spans to numpy arrays
        idx_spans = np.asarray(idx_spans, dtype=int).reshape(-1, 2)
        spans = np.asarray(spans, dtype=int).reshape(-1, 2)
        # apply index spans
        begins = spans[idx_spans[:, 0], 0].tolist()
        ends = spans[idx_spans[:, 1] - 1, 1].tolist()

        # unpack if necessary
        if is_value:
            begins = begins[0]
            ends = ends[0]

        return {
            SpansOutputs.BEGINS.value: begins,
            SpansOutputs.ENDS.value: ends,
        }

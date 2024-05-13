"""Relation Extraction Tagger Data Processor."""

from enum import Enum
from typing import Any

import numpy as np
from datasets import Features, Sequence, Value

from hyped.common.feature_checks import (
    INDEX_TYPES,
    get_sequence_feature,
    get_sequence_length,
    raise_feature_equals,
    raise_feature_is_sequence,
)
from hyped.common.feature_key import FeatureKey
from hyped.data.processors.base import (
    BaseDataProcessor,
    BaseDataProcessorConfig,
)

from ..spans.common import make_spans_exclusive


class RelExTaggerOutputs(str, Enum):
    """Enumeration of outputs of the relation extraction tagger."""

    MARKED_SEQUENCE = "marked_sequence"
    """Output column containing the marked input sequence"""


class RelExTaggerConfig(BaseDataProcessorConfig):
    """Relation Extraction Tagger.

    Marks source and target entities in the input sequence.

    Attributes:
        source_begin_marker (str | int):
            marker used to indicate the beginning of the source entity.
            Marker type should match the item type of the input sequence,
            i.e. string for token sequence and integer for token id sequence.
        source_end_marker (str | int):
            marker used to indicate the end of the source entity.
        target_begin_marker (str | int):
            marker used to indicate the begging of the target entity.
        target_end_marker (str | int):
            marker used to indicate the end of the target entity.
        input_sequence (FeatureKey):
            feature containing the input sequence in which to mark
            the related entities
        source_span_begin (FeatureKey):
            feature containing the begin value of the source entity span wrt.
            the input sequence
        source_span_end (FeatureKey):
            feature containing the end value of the source entity span wrt.
            the input sequence
        target_span_begin (FeatureKey):
            feature containing the begin value of the target entity span wrt.
            the input sequence
        target_span_end (FeatureKey):
            feature containing the end value of the target entity span wrt.
            the input sequence
        source_span_inclusive (bool):
            whether the end coordinate of the source span is
            inclusive or exclusive. Defaults to false.
        target_span_inclusive (bool):
            whether the end coordinate of the target span is
            inclusive or exclusive. Defaults to false.
        max_sequence_length (None | int):
            if set the input sequence is truncated around the entities to the
            specified adhere to the specified maximum sequence length.
            Examples where the distance between entities exceeds the maximum
            length are filtered
    """

    # source entity markers
    source_begin_marker: str | int
    source_end_marker: str | int
    # target entity markers
    target_begin_marker: str | int
    target_end_marker: str | int

    input_sequence: FeatureKey
    # source entity span
    source_span_begin: FeatureKey
    source_span_end: FeatureKey
    # target entity span
    target_span_begin: FeatureKey
    target_span_end: FeatureKey

    # span inclusive or not
    source_span_inclusive: bool = False
    target_span_inclusive: bool = False

    # maximum allowed sequence length
    max_sequence_length: None | int = None

    @property
    def markers(self) -> list[str | int]:
        """List of Source and Target markers."""
        return [
            self.source_begin_marker,
            self.source_end_marker,
            self.target_begin_marker,
            self.target_end_marker,
        ]


class RelExTagger(BaseDataProcessor[RelExTaggerConfig]):
    """Relation Extraction Tagger.

    Marks source and target entities in the input sequence.
    """

    def _marked_sequence_feature(self, sequence: Sequence) -> Sequence:
        """Marked sequence feature.

        Arguments:
            sequence (Sequence): source sequence feature

        Returns:
            marked_sequence (Sequence): marked sequence feature
        """
        # increase length by four to account for the entity markers
        length = get_sequence_length(sequence)
        length = -1 if length == -1 else (length + 4)
        # apply maximum sequence length
        if self.config.max_sequence_length is not None:
            length = min(length, self.config.max_sequence_length)

        return Sequence(get_sequence_feature(sequence), length=length)

    def _get_sequence_value_type(self) -> Value | list[Value]:
        """Get sequence value type.

        Check the marker configuration and infer the expected
        value type of the items in the input sequence from it.

        Returns:
            value_type (Value | list[Value]): expected value type(s)
        """
        if (
            isinstance(self.config.source_begin_marker, str)
            and isinstance(self.config.source_end_marker, str)
            and isinstance(self.config.target_begin_marker, str)
            and isinstance(self.config.target_end_marker, str)
        ):
            # when the markers are of type string then the input
            # sequence is expected to be a token sequence, i.e.
            # a sequence of strings
            return Value("string")

        elif (
            isinstance(self.config.source_begin_marker, int)
            and isinstance(self.config.source_end_marker, int)
            and isinstance(self.config.target_begin_marker, int)
            and isinstance(self.config.target_end_marker, int)
        ):
            # when the markers are of type int then the input
            # sequence is expected to be a token id sequence
            return INDEX_TYPES

        else:
            # the marker types are either invalid or do not match
            raise TypeError(
                "Marker types must all either be str or int, "
                "got %s, %s, %s, %s"
                % (
                    self.config.source_begin_marker,
                    self.config.source_end_marker,
                    self.config.target_begin_marker,
                    self.config.target_end_marker,
                )
            )

    def map_features(self, features: Features) -> Features:
        """Map input features to *new* features.

        Arguments:
            features (Features): input dataset features

        Returns:
            out (Features): new dataset features
        """
        # make sure the maximum sequence length value is valid if set
        if (self.config.max_sequence_length is not None) and (
            self.config.max_sequence_length <= 0
        ):
            raise ValueError(
                "Expected maximum sequence length to be a positive non-zero "
                "value, got %s" % self.config.max_sequence_length
            )

        # infer expected sequence value type from config
        value_type = self._get_sequence_value_type()

        # make sure input feature exists
        sequence = self.config.input_sequence.index_features(features)
        raise_feature_is_sequence(
            self.config.input_sequence,
            sequence,
            value_type,
        )

        for key in [
            self.config.source_span_begin,
            self.config.source_span_end,
            self.config.target_span_begin,
            self.config.target_span_end,
        ]:
            # make sure span exists and is of expected type
            feature = key.index_features(features)
            raise_feature_equals(key, feature, INDEX_TYPES)

        # build output feature
        out_feature = self._marked_sequence_feature(sequence)
        return {RelExTaggerOutputs.MARKED_SEQUENCE.value: out_feature}

    def process(
        self, example: dict[str, Any], index: int, rank: int
    ) -> dict[str, Any]:
        """Process given example.

        Arguments:
            example (dict[str, Any]): example to process
            index (int): dataset index of the example
            rank (int): execution process rank

        Returns:
            out (dict[str, Any]): output

        """
        # get input sequence from example
        input_sequence = self.config.input_sequence.index_example(example)
        input_sequence = list(input_sequence)
        l = len(input_sequence)  # noqa: E741

        # get source and target spans
        src_span = (
            self.config.source_span_begin.index_example(example),
            self.config.source_span_end.index_example(example),
        )
        tgt_span = (
            self.config.target_span_begin.index_example(example),
            self.config.target_span_end.index_example(example),
        )
        # make spans exclusive, that is the end coordinate points
        # to the first item after the entity as the marker will be
        # inserted before the item
        src_span = make_spans_exclusive(
            [src_span], self.config.source_span_inclusive
        )[0]
        tgt_span = make_spans_exclusive(
            [tgt_span], self.config.target_span_inclusive
        )[0]
        # concatenate spans for ease of use later
        spans = np.asarray([*src_span, *tgt_span], dtype=int)

        if self.config.max_sequence_length is not None:
            i, j = min(spans), max(spans)
            # check if the example exceeds the maximum sequence length
            if j - i > self.config.max_sequence_length:
                # filter out the example
                return

            # compute the budget of tokens to spend
            # accounting for the four markers
            d = self.config.max_sequence_length - 4 - (j - i)
            # compute sub-sequence span containing source
            # and target entities
            i = max(0, i - d // 2)
            j = min(l, i + self.config.max_sequence_length - 4)
            i = max(0, j - (self.config.max_sequence_length - 4))

            # get the relevant sub-sequence
            # and update the spans accordingly
            input_sequence = input_sequence[i:j]
            spans -= i

        # insert markers from back to front
        # sort markers by their actual positions and insert begin
        # markers before end markers to avoid overlaps in case
        # begin and end position are equal (ends are exclusive)
        for i in sorted(range(4), key=lambda i: (-spans[i] - i // 2)):
            input_sequence.insert(spans[i], self.config.markers[i])

        # remove dummy item at the end of the sequence and return
        yield {RelExTaggerOutputs.MARKED_SEQUENCE.value: input_sequence}

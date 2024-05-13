"""Begin-In-Out (BIO) Tagger Data Processor."""

from enum import Enum
from typing import Any

import numpy as np
from datasets import ClassLabel, Features, Sequence, Value

from hyped.common.feature_checks import (
    INDEX_TYPES,
    get_sequence_feature,
    get_sequence_length,
    raise_feature_is_sequence,
    raise_features_align,
)
from hyped.common.feature_key import FeatureKey
from hyped.data.processors.base import (
    BaseDataProcessor,
    BaseDataProcessorConfig,
)

from ..spans.common import make_spans_exclusive


class BioTaggerOutputs(str, Enum):
    """Enumeration of outputs of the bio tagger processor."""

    BIO_TAGS = "bio_tags"
    """Output column containing the generated bio tag sequence"""


class BioTaggerConfig(BaseDataProcessorConfig):
    """Begin-In-Out (BIO) Tagger Config.

    Convert Entity span annotations to per-token labels
    using the BIO-tagging scheme.

    Attributes:
        begin_tag_prefix (str):
            tag prefix used to mark the beginning of a new entity
            of a specific class
        in_tag_prefix (str):
            tag prefix used to mark the interior of an entity
            of a specific class
        out_tag (str):
            out tag used to mark tokens that are not part of any entity
        input_sequence (FeatureKey):
            feature containing the input sequence
        mask (None | FeatureKey):
            feature containing a mask specifying items to ignore in the
            input sequence. The corresponding items in the generated bio
            tag sequence will be set to INV or -100. Typically this is
            set to the `HuggingFaceTokenizerOutputs.SPECIAL_TOKENS_MASK`.
        entity_spans_begin (FeatureKey):
            feature containing begins of the entity span annotations
        entity_spans_end (FeatureKey):
            feature containing ends of the entity span annotations
        entity_spans_label (FeatureKey):
            feature containing the entity class label to each entity
            span
        entity_spans_inclusive (bool):
            whether the end coordinate of the entity spans are
            inclusive or exclusive. Defaults to false.
    """

    begin_tag_prefix: str = "B-"
    in_tag_prefix: str = "I-"
    out_tag: str = "O"

    input_sequence: FeatureKey
    mask: None | FeatureKey = None
    entity_spans_begin: FeatureKey
    entity_spans_end: FeatureKey
    entity_spans_label: FeatureKey

    entity_spans_inclusive: bool = False


class BioTagger(BaseDataProcessor[BioTaggerConfig]):
    """Begin-In-Out (BIO) Tagger Config.

    Convert Entity span annotations to per-token labels
    using the BIO-tagging scheme.
    """

    INVALID_TAG = "INV"
    INVALID_VAL = -100

    @property
    def entity_label_space(self) -> None | ClassLabel:
        """Entity label-space extracted from input features."""
        feature = self.config.entity_spans_label.index_features(
            self.in_features
        )
        feature = get_sequence_feature(feature)
        return feature if isinstance(feature, ClassLabel) else None

    @property
    def bio_label_space(self) -> None | ClassLabel:
        """Bio tags label-space extracted from new features."""
        feature = self.raw_features[BioTaggerOutputs.BIO_TAGS]
        feature = get_sequence_feature(feature)
        return feature if isinstance(feature, ClassLabel) else None

    def _tag_sequence_feature(self, features: Features) -> Sequence:
        """Tag sequence feature.

        Build the tag sequence dataset feature given the input
        feature mapping.

        If the entity labels feature is a sequence of class labels, then
        the bio tag label-space is inferred from it by applying the BIO
        label scheme. Otherwise the tag sequence will be a sequence of
        strings.

        Arguments:
            features (Features): input dataset features

        Returns:
            tag_seq (Sequence): the dataset feature for the bio tags
        """
        # get input sequence and entity spans label feature
        input_sequence = self.config.input_sequence.index_features(features)
        entity_spans_label = self.config.entity_spans_label.index_features(
            features
        )
        # the entity class label feature must be a sequence of
        # string values or class labels
        raise_feature_is_sequence(
            self.config.entity_spans_label,
            entity_spans_label,
            [Value("string"), ClassLabel],
        )
        # get the item feature type and length of the sequence
        feature = get_sequence_feature(entity_spans_label)
        length = get_sequence_length(input_sequence)

        # build output feature type
        if isinstance(feature, ClassLabel):
            bio_feature_type = ClassLabel(
                names=[self.config.out_tag]
                + [
                    "%s%s" % (prefix, label)
                    for label in feature.names
                    for prefix in [
                        self.config.begin_tag_prefix,
                        self.config.in_tag_prefix,
                    ]
                ]
            )

            return Sequence(bio_feature_type, length=length)

        # otherwise the input feature type must be string
        # in which case keep it a string
        return Sequence(Value("string"), length=length)

    def map_features(self, features: Features) -> Features:
        """Map dataaset features.

        Check input features and return feature mapping
        for the bio tags.

        Arguments:
            features (Features): input dataset features

        Returns:
            out (Features): bio tags feature mapping
        """
        # make sure the input sequence exists and is a sequence
        input_sequence = self.config.input_sequence.index_features(features)
        raise_feature_is_sequence(self.config.input_sequence, input_sequence)

        # make sure the invalid mask exists and is a sequence when set
        if self.config.mask:
            mask = self.config.mask.index_features(features)
            raise_feature_is_sequence(
                self.config.mask, mask, [Value("bool")] + INDEX_TYPES
            )

        # make sure entity spans exist and are of correct type
        entity_spans_begin = self.config.entity_spans_begin.index_features(
            features
        )
        entity_spans_end = self.config.entity_spans_end.index_features(
            features
        )
        # begin and end sequences should contain indices
        raise_feature_is_sequence(
            self.config.entity_spans_begin,
            entity_spans_begin,
            INDEX_TYPES,
        )
        raise_feature_is_sequence(
            self.config.entity_spans_end,
            entity_spans_end,
            INDEX_TYPES,
        )
        raise_features_align(
            self.config.entity_spans_begin,
            self.config.entity_spans_end,
            entity_spans_begin,
            entity_spans_end,
        )

        return {
            BioTaggerOutputs.BIO_TAGS: self._tag_sequence_feature(features)
        }

    def process(
        self, example: dict[str, Any], index: int, rank: int
    ) -> dict[str, Any]:
        """Apply processor to an example.

        Arguments:
            example (dict[str, Any]): example to process
            index (int): dataset index of the example
            rank (int): execution process rank

        Returns:
            out (dict[str, Any]): token-level span annotations
        """
        # get length of input sequence
        length = len(self.config.input_sequence.index_example(example))
        # get the invalid mask
        if self.config.mask is not None:
            mask = self.config.mask.index_example(example)
            mask = np.asarray(mask, dtype=bool)
        else:
            mask = np.full(length, fill_value=False, dtype=bool)

        # get entity spans
        spans = zip(
            self.config.entity_spans_begin.index_example(example),
            self.config.entity_spans_end.index_example(example),
        )
        # make entity spans exclusive and filter overlapping spans
        spans = make_spans_exclusive(spans, self.config.entity_spans_inclusive)

        # get the entity labels
        labels = self.config.entity_spans_label.index_example(example)
        # convert label ids to label strings
        if self.entity_label_space is not None:
            labels = self.entity_label_space.int2str(labels)

        # build initial tag sequence of all out and invalid tags
        tags = np.full(length, fill_value=self.config.out_tag, dtype=object)
        tags[mask] = type(self).INVALID_TAG

        # insert all entity spans
        for label, (b, e) in zip(labels, spans):
            # check for overlaps with previous annotations
            if (tags[b:e] != self.config.out_tag).any():
                # get the overlapping entity types
                overlap_types = [label] + [
                    (
                        tag.removeprefix(
                            self.config.begin_tag_prefix
                        ).removeprefix(self.config.in_tag_prefix)
                    )
                    for tag in tags[b:e]
                    if tag != self.config.out_tag
                ]
                # raise error on overlap
                raise ValueError(
                    "Detected overlap between entities of types %s"
                    % ", ".join(overlap_types)
                )

            # add entity to tag sequence
            tags[b:e] = "%s%s" % (self.config.in_tag_prefix, label)
            tags[b] = "%s%s" % (self.config.begin_tag_prefix, label)

        # convert label strings to label ids
        if self.bio_label_space is not None:
            tags[mask] = type(self).INVALID_VAL
            tags[~mask] = self.bio_label_space.str2int(tags[~mask].tolist())

        # return bio tags
        return {BioTaggerOutputs.BIO_TAGS: tags.tolist()}

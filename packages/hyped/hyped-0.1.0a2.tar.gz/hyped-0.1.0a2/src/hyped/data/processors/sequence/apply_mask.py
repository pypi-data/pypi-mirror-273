"""Apply Mask Data Processor."""
from itertools import compress
from typing import Any

from datasets import Features, Sequence, Value

from hyped.common.feature_checks import (
    get_sequence_feature,
    get_sequence_length,
    raise_feature_is_sequence,
)
from hyped.common.feature_key import FeatureKey
from hyped.data.processors.base import (
    BaseDataProcessor,
    BaseDataProcessorConfig,
)


class ApplyMaskConfig(BaseDataProcessorConfig):
    """Apply Mask Data Processor Config.

    Apply a given mask onto a set of sequences

    Attributes:
        mask (FeatureKey):
            the feature key refering to the mask to apply
        sequences (dict[str, FeatureKey]):
            Collection of feature keys referring to the sequences
            to which to apply the mask. The mask is applied to each
            features referenced by the given keys. The resulting
            masked sequence will be stored under the dictionary key.
    """

    mask: FeatureKey
    sequences: dict[str, FeatureKey]


class ApplyMask(BaseDataProcessor[ApplyMaskConfig]):
    """Apply Mask Data Processor.

    Apply a given mask onto a set of sequences
    """

    def map_features(self, features: Features) -> Features:
        """Map dataset features.

        Check mask and sequence features and overwrite sequence
        features.

        Arguments:
            features (Features): input dataset features

        Returns:
            out (Features): sequence features to overwrite
        """
        # check mask feature exists and is a sequence of booleans
        mask = self.config.mask.index_features(features)
        raise_feature_is_sequence(self.config.mask, mask, Value("bool"))
        # get the length of the mask
        length = get_sequence_length(mask)

        out_features = Features()
        # check each sequence feature
        for name, key in self.config.sequences.items():
            # make sure it exists and is a sequence
            seq = key.index_features(features)
            raise_feature_is_sequence(key, seq)
            # it has to be of the same size as the mask
            if length != get_sequence_length(seq):
                raise TypeError(
                    "Length mismatch between mask sequence `%s` and "
                    "sequence `%s`, got %i != %i"
                    % (
                        self.config.mask,
                        key,
                        length,
                        get_sequence_length(seq),
                    )
                )
            # add sequence feature to output features
            out_features[name] = Sequence(get_sequence_feature(seq))

        # return all collected output features
        return out_features

    def process(
        self, example: dict[str, Any], index: int, rank: int
    ) -> dict[str, Any]:
        """Apply processor to an example.

        Arguments:
            example (dict[str, Any]): example to process
            index (int): dataset index of the example
            rank (int): execution process rank

        Returns:
            out (dict[str, Any]):
        """
        # get the mask
        mask = self.config.mask.index_example(example)

        out = {}
        # apply mask to each sequence
        for name, key in self.config.sequences.items():
            seq = key.index_example(example)
            # check length
            if len(seq) != len(mask):
                raise ValueError(
                    "Length mismatch between mask sequence `%s` and "
                    "sequence `%s`, got %i != %i"
                    % (self.config.mask, key, len(mask), len(seq))
                )
            # apply mask to sequence
            out[name] = list(compress(seq, mask))

        return out

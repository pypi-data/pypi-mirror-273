"""Token Spans from Word Ids Processor."""
from typing import Any

import numpy as np
from datasets import Features, Sequence, Value

from hyped.common.feature_checks import INDEX_TYPES, raise_feature_is_sequence
from hyped.common.feature_key import FeatureKey
from hyped.data.processors.base import (
    BaseDataProcessor,
    BaseDataProcessorConfig,
)
from hyped.data.processors.tokenizers.hf import HuggingFaceTokenizerOutputs

from .common import SpansOutputs


class TokenSpansFromWordIdsConfig(BaseDataProcessorConfig):
    """Token Spans from Word Ids Processor Config.

    Convert word-ids to token-level spans. Word-ids are typically
    provided by the tokenizer (see `HuggingFaceTokenizer`).

    Attributes:
        word_ids (FeatureKey):
            column containing the word-ids to parse.
            Defaults to `HuggingFaceTokenizerOutputs.WORD_IDS`
        mask (None | FeatureKey):
            column containing mask over words indicating which items
            in the `word_ids` sequence to ignore for building the spans.
            If set to None, all values in the word-ids sequence are
            considered. Defaults to
            `HuggingFaceTokenizerOutputs.SPECIAL_TOKENS_MASK`.
    """

    word_ids: FeatureKey = HuggingFaceTokenizerOutputs.WORD_IDS.value
    mask: None | FeatureKey = (
        HuggingFaceTokenizerOutputs.SPECIAL_TOKENS_MASK.value
    )


class TokenSpansFromWordIds(BaseDataProcessor[TokenSpansFromWordIdsConfig]):
    """Token Spans from Word Ids Processor Config.

    Convert word-ids to token-level spans. Word-ids are typically
    provided by the tokenizer (see `HuggingFaceTokenizer`).
    """

    def __init__(
        self,
        config: TokenSpansFromWordIdsConfig = TokenSpansFromWordIdsConfig(),
    ) -> None:
        """Initialize Data Processor."""
        super(TokenSpansFromWordIds, self).__init__(config)

    def map_features(self, features: Features) -> Features:
        """Check word-ids feature and return token level span features.

        Arguments:
            features (Features): input features

        Returns:
            out (Features): span features
        """
        # make sure word ids feature exists and is a sequence of indices
        word_ids = self.config.word_ids.index_features(features)
        raise_feature_is_sequence(self.config.word_ids, word_ids, INDEX_TYPES)
        # make sure mask is valid if specified
        if self.config.mask is not None:
            mask = self.config.mask.index_features(features)
            raise_feature_is_sequence(
                self.config.mask,
                mask,
                [Value("bool")] + INDEX_TYPES,
            )
        # return token-level span features
        return {
            SpansOutputs.BEGINS.value: Sequence(Value("int32")),
            SpansOutputs.ENDS.value: Sequence(Value("int32")),
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
            out (dict[str, Any]): token-level spans
        """
        # get word ids from example and convert to numpy array
        word_ids = self.config.word_ids.index_example(example)
        word_ids = np.asarray(word_ids)

        if self.config.mask is not None:
            # get mask from example and convert to numpy array
            # also invert it to get a mask indicating valid items
            mask = self.config.mask.index_example(example)
            mask = ~np.asarray(mask).astype(bool)
        else:
            # create a dummy mask of all trues when mask is not specified
            mask = np.full_like(word_ids, fill_value=True, dtype=bool)

        # apply mask to word ids
        masked_word_ids = word_ids[mask]

        # check word ids
        if (masked_word_ids[:-1] > masked_word_ids[1:]).any():
            raise ValueError(
                "Word id sequence must be monotonically increasing, got %s"
                % masked_word_ids
            )

        word_bounds_mask = word_ids[:-1] != word_ids[1:]
        # identify the beginnings of words
        word_begins_mask = np.append(True, word_bounds_mask)
        word_begins_mask &= mask
        # identify the ends of words
        word_ends_mask = np.append(word_bounds_mask, True)
        word_ends_mask &= mask
        # get the indices, that is the index spans
        (word_begins,) = word_begins_mask.nonzero()
        (word_ends,) = word_ends_mask.nonzero()
        # make word-spans exclusive
        word_ends += 1

        return {
            SpansOutputs.BEGINS.value: word_begins.tolist(),
            SpansOutputs.ENDS.value: word_ends.tolist(),
        }

"""Huggingface Transformers Tokenizer Data Processor."""

from enum import Enum
from typing import Annotated, Any

from datasets import Features, Sequence, Value
from pydantic import ConfigDict, SkipValidation
from transformers import (
    AutoTokenizer,
    LayoutXLMTokenizer,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)
from transformers.tokenization_utils_base import TruncationStrategy
from transformers.utils import PaddingStrategy

from hyped.common.feature_checks import (
    INT_TYPES,
    UINT_TYPES,
    raise_feature_equals,
    raise_feature_is_sequence,
)
from hyped.common.feature_key import FeatureKey
from hyped.data.processors.base import (
    BaseDataProcessor,
    BaseDataProcessorConfig,
)


class HuggingFaceTokenizerOutputs(str, Enum):
    """Enumeration of the outputs of the HuggingFace (transformers) Tokenizer.

    Note that some of the output columns are optional and controlled by the
    specific type of tokenizer and the configuration. Furthermore there might
    be outputs of tokenizer that are not explicitly listed here.

    For more information on each output please refer to the transformers
    documentation.
    """

    TOKENS = "tokens"
    """Output column containing the token sequence"""

    INPUT_IDS = "input_ids"
    """Output column containing the input id sequence"""

    TOKEN_TYPE_IDS = "token_type_ids"
    """Output column containing the token type id sequence. Only available
    when `return_token_type_ids=True` in the configuration."""

    ATTENTION_MASK = "attention_mask"
    """Output column containing the token type id sequence. Only available
    when `return_attention_mask=True` in the configuration."""

    OVERFLOW_TO_SAMPLE_MAPPING = "overflow_to_sample_mapping"
    """Output column containing the overflow to sample mapping. Only available
    when `return_overflowing_tokens=True` in the configuration."""

    SPECIAL_TOKENS_MASK = "special_tokens_mask"
    """Output column containing the special tokens mask. Only available when
    `return_special_tokens_mask=True` in the configuration."""

    OFFSETS_MAPPING = "offset_mapping"
    """Output column containing the character offsets of each token. Only
    available when `return_offsets_mapping=True` in the configuration."""

    LENGTH = "length"
    """Output column containing the length of the tokenized sequence. Only
    available when `return_length=True` in the configuration."""

    WORD_IDS = "word_ids"
    """Output column containing the word-id sequence mapping each token to
    the index word it is a part of. Only available when `return_word_ids=True`
    in the configuration."""


class HuggingFaceTokenizerConfig(BaseDataProcessorConfig):
    """HuggingFace (Transformers) Tokenizer Config.

    Data Processor applying a pre-trained huggingface tokenizer.
    For more information please refer to the documentation of
    the hugginface transformers `PreTrainedTokenizer` class.

    Attributes:
        tokenizer (str | PreTrainedTokenizer):
            the pre-trained tokenizer to apply. Either the uri or local
            path to load the tokenizer from using `AutoTokenizer`, or
            the pre-trained tokenizer object.
        text (None | FeatureKey):
            feature to pass as `text` keyword argument
            to the tokenizer. Defaults to `text`.
        text_pair (None | FeatureKey):
            feature to pass as `text_pair` keyword argument
            to the tokenizer
        text_target (None | FeatureKey):
            feature to pass as `text_target` keyword argument
            to the tokenizer
        text_pair_target (None | FeatureKey):
            feature to pass as `text_pair_target` keyword argument
            to the tokenizer
        boxes (None | FeatureKey):
            feature to pass as `boxes` to the tokenizer.
            Required for `LayoutXLMTokenizer`.
        add_special_tokens (None | bool):
            whether to add special tokens to the tokenized sequence.
            Defaults to true.
        padding (bool | str | PaddingStrategy):
            Activate and control padding of the tokenized sequence.
            Defaults to False. See `PreTrainedTokenizer.call` for more
            information.
        truncation (bool | str | TruncationSrategy):
            Activate and control truncation of the tokenized sequence.
            Defaults to False. See `PreTrainedTokenizer.call` for more
            information.
        max_length (None | str):
            the maximum length to be used by the truncation and padding
            strategy.
        stride (int):
            overflowing tokens will have overlap of this value with the
            truncated sequence. Defaults to zero, effectively deactivating
            striding.
        is_split_into_words (bool):
            whether the text inputs are already pre-tokenized into words.
            Defaults to false.
        pad_to_multiple_of (None | int):
            when set, the sequence will be padded to a multiple of
            the specified value
        return_tokens (bool):
            whether to return the token sequence
        return_token_type_ids (bool):
            whether to return the token type ids
        return_attention_mask (bool):
            whether to return the attention mask
        return_special_tokens_mask (bool):
            whether to return the special tokens mask
        return_offsets_mapping (bool):
            whether to return the character offset mapping. Only availabel
            for fast tokenizers.
        return_length (bool):
            whether to return the sequence length
        return_word_ids (bool):
            whether to return the word ids for each token. Only available
            for fast tokenizers. Defaults to false.
    """

    # allow tokenizer type in pydantic model
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tokenizer: Annotated[
        str | PreTrainedTokenizer, SkipValidation
    ] = "bert-base-uncased"
    # text input to tokenize
    text: None | FeatureKey = "text"
    text_pair: None | FeatureKey = None
    text_target: None | FeatureKey = None
    text_pair_target: None | FeatureKey = None
    boxes: None | FeatureKey = None
    # post-processing
    add_special_tokens: bool = True
    padding: bool | str | PaddingStrategy = False
    truncation: bool | str | TruncationStrategy = False
    max_length: None | int = None
    stride: int = 0
    is_split_into_words: bool = False
    pad_to_multiple_of: None | int = None
    # output features
    return_tokens: bool = False
    return_token_type_ids: bool = False
    return_attention_mask: bool = False
    return_special_tokens_mask: bool = False
    return_offsets_mapping: bool = False
    return_length: bool = False
    return_word_ids: bool = False


class HuggingFaceTokenizer(BaseDataProcessor[HuggingFaceTokenizerConfig]):
    """HuggingFace (Transformers) Tokenizer.

    Data Processor applying a pre-trained huggingface tokenizer.
    For more information please refer to the documentation of
    the hugginface transformers `PreTrainedTokenizer` class.
    """

    # feature keys for which the value must be extracted from the example
    # and who's values are specified directly in the configuration
    KWARGS_FROM_EXAMPLE = [
        "text",
        "text_pair",
        "text_target",
        "text_pair_target",
        "boxes",
    ]
    KWARGS_FROM_CONFIG = [
        "add_special_tokens",
        "padding",
        "truncation",
        "max_length",
        "stride",
        "is_split_into_words",
        "pad_to_multiple_of",
        "return_token_type_ids",
        "return_attention_mask",
        "return_special_tokens_mask",
        "return_offsets_mapping",
        "return_length",
    ]

    def __init__(self, config: HuggingFaceTokenizerConfig) -> None:
        """Initialize the data processor.

        Arguments:
            config (HuggingFaceTokenizerConfig): processor configuration
        """
        super(HuggingFaceTokenizer, self).__init__(config)
        # prepare tokenizer
        tokenizer = self.config.tokenizer
        tokenizer = (
            tokenizer
            if isinstance(
                tokenizer, (PreTrainedTokenizer, PreTrainedTokenizerFast)
            )
            else AutoTokenizer.from_pretrained(
                tokenizer, use_fast=True, add_prefix_space=True
            )
        )
        self.tokenizer = tokenizer

        # check if requested functionality is present
        if not tokenizer.is_fast:
            if self.config.return_offsets_mapping:
                raise ValueError(
                    "Offsets mapping is only available for fast "
                    "tokenizers, got %s" % self.tokenizer
                )
            if self.config.return_word_ids:
                raise ValueError(
                    "Word IDs is only available for fast tokenizers"
                    ",got %s" % self.tokenizer
                )

    def _check_text_feature(self, key: FeatureKey, features: Features) -> None:
        """Check textual input dataset features.

        Raises KeyError when the key is not present in the feature mapping.
        Raises TypeError when the feature type is invalid, i.e. when the
        feature is of type string but expected token sequence or vise versa.

        Arguments:
            key (FeatureKey): feature key to check
            features (Features): feature mapping
        """
        # make sure feature exists
        feature = key.index_features(features)
        # check type
        if self.config.is_split_into_words:
            # when pre-tokenized the input should be a sequence of strings
            raise_feature_is_sequence(key, feature, Value("string"))

        else:
            # otherwise it should simply be a string
            raise_feature_equals(key, feature, Value("string"))

    def _check_input_features(self, features: Features) -> None:
        """Check input features."""
        # make sure some input is specified
        if self.config.text is None:
            raise ValueError("No text input to tokenizer specified")

        # check text input features
        for key in ["text", "text_pair", "text_target", "text_pair_target"]:
            if getattr(self.config, key) is not None:
                self._check_text_feature(getattr(self.config, key), features)

        # special case for layout-xlm
        if isinstance(self.tokenizer, LayoutXLMTokenizer):
            if not self.config.is_split_into_words:
                raise ValueError(
                    "`LayoutXLMTokenizer` expects pre-tokenized inputs"
                )

            if self.config.boxes is None:
                raise ValueError(
                    "`LayoutXLMTokenizer` requires boxes argument containing "
                    "word-level bounding boxes"
                )

            # make sure the feature exists
            boxes = self.config.boxes.index_features(features)
            # make sure its of the correct type
            raise_feature_is_sequence(
                self.config.boxes,
                boxes,
                Sequence(INT_TYPES + UINT_TYPES, length=4),
            )

    def _get_output_sequence_length(self) -> int:
        """Get output sequence length.

        Infers the (fixed) sequence length of the output sequences such
        as the `input_ids` and `attention_mask` given the config. Returns
        -1 when the sequence length is not guaranteed to be constant.

        Returns:
            length (int): the sequence length of output sequences
        """
        # check for constant length
        is_constant = (
            (self.config.max_length is not None)
            and (self.config.padding == "max_length")
            and (
                self.config.truncation
                in (True, "longest_first", "only_first", "only_second")
            )
        )
        # get sequence length in case it's constant
        return self.config.max_length if is_constant else -1

    def _build_output_features(self) -> Features:
        """Build output features.

        Build the output feature mapping based on the return options
        set in the config.

        Returns:
            features (Features): output feature mapping
        """
        # infer the output sequence length given the configuration
        length = self._get_output_sequence_length()

        out_features = Features()
        # add all fixed-length integer sequence outputs to features
        for key in [
            HuggingFaceTokenizerOutputs.INPUT_IDS.value,
            HuggingFaceTokenizerOutputs.TOKEN_TYPE_IDS.value,
            HuggingFaceTokenizerOutputs.ATTENTION_MASK.value,
            HuggingFaceTokenizerOutputs.SPECIAL_TOKENS_MASK.value,
            HuggingFaceTokenizerOutputs.WORD_IDS.value,
        ]:
            if (key == HuggingFaceTokenizerOutputs.INPUT_IDS.value) or getattr(
                self.config, "return_%s" % key
            ):
                out_features[key] = Sequence(
                    Value(dtype="int32"), length=length
                )

        if self.config.return_tokens:
            out_features[HuggingFaceTokenizerOutputs.TOKENS.value] = Sequence(
                Value(dtype="string"), length=length
            )

        if self.config.return_offsets_mapping:
            out_features[
                HuggingFaceTokenizerOutputs.OFFSETS_MAPPING.value
            ] = Sequence(Sequence(Value("int32"), length=2), length=length)

        if self.config.return_length:
            # length output is nested into a sequence of length one
            out_features[HuggingFaceTokenizerOutputs.LENGTH.value] = Value(
                "int32"
            )

        return out_features

    def map_features(self, features: Features) -> Features:
        """Check tokenizer input and return output features.

        Arguments:
            features (Features): the input dataset features

        Returns:
            new_features (Features): features generated by the tokenizer
        """
        # check features and build output features
        self._check_input_features(features)
        return self._build_output_features()

    def _build_kwargs(self, examples: dict[str, list[Any]]) -> dict[str, Any]:
        """Build/Collect all input features required for tokenization.

        Collects features from the example according
        `HuggingFaceTokenizer.KWARGS_FROM_EXAMPLE`.
        Collects features/flags from the configuration according to
        `HuggingFaceTokenizer.KWAGRS_FROM_CONFIG`.

        Arguments:
            examples (dict[str, list[Any]):
                the input batch of examples to tokenize

        Returns:
            kwargs (dict[str, Any]):
                input keyword arguments to the call method of the tokenizer
        """
        kwargs = {}
        # collect all features form the example
        for key in type(self).KWARGS_FROM_EXAMPLE:
            if getattr(self.config, key) is not None:
                kwargs[key] = getattr(self.config, key).index_batch(examples)
        # add all options kwargs specified in the config
        for key in type(self).KWARGS_FROM_CONFIG:
            kwargs[key] = getattr(self.config, key)
        # return the keyword arguments
        return kwargs

    def internal_batch_process(
        self, examples: dict[str, list[Any]], index: list[int], rank: int
    ) -> tuple[dict[str, list[Any]], list[int]]:
        """Tokenize a batch of examples.

        Arguments:
            examples (dict[str, list[Any]]): batch of examples to process
            index (list[int]): dataset indices of the examples
            rank (int): execution process rank

        Returns:
            out_batch (dict[str, list[Any]]): tokenized examples
            index (list[int]): pass through of the input indices
        """
        # apply tokenizer
        kwargs = self._build_kwargs(examples)
        enc = self.tokenizer(**kwargs)
        # add tokens to output
        if self.config.return_tokens:
            enc[HuggingFaceTokenizerOutputs.TOKENS.value] = list(
                map(self.tokenizer.convert_ids_to_tokens, enc.input_ids)
            )
        # add word ids to output
        if self.config.return_word_ids:
            enc[HuggingFaceTokenizerOutputs.WORD_IDS.value] = [
                [(i if i is not None else -1) for i in enc.word_ids(j)]
                for j in range(len(index))
            ]
        # convert offset mapping items to lists instead of tuples
        if self.config.return_offsets_mapping:
            enc[HuggingFaceTokenizerOutputs.OFFSETS_MAPPING.value] = [
                list(map(list, item))
                for item in enc[
                    HuggingFaceTokenizerOutputs.OFFSETS_MAPPING.value
                ]
            ]
        # convert to dict and return
        return dict(enc), list(range(len(index)))

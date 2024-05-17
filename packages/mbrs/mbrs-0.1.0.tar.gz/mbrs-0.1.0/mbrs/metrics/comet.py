from __future__ import annotations

from dataclasses import dataclass

import torch
from comet import download_model, load_from_checkpoint
from torch import Tensor

from . import MetricCacheable, register


@register("comet")
class MetricCOMET(MetricCacheable):
    """COMET metric class."""

    @dataclass
    class Config(MetricCacheable.Config):
        """COMET metric configuration.

        - model (str): Model name or path.
        - batch_size (int): Batch size.
        - fp16 (bool): Use float16 for the forward computation.
        - bf16 (bool): Use bfloat16 for the forward computation.
        - cpu (bool): Use CPU for the forward computation.
        """

        model: str = "Unbabel/wmt22-comet-da"
        batch_size: int = 64
        fp16: bool = False
        bf16: bool = False
        cpu: bool = False

    def __init__(self, cfg: MetricCOMET.Config):
        self.cfg = cfg
        self.scorer = load_from_checkpoint(download_model(cfg.model))
        self.scorer.eval()
        for param in self.scorer.parameters():
            param.requires_grad = False

        if not cfg.cpu and torch.cuda.is_available():
            self.scorer = self.scorer.cuda()
            if cfg.fp16:
                self.scorer = self.scorer.half()
            elif cfg.bf16:
                self.scorer = self.scorer.bfloat16()

    @property
    def device(self) -> torch.device:
        """Returns the device of the model."""
        return self.scorer.device

    def encode(self, sentences: list[str]) -> torch.Tensor:
        """Compute sentence embedding vectors of the given sentences.

        Args:
            sentences (list[str]): Input sentences.

        Returns:
            torch.Tensor: Sentence embeddings of shape `(N, D)`, where
              - N: the number of sentences
              - D: size of the embedding dimmension
        """
        batches = [
            self.scorer.encoder.prepare_sample(sentences[i : i + self.cfg.batch_size])
            for i in range(0, len(sentences), self.cfg.batch_size)
        ]
        embeds = []
        for batch in batches:
            emb = self.scorer.get_sentence_embedding(**batch.to(self.scorer.device))
            if self.scorer.device.type != "cpu":
                if self.cfg.fp16:
                    emb = emb.half()
                elif self.cfg.bf16:
                    emb = emb.bfloat16()
                else:
                    emb = emb.float()
            embeds.append(emb)
        embeds = torch.vstack(embeds)
        return embeds

    def out_proj(
        self, hypotheses_ir: Tensor, references_ir: Tensor, source_ir: Tensor
    ) -> Tensor:
        """Forward the output projection layer.

        Args:
            hypotheses_ir (Tensor): Intermediate representations of hypotheses.
            references_ir (Tensor): Intermediate representations of references.
            source_ir (Tensor): Intermediate representations of a source.

        Returns:
            Tensor: N scores.
        """
        return self.scorer.estimate(source_ir, hypotheses_ir, references_ir)["score"]

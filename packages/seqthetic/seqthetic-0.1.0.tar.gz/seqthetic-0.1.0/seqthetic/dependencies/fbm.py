from typing import List

from pydantic import Field
from stochastic.processes.continuous import FractionalBrownianMotion

from seqthetic.dependencies.base import BaseDependency, DependencyResult, SchemaList
from seqthetic.range import FlexibleRange
from seqthetic.utils import make_digitizer


class FBMDependency(BaseDependency):
    """
    Dependency from discretized fractional brownian motion(fBm).

    Attributes:
        hurst: Hurst exponent for the fbm
        discretize_ratio: ratio for discretizing: binning into round(length * binning_ratio) bins. range (0, 1]
        sequence_vocab_size: size of the vocabulary for each sequence
    """

    generator: str = "fbm"

    hurst: FlexibleRange = Field(..., gt=0, lt=1)
    discretize_ratio: FlexibleRange = Field(..., gt=0, le=1)
    metadata_schema: List[str] = SchemaList(["hurst", "discretize_ratio"])

    custom_seed_schema: List[str] = SchemaList(
        ["hurst", "discretize_ratio", "dependency"]
    )

    def make_dependency(self, num_sequence: int):
        # prepare random generators
        rngs = {}
        for field in ["hurst", "sequence_length", "discretize_ratio", "dependency"]:
            rngs[field] = self.seed.get_rng(field)

        dep_rngs = self.seed.get_rng("dependency", num_sequence, return_list=True)

        # sample parameters
        hursts = rngs["hurst"].uniform(self.hurst.min, self.hurst.max, num_sequence)
        if self.sequence_length.constant:
            lengths = [int(self.sequence_length.min)] * num_sequence
        else:
            lengths = rngs["sequence_length"].integers(
                self.sequence_length.min, self.sequence_length.max, num_sequence
            )
        binning_ratios = rngs["discretize_ratio"].uniform(
            self.discretize_ratio.min, self.discretize_ratio.max, num_sequence
        )
        # make digitizer
        digitizers = [make_digitizer(ratio) for ratio in binning_ratios]
        # make fbms
        fbms = [
            FractionalBrownianMotion(hurst, rng=rng)
            for hurst, rng in zip(hursts, dep_rngs)
        ]
        deps_raw = [fbm.sample(length) for length, fbm in zip(lengths, fbms)]
        dependencies = [digitize(dr) for dr, digitize in zip(deps_raw, digitizers)]
        metadata = [
            {"hurst": h, "sequence_length": l, "discretize_ratio": b}
            for h, l, b in zip(hursts, lengths, binning_ratios)
        ]
        return DependencyResult(dependencies, metadata)

import datetime
import json
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field, computed_field

from seqthetic.dependencies import adapter
from seqthetic.dependencies.base import BaseDependency
from seqthetic.mapping import MappingSpec
from seqthetic.seed import Seed, SpecSeed

from .dependencies import DependencySpec
from .utils import ID, SizeValue
from .vocabulary import VocabularySpec

# todo: insights into tasks;


class DomainSpec(BaseModel):
    """a kind of data with designated dependency"""

    id: str = ID
    mixture_ratio: float = Field(..., gt=0, le=1)  # ratio of token in the total dataset
    num_sequence: int = 0  # number of sequences in this domain
    num_token: int = 0  # number of total tokens in this domain
    mapping: MappingSpec = Field(default_factory=MappingSpec)
    dependency: DependencySpec
    comment: str = ""

    def set_dependency_seeds(self, seed: Seed):
        self.dependency.seed = seed


class SynthesisSpec(BaseModel):
    id: str = ID
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    name: str = ""
    """total token specified by user, real number may vary depending on the randomness in domains"""
    num_token: SizeValue
    vocabulary: VocabularySpec
    domains: List[DomainSpec]
    seeds: SpecSeed = Field(default_factory=SpecSeed)

    def model_post_init(self, __context):
        self.init_seeds()
        self.check_mixture_sum()
        self.update_domain_stat()

    @computed_field
    @property
    def num_token_exact(self) -> int:
        return sum([domain.num_token for domain in self.domains])

    @staticmethod
    def register_dependency(dependency: BaseDependency):
        adapter.register(dependency)

    def init_seeds(self, set_domain_seed=True, set_vocab_seed=True):
        # requires creating new seed
        if len(self.seeds.vocabulary.seeds) == 0:
            seeds = SpecSeed(
                vocabulary=Seed(seed_schema=self.vocabulary.seed_schema),
                domains=[
                    Seed(seed_schema=domain.dependency.seed_schema)
                    for domain in self.domains
                ],
            )

            self.seeds = seeds
        # if not empty, means contains seeds, often for deserializing
        # move seed to vocabulary and depdendency
        self.vocabulary.set_seed(self.seeds.vocabulary)
        if set_domain_seed:
            for domain, seed in zip(self.domains, self.seeds.domains):
                domain.set_dependency_seeds(seed)

        return self

    def seed_from_domains(self):
        self.seeds.domains = [domain.dependency.seed for domain in self.domains]

    def check_mixture_sum(self):
        mixtures = sum([domain.mixture_ratio for domain in self.domains])
        if abs(mixtures - 1) > 1e-6:
            raise ValueError("sum of mixture ratio should be 1")
        return self

    def update_domain_stat(self):
        for domain in self.domains:
            domain.num_token = round(self.num_token * domain.mixture_ratio)
            seq_len = domain.dependency.sequence_length
            if seq_len.constant:
                domain.num_sequence = int(
                    domain.num_token // domain.dependency.sequence_length.min
                )
            # todo: for not constant length sequence
        return self

    def save(self, path_str: str = "./", name: str | None = None):
        """save the dataset spec to a json file"""
        spec_json = self.model_dump_json(indent=4)
        name = name or self.id
        path = Path(path_str) / f"{name}.synspec.json"
        with open(path, "w") as f:
            f.write(spec_json)
        return str(path)

    @classmethod
    def load(cls, path: str = ""):
        with open(path, "r") as f:
            spec_dict = json.load(f)
            spec = SynthesisSpec.model_validate(spec_dict)

        return spec

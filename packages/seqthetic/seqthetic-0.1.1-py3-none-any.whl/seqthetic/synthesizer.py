import logging

import pandas as pd

from seqthetic.dataset import Dataset

from .synthesis_spec import DomainSpec, SynthesisSpec
from pydantic import BaseModel
import random


class DomainItem(BaseModel):
    dependency: list[int]
    sequence: list[int]
    domain_id: str
    metadata: dict
    split: str = "train"


class DomainResult(BaseModel):
    items: list[DomainItem]


class Synthesizer:
    def __init__(self, spec: SynthesisSpec):
        self.spec = spec
        self.vocab = spec.vocabulary.make_vocabulary()
        self.dataset = pd.DataFrame(columns=Dataset.columns)
        self.made_dataset = False

    def make_dataset(self, debug=False) -> Dataset:
        if self.made_dataset:
            return self.dataset
        if debug:
            logging.basicConfig(level=logging.DEBUG)

        domains: list[DomainResult] = [
            self._make_domain(domain, debug) for domain in self.spec.domains
        ]
        items = self._dataset_train_test_split(domains)
        self.dataset = pd.DataFrame.from_records(
            [item.model_dump() for item in items], columns=Dataset.columns
        )
        self.made_dataset = True
        return Dataset(self.spec, self.dataset)

    def _shuffle(self, seed_name: str, lst: list):
        rng = self.spec.seeds.split.get_rng(seed_name)

        rng.shuffle(lst)

    def _domain_split(self, items: list[DomainItem]):
        train_index, val_index = self.spec.split.get_index(len(items))
        for item in items[train_index:val_index]:
            item.split = "val"
        for item in items[val_index:]:
            item.split = "test"

    def _make_domain(self, domain: DomainSpec, debug=False) -> DomainResult:
        if debug:
            logging.basicConfig(level=logging.DEBUG)

        res = domain.dependency.make_dependency(domain.num_sequence)
        dependencies = res.dependencies
        metadata = res.metadata
        sequences = domain.mapping.map_to_sequence(
            dependencies, self.vocab, self.spec.vocabulary.seed
        )
        domain_id = [domain.id] * domain.num_sequence

        return DomainResult(
            items=[
                DomainItem(
                    dependency=dep, sequence=seq, domain_id=dom_id, metadata=meta
                )
                for dep, seq, dom_id, meta in zip(
                    dependencies, sequences, domain_id, metadata
                )
            ]
        )

    def _dataset_train_test_split(self, domains: list[DomainResult]):
        split_config = self.spec.split
        items = []

        if split_config.shuffle_dataset:
            items = [item for domain in domains for item in domain.items]
            self._shuffle("shuffle_dataset", items)
            self._domain_split(items)
        else:
            if split_config.shuffle_domain_order:
                self._shuffle("shuffle_domain_order", domains)
            if split_config.shuffle_domain_sequence:
                rngs = self.spec.seeds.split.get_rng(
                    "shuffle_domain_sequence", len(domains), return_list=True
                )
                for rng, domain in zip(rngs, domains):
                    rng.shuffle(domain.items)
            for domain in domains:
                self._domain_split(domain.items)
                items.extend(domain.items)
        return items

    def save_dataset(self, path: str = "./", name=""):
        if not self.made_dataset:
            raise ValueError("dataset not made yet")
        Dataset(self.spec, self.dataset).save(path, name)

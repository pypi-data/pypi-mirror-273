import logging

import pandas as pd

from seqthetic.dataset import Dataset

from .synthesis_spec import SynthesisSpec


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

        all_dependencies = []
        all_sequences = []
        all_domain_id = []
        all_metadata = []
        for domain in self.spec.domains:
            res = domain.dependency.make_dependency(domain.num_sequence)
            dependencies = res.dependencies
            metadata = res.metadata
            # todo
            sequences = domain.mapping.map_to_sequence(
                dependencies, self.vocab, self.spec.vocabulary.seed
            )
            domain_id = [domain.id] * domain.num_sequence

            all_dependencies.extend([d.tolist() for d in dependencies])
            all_sequences.extend(sequences)
            all_domain_id.extend(domain_id)
            all_metadata.extend(metadata)

        self.dataset["dependency"] = all_dependencies
        self.dataset["sequence"] = all_sequences
        self.dataset["domain_id"] = all_domain_id
        self.dataset["metadata"] = all_metadata
        self.made_dataset = True
        return Dataset(self.spec, self.dataset)

    def save_dataset(self, path: str = "./", name=""):
        if not self.made_dataset:
            raise ValueError("dataset not made yet")
        Dataset(self.spec, self.dataset).save(path, name)

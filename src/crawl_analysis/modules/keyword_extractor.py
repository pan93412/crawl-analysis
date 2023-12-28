from typing import Generator
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger
from concurrent.futures import ThreadPoolExecutor

import torch


class KeywordExtractor:
    filter_pos = ["Na", "Nb", "Nc", "Nd", "Ncd", "VC", "VG"]

    def __init__(self, device: int | torch.device):
        self.ws_driver = CkipWordSegmenter(model="bert-base", device=device)
        self.pos_driver = CkipPosTagger(model="bert-base", device=device)

    def split_words_raw(self, text: list[str]) -> Generator[tuple[str, str, bool], None, None]:
        ws_list = self.ws_driver(text)
        pos_list = self.pos_driver(ws_list)

        for ws, pos in zip(ws_list, pos_list):
            for ws_, pos_ in zip(ws, pos):
                yield ws_, pos_, pos_ in self.filter_pos

    def split_words(self, text: list[str]) -> Generator[str, None, None]:
        return (ws for ws, _, included in self.split_words_raw(text) if included)

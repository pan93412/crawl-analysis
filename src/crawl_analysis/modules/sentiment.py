# Use a pipeline as a high-level helper
from typing import Literal, cast
from transformers import pipeline


class SentimentAnalysis:
    def __init__(self):
        self.pipe = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")

    def predict(self, text: str) -> tuple[Literal["positive", "negative", "neutral"], float]:
        output = cast(list[dict], self.pipe(text))
        label, score = output[0]["label"], output[0]["score"]

        return label, score

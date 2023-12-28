# Use a pipeline as a high-level helper
from typing import Literal, cast
from transformers import pipeline


class SentimentAnalysis:
    def __init__(self):
        self.pipe = pipeline("text-classification", model="IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment")

    def predict(self, text: str) -> tuple[Literal["Positive", "Negative", "Neutral"], float]:
        output = cast(list[dict], self.pipe(text))
        label, score = output[0]["label"], output[0]["score"]

        if score < 0.75:
            label = "Neutral"

        return label, score

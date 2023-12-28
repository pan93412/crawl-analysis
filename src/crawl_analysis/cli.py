from modules.sentiment import SentimentAnalysis
import argparse


def main():
    root_parser = argparse.ArgumentParser(description="Crawl Analysis")
    modules_parser = root_parser.add_subparsers(dest="modules", title="Description")

    sentiment_parser = modules_parser.add_parser("sentiment", help="Sentiment Analysis")
    sentiment_parser.add_argument("text", type=str, help="Text data to analyze")

    root_args = root_parser.parse_args()

    match root_args.modules:
        case "sentiment":
            sa = SentimentAnalysis()
            l, w = sa.predict(root_args.text)
            print(f"{round(w*100, 3)}% {l}")
        case _:
            print("Invalid command: %s" % (root_args.command))


if __name__ == "__main__":
    main()

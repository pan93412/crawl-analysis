FROM alpine
WORKDIR /app

RUN apk add bash curl
RUN printf "analysis@\nanalysis@" | adduser -s /bin/bash analysis
USER analysis

RUN (curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash) && (echo 'source "$HOME/.rye/env"' >> ~/.bashrc)

RUN rye sync
CMD rye run streamlit src/crawl_analysis/app.py

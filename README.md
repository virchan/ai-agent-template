uv venv .venv --python 3.11

Activate the named venv
source .venv/bin/activate # macOS/Linux

or
.venv\Scripts\activate


flyte create config \
    --endpoint https://demo.hosted.unionai.cloud \
    --auth-type headless\
    --builder remote \
    --domain development \
    --project flytesnacks
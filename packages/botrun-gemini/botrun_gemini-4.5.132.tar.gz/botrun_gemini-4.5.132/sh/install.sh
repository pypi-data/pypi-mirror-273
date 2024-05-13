python3 -m venv venv
source venv/bin/activate
uv pip install --upgrade twine build
uv pip install -U -r requirements.txt

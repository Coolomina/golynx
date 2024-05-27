# Setup

#### Local env

```bash
python3 -m venv .e
. .e/bin/activate
pip install '.'

# Optionally, test deps
pip install '.[test]'
```

##### Test in integration

```bash
docker compose up --build
```

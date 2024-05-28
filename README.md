# Golynx

🦊 `golynx` is a shitty Python implementation of the [go-links formula](https://meta.wikimedia.org/wiki/Go_links).

You are presented with the minimum expression of a frontend (ChatGPT wrote it). Just add some redirections there and share them with the rest of the org for 10x workers. Boom.

This project can use [oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/) to authenticate requests, so please navigate its configuration in the provided link.

You can find an example of `google` authentication provider in the [docker-compose.yml](docker-compose.yml).

## Implementation details

You're tired of relying on Chrome history to re-visit handy URLs, so you say "I'm done with this crap" and you look for a cool `go-links` implementation out there. You find something sweet, you start configuring its shit, you have the db and cache in HA for max availability, your YAMLs are all interpolated with different configs for different envs.

Before you know it you're asking yourself who you are and what you've done with your life. Why the fuck would you take yourself through all of that for deploying a shit application?, we need to talk.

This `go-links` implementation aims to make things **absolutely dumb**. That's why:

- It has an in-memory database. Forget about feeling like a 10x engineer because you misconfigured your autoscaling. This fucker won't scale out.
- It flushes it to disk every now and then. Fuck you, you're paying for a disk, you better use it.
- The frontend uses no frameworks. It fucking loads in 4ms.

## Installation

```bash
git clone https://github.com/Coolomina/golynx.git
docker build -t golynx .
docker run --rm -d -v $PWD/data:/app/data -p 8000:8000 golynx
```

## Environment variables

There are [some defaults](./golynx/config.py), but you can override them.

| Key | Description |
| --- | --- |
| BYPASS_OAUTH_PROXY | Whether you want to use it with `oauth2-proxy` or not |
| STORAGE_FLUSH_DIR | Absolute/relative path for the app to flush the DB to |
| STORAGE_FLUSH_FILE | Name of the file the app will flush the DB to. It combines with `STORAGE_FLUSH_DIR` |
| STORAGE_FLUSH_PERIOD_SECONDS | Time in seconds the DB will flush to the storage |
| DEFAULT_USER | When bypassing oauth2-proxy, this will be the user that creates the golynx |
| LOG_LEVEL | You know what this is |
| DEV_MODE | For devs only, it won't register some middlewares for practicity |

## How do I fucking roll this out to the rest of my org?

1. Deploy it wherever the fuck you want
2. Be sure the IP is reachable, you moron.
3. Use it. But... how?

I'm not gonna make you download an obnoxious browser extension, are we crazy?

You know your org better than I do, but here are some tips:

- Just use Chrome [custom search engines](https://zapier.com/blog/add-search-engine-to-chrome/) and use it like:
    - Search engine: golynx
    - Shortcut: go
    - URL with %s in place of query: https://your-golynx-deployment/go/%s

- If you live in 2001 and don't use Chrome, you can always do the filthiest of the tricks and hack your `/etc/hosts` to resolve to your golynx deployment.

- If you want to make things even more complicated, God bless you. Some say just add a DNS record to your internal DNS. Why would you fucking maintain that, but if it works for you... /shrug.

## Setup

#### Local env

```bash
python3 -m venv .e
. .e/bin/activate
pip install '.'

# Optionally, test deps
pip install '.[test]'
```

#### Test in integration with Google auth provider

```bash
export OAUTH2_PROXY_COOKIE_SECRET=xxxxxxx
export OAUTH2_PROXY_CLIENT_ID=yyyyyyy
export OAUTH2_PROXY_CLIENT_SECRET=zzzzzz
export OAUTH2_PROXY_EMAIL_DOMAINS=myballs.bat

docker compose up --build
```

#### Tests

```bash
pytest
```

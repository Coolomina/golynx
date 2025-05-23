# Golynx

🦊 `golynx` is a Python implementation of the [go-links formula](https://meta.wikimedia.org/wiki/Go_links).

You are presented with the minimum expression of a frontend (ChatGPT wrote it). Just add some redirections there and share them with the rest of the org for 10x workers. Boom.

This project can use [oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/) to authenticate requests, so please navigate its configuration in the provided link.

You can find an example of `google` authentication provider in the [docker-compose.yml](docker-compose.yml).

## Poor demo

![Cool huh](./img/golynx.gif)

## Implementation details

You're tired of relying on Chrome history to re-visit handy URLs, so you say "I'm done with this crap" and you look for a cool `go-links` implementation out there. You find something sweet, you start configuring its stuff, you have the db and cache in HA for max availability, your YAMLs are all interpolated with different configs for different envs.

Before you know it you're asking yourself who you are and what you've done with your life. Why the heck would you take yourself through all of that for deploying a tiny application?, we need to talk.

This `go-links` implementation aims to make things **absolutely dumb**. That's why:

- It has an in-memory database. Forget about feeling like a 10x engineer because you misconfigured your autoscaling. This thing won't scale out.
- It flushes it to disk every now and then. You're paying for a disk, you better use it.
- The frontend uses no frameworks. It loads in 4ms.

> How do I backup my shit?

https://linux.die.net/man/1/inotifywait

## Installation

##### Container

```bash
git clone https://github.com/Coolomina/golynx.git
docker build -t golynx .
docker run --rm -d -v $PWD/data:/app/data -p 8000:8000 golynx
```

##### Bare metal

Just do what the [Dockerfile](./Dockerfile) does but in your VM :D. I honestly haven't tried this.


## Environment variables

There are [some defaults](./golynx/config.py), but you can override them.

| Key | Description | Appliable when | Default |
| --- | --- | --- | --- |
| BYPASS_OAUTH_PROXY | Whether you want to use it with `oauth2-proxy` or not | - | `False` |
| STORAGE_FLUSH_DIR | Absolute/relative path for the app to flush the DB to | - | `./data` |
| STORAGE_FLUSH_FILE | Name of the file the app will flush the DB to. It combines with `STORAGE_FLUSH_DIR` | - | `golynx.db` |
| STORAGE_FLUSH_PERIOD_SECONDS | Time in seconds the DB will flush to the storage | - | `10` |
| DEFAULT_USER | When bypassing oauth2-proxy, this will be the user that creates the golynx | - | `default@default` |
| DEFAULT_REDIRECTION | Default redirection when not matching any golynx | - | `https://www.chiquitoipsum.com/` |
| LOG_LEVEL | You know what this is | - | `INFO` |
| DATABASE | Type of database to use | - | `in_memory` |
| SUPABASE_URL | URL of the Supabase instance | When using `supabase` database | `https://lol.supabase.co` |
| SUPABASE_KEY | Key of the Supabase instance | When using `supabase` database | `lol` |
| STORAGE_TYPE | Type of storage to use | - | `disk` |
| STORAGE_S3_BUCKET | Bucket to use for S3 storage | When using `s3` storage | `golynx` |
| STORAGE_S3_AWS_ACCESS_KEY_ID | AWS access key ID for S3 storage | When using `s3` storage | `lol` |
| STORAGE_S3_AWS_SECRET_ACCESS_KEY | AWS secret access key for S3 storage | When using `s3` storage | `lol` |

## How do I roll this out to the rest of my org?

1. Deploy it wherever you want
2. Be sure the IP is reachable.
3. Use it. But... how?

I'm not gonna make you download an obnoxious browser extension, are we crazy?

You know your org better than I do, but here are some tips:

- Just use Chrome [custom search engines](https://zapier.com/blog/add-search-engine-to-chrome/) and use it like:
    - Search engine: golynx
    - Shortcut: go
    - URL with %s in place of query: https://your-golynx-deployment/go/%s

- You can always do the filthiest of the tricks and hack your `/etc/hosts` to resolve to your golynx deployment.

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

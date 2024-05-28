# Golynx

🦊 `golynx` is a shitty Python implementation of the go-links formula.

You are presented with the minimum expression of a frontend (ChatGPT wrote it). Just add some redirections there and share them with the rest of the org for 10x workers. Boom.

This project uses [oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/) to authenticate requests, so please navigate its configuration in the provided link.

You can find an example of `google` authentication provider in the [docker-compose.yml](docker-compose.yml).

## How do I fucking roll this out to the rest of my org?

I'm not gonna make you download an obnoxious browser extension, are we crazy?

You know your org better than I do, but here are some tips:

- Just use Chrome [custom search engines](https://zapier.com/blog/add-search-engine-to-chrome/) and use it like:
    - Search engine: golynx
    - Shortcut: go
    - URL with %s in place of query: https://your-golynx-deployment/go/%s

- If you live in 2001 and don't use Chrome, you can always do the filthiest of the tricks and hack your `/etc/hosts` to resolve to your golynx deployment.

- If you want to make things even more complicated, God bless you. Some say just add a DNS record to your internal DNS. Why would you fucking maintain that, but if it works for you... /shrug.

## Implementation details

You're tired of relying on Chrome history to re-visit handy URLs, so you say "I'm done with this crap" and you look for a cool `go-links` implementation out there. You find something sweet, you start configuring its shit, you have the db and cache in HA for max availability, your YAMLs are all interpolated with different configs for different envs.

Before you know it you're asking yourself who you are and what you've done with your life. Why the fuck would you take yourself through all of that for deploying a shit application?

This `go-links` implementation aims to make things **absolutely dumb**. That's why:

- It has an in-memory database. Forget about feeling like a 10x engineer because you misconfigured your autoscaling. This fucker won't scale out.
- It flushes it to disk every now and then. Fuck you, you're paying for a disk, you better use it.
- The frontend uses no frameworks. It fucking loads in 4ms.

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

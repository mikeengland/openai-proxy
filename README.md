# OpenAI Proxy backend

A demo backend app to test proxying streaming (via server side events) and non-streaming requests to OpenAI.

This can be run via:

```commandline
docker build -t openai_proxy:latest .
docker run -p 8000:8000 -e OPENAI_API_KEY=xyz  openai_proxy:latest
```

This can be used via a [Chainlit UI](https://github.com/mikeengland/openai-proxy-chainlit)
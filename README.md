# Cyberlab — Web Security & Resilience Lab

## Overview
A local web security learning project focused on HTTP request
handling, basic rate limiting, input validation, and HTML output
escaping.

## Objectives
- Measure baseline HTTP response behavior.
- Compare HTTPServer and ThreadingHTTPServer.
- Implement a simple per-client rate limiter.
- Test input length validation and HTML escaping.
- Document results and testing limitations.

## Environment
- Python 3
- Python standard library
- Local target: 127.0.0.1:8081

## Security Controls
- ThreadingHTTPServer for concurrent request handling.
- Rate limit: 30 requests per 10-second window per client IP.
- Input length limit: 100 characters.
- HTML escaping for reflected search input.
- HTTP 429 responses when the rate limit is exceeded.

## Test Results

| Test | Result |
|---|---|
| Baseline, 10 sequential requests | All requests succeeded |
| Before threading change, 20 requests | 20/20 HTTP 200 |
| After threading change, 20 requests | 20/20 HTTP 200 |
| Rate limit, 35 sequential requests | 30 HTTP 200, 5 HTTP 429 |
| Normal input | HTTP 200 |
| Input of 101 characters | HTTP 400 |
| HTML script payload | Escaped in the response |

The 20-request test took 0.141 seconds before the threading change
and 0.083 seconds afterward. These are single small test runs, not
a controlled benchmark proving that threading caused the improvement.

## Run Locally
```bash
python -m venv .venv
source .venv/bin/activate
python app.py
```

Open another terminal and test:
```bash
curl -i 'http://127.0.0.1:8081/?q=hello'
```

## Limitations
- Testing was performed only against localhost.
- Small test samples do not demonstrate DoS/DDoS resistance.
- The in-memory rate limiter is a learning implementation, not
  production-ready protection.
- Multi-client behavior, resource exhaustion, and broader security
  cases have not been comprehensively tested.
- HTML escaping was checked with a limited test payload.

## Scope
This project is an educational lab. It is not a production web server
or a certification of security.

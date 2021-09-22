#!/bin/bash
hypercorn --quic-bind 0.0.0.0:4433 --certfile cert.pem --keyfile key.pem --bind 0.0.0.0:8080 src.main:app

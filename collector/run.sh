#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
/usr/bin/env python -u collector.py

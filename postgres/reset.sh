#!/bin/bash
cd "$(dirname "$0")"
sudo -u postgres psql -f setup.sql

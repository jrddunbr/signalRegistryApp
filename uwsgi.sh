#!/bin/bash
uwsgi --socket 127.0.0.1:13030 --wsgi-file main.py --callable app --master --processes 1 --stats 127.0.0.1:13031


#!/bin/bash
source /home/atepaevm/lab_klychev/venv/bin/activate
nohup python /home/atepaevm/lab_klychev/manage.py runserver 0.0.0.0:8000 &

#!/bin/bash  
pipenv run alembic init migrations
if [ $? -eq 0 ]; then
    cp env.py migrations
fi
if [ $? -eq 0 ]; then
    pipenv run alembic revision --autogenerate -m "Initial migration"
fi
if [ $? -eq 0 ]; then
    pipenv run alembic upgrade head
fi

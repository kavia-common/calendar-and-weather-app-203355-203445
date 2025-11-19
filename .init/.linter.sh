#!/bin/bash
cd /home/kavia/workspace/code-generation/calendar-and-weather-app-203355-203445/CalendarServiceContainer
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi


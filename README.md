# Personal AI Assistant

A lightweight **general personal AI assistant** you can run locally from the terminal.

## Features
- Task management: add, list, and complete tasks
- Notes: add, list, and search notes by keyword
- Daily briefing: date + pending task summary
- Natural-ish command handling for common requests
- Local persistence in `assistant_data.json`

## Quick start
```bash
python assistant.py
```

## Example commands
- `add task Book dentist appointment`
- `list tasks`
- `complete task 1`
- `add note Remember to renew passport in June`
- `search notes passport`
- `briefing`
- `help`

## Testing
```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Notes
This version is offline-first and rule-based. You can later extend it with:
- calendar API integrations
- reminders/notifications
- LLM-backed reasoning and planning
- web and email tools

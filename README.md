This is the backend for codecrafters user events slack bot.

## Initialization
- `python3 db_init.py`

## Run
- `python3 -m app.main`

## Lint & format

- To autoformat code, use `yapf -i -vv -r .`
- Run the command before any git commit

## Test

- Test db: `python3 db_test_init.py`
- Run `pytest`
- Coverage: `pytest --cov`
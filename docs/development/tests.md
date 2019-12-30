## Run tests

All checks should be run from the _project root_.

## Automated checks

This repo is configured to run checks to help maintain code quality. The **linting** checks are for style and the **tests** ensure the code does what is expected.

See the `setup.cfg` file for broad lint settings.

#### On Github

These checks are automatically on a push to Github. This is configured with a Github [actions file](https://github.com/MichaelCurrin/twitterverse/blob/master/.github/workflows/pythonapp.yml). View the Actions tab on the Github repo for log results.

There are restrictions on the repo to ensure that a PR can only be merged if all checks pass.

#### Locally

Run the checks locally.

See available commands in the `Makefile`.

```bash
$ make help
```

Run lint checks.

```bash
$ make lint
```

Run unit and integration tests.

```bash
$ make test
```

## Manual tests

These tests should only be run locally. As some need valid credentials to do API calls, some need a DB to be setup and some are just useful for inspecting output.

These do not need to be run frequently are are useful when making changes to Twitter or ORM logic and several integrations need to tested.

### Important tests

_Note: These run against the **main** DB and not test DB._

```bash
$ make test-local
```

### Other tests

There are other manual tests which can be run individually.

```bash
$ ls -l tests/manual
```

Run one of the scripts listed. For example:

```bash
$ tests/manual/test_characters.py
```

## Development

All checks should be run from the _project root_, not the `app` directory.

```bash
$ cd <PATH_TO_REPO>
```

## Automated checks

This repo is configured to run checks to help maintain code quality. The **linting** checks are for style and the **tests** ensure the code does what is expected.

See the `setup.cfg` file for broad lint settings.

#### On Github

These checks are automatically on a push to Github. This is configured using `.github/worksflows` directory in the repo. View the Actions tab on Github for log results.

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

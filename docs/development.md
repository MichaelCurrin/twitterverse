## Development

All checks should be run from the _project root_, not the `app` directory.

```bash
$ cd <PATH_TO_REPO>
```

## Checks

This repo is configured to run checks to help maintain code quality. The **linting** checks are for style and the **tests** ensure the code does what is expected.

See the `setup.cfg` file for broad lint settings.

#### Github checks

These checks are automatically on a push to Github. This is configured using `.github/worksflows` directory in the repo. View the Actions tab on Github for log results.

There are restrictions on the repo to ensure that a PR can only be merged if all checks pass.

#### Local check

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

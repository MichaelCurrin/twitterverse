## Docs site
> How to serve the Docs site

This project has documentation in the _docs_ directory which can be served through _Docsify_.

To serve as a Github Pages site, update the Github Pages settings section of the Github repo's settings.

To serve locally:

1. Optionally install [Docsify CLI](https://docsifyjs.github.io/docsify-cli/#/) globally.
    ```bash
    $ npm i -g docsify-cli
    ```
2. Run this command from the project root.
    ```bash
    $ make docs
    ```
3. View in the browser - [localhost:3000](http://localhost:3000).

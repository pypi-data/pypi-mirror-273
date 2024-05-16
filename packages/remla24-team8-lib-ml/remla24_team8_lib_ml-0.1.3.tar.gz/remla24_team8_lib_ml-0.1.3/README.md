# lib-ml

Contains the pre-processing logic for data that is used for training or queries.

• Factor out the pre-processing logic from the training pipeline.

• Fetch relevant dependencies through a package manager, e.g., by creating a separate requirements.txt. (DONE)

• The library is versioned automatically, e.g., by picking-up on the corresponding Git version tag. (DONE)

• A workflow is used to automatically release the library in a package registry that matches the language. (As stated before, this includes either supported package registries on GitHub or repository tags in languages that support it.) (DONE)

## Usage

Install with

```
pip install remla24-team8-lib-ml

```

Use as

```
from lib_ml import DataProcessor 

data_processor = DataProcessor()

```

## Publish a release

To publish a new release, simply create a new release in GitHub with the appropriate tag name. Be sure that this tag name matches the version in the `pyproject.toml`. GitHub Actions will then automatically release and publish this. If the release failed, then remove the tag while in the Git repo using `git push origin --delete <tag name>`, after which you can then re-release the (now draft) release on GitHub.

When using Poetry, you can also depend on the latest commit using the following dependency:

```
remla24-team8-lib-ml = { git = "https://github.com/remla24-team8/lib-ml.git", branch = "main" }
```

### PyPi organization

For now it is owned by tmtenbrink on PyPI, but hopefully we get an organization so we can put it there.
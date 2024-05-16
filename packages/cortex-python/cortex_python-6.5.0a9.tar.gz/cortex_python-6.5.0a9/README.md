# Python Module for the Cortex Cognitive Platform

The Cortex Python module provides an API client library to easily integrate with the Cortex Cognitive Platform. 
Refer to the Cortex documentation for details on how to use the library: 

- Developer guide: https://cognitivescale.github.io/cortex-fabric/
- Cortex Python references: https://cognitivescale.github.io/cortex-python/master/

## Installation
There are several installation options available: 

* base library - for interacting with a Sensa cluster or developing skills 

```bash
poetry add cortex-python
```

* model development - for feature and model developing within jupyter notebooks 
```bash
poetry add cortex-python[model_development]
```

* model development extras - for developing model training and inference skills
```bash
poetry add cortex-python[model_runtime]
```

* Certifai Evaluator plugin - this must be installed with on of the model* extras
    **NOTE:** extra config needed to access the Sensa python repository
```bash
poetry config http-basic.sensa <USER> <TOKEN> 
poetry add cortex-python[model_development,certifai]
```

#### Install from source
```bash
git clone git@github.com:CognitiveScale/cortex-python.git
cd cortex-python
# Needed for certifai components
poetry config http-basic.sensa <USER> <TOKEN> 
poetry install
```

## Development 

### Setup

When developing, it's a best practice to work in a virtual environment. Create and activate a virtual environment:

```bash
poetry install
poetry shell
```

Install developer dependencies:

```bash
git clone git@github.com:CognitiveScale/cortex-python.git
cd cortex-python
make dev.install
```

Run Developer test and linting tasks:
Three types of checks are configured for this:
1. [symilar](https://pylint.readthedocs.io/en/v2.16.2/symilar.html) - to test code duplication
2. [pylint](https://pylint.readthedocs.io/en/v2.16.2/) - for linting
3. [pytest](https://docs.pytest.org/en/7.2.x/) - for running the unit tests. These are orchestrated through [tox](https://tox.wiki/en/3.27.1/). The tox configuration is available at [`tox.ini`](/tox.ini)

There's a convenience `Makefile` that has commands to common tasks, such as build, test, etc. Use it!

### Testing

#### Unit Tests

Follow above setup instructions (making sure to be in the virtual environment and having the necessary dependencies)

- `make test` to run test suite

To run an individual file or class method, use pytest. Example tests shown below:

- file: `pytest test/unit/agent_test.py` 
- class method: `pytest test/unit/agent_test.py::TestAgent::test_get_agent`

### Pre-release to staging
**Note:** this repository using git tag for versionning

1. Create and push an alpha release:

```bash
git tag -a 6.5.0a<N> -m 'alpha tag'
git push --tags
make dev.push
```
    This will build an alpha-tagged package.
2. Merge `develop` to `staging` branch:

```bash
make stage
```

3. In GitHub, create a pull request from `staging` to `master`.
```
git tag -a 6.5.0 -m 'rlease tag'
git push --tags
```

### Contributing 

After contributing to the library, and before you submit changes as a PR, please do the following

1. Run unit tests via `make test`
2. Manually verification (i.e. try the new changes out in Cortex) to make sure everything is going well. Not required, but highly encouraged.
3. Bump up `setup.py` version and update the `CHANGELOG.md` 

### Documentation

Activate your virtual environment:

```bash
poetry shell
```

Set up your environment, if you have not done so:

```bash
make dev.install 
```

The package documentation is built with Sphinx and generates versioned documentation for all tag matching the `release/X.Y.Z` pattern and for the `master` branch. To build the documentation:

```bash
make docs.multi
```
The documentation will be rendered in HTML format under the `docs/_build/${VERSION}` directory.

## Configuring the client

There are four mechanisms for configuring a client connection. 

1) Use `$HOME/.cortex/config` file setup via `cortex configure`.
    ```python
   from cortex.client import Cortex
   client=Cortex.client(verify_ssl_cert=True|False)
   ```
   
2) Use environment variables CORTEX_URL, CORTEX_TOKEN, and CORTEX_PROJECT
    ```python
   from cortex.client import Cortex
   client=Cortex.client(verify_ssl_cert=True|False)
   ```
    
This is a table of supported environment variables.

These ENV vars are injected by the Sensa RUNTIME for use during skill startup.

| Environment variables         | Description                                                             |
|-------------------------------|-------------------------------------------------------------------------|
| CORTEX_PERSONAL_ACCESS_CONFIG | JSON string containing a Pesonal Access Token obtained from the console UI |
| CORTEX_CONFIG_DIR             | A folder containing the `config` created by the `cortex configure` command |
| CORTEX_TOKEN                  | A JWT token generate by `cortex configure token` or provided during skill invokes |
| CORTEX_PROJECT                | Project used during api requests                                        |
| CORTEX_URL                    | URL for Sensa apis                                                      |

3) Use method kwargs with `Cortex.client()` 
    ```python
   from cortex.client import Cortex
   client=Cortex.client(api_endpoint="<URL>", token="<token>", project="<project>", verify_ssl_cert=True|False)
   ```
   
4) Using the skills invoke message, this allows for authentication using the caller's identity.
    ```python
   from cortex.client import Cortex
   client=Cortex.from_message({})    
   ```
# ou-tm351-jl-extensions

Install from pypi as `ou-tm351-jl-extensions`

- JupyterLab 3: v0.1.2
- JupyterLab 4: v 0.2.0

Recommended JupyterLab extensions for use in the OU TM351 module.

This package will install several JupyterLab extensions that brand and extend a JupyterLab environment to support its use as a teaching and learning environment.

Extensions installed:

```text
jupyterlab = ">=4.1"

# Branding and OU extensions
jupyterlab-ou-brand-extension = "^0.2.0" # OU brand extension (favicon, logo)

# Notebook cell tools
jupyterlab-cell-status-extension = "^0.2.2" # cell execution status; accessibility tools
jupyterlab-empinken-extension = "^0.5.2" # cell background styling
jupyterlab-skip-traceback = "^5.1.0" # skip trackeback / error reporting
jupyterlab-myst = "^2.4.0" ## MyST parser and styling (markdown cells)
jupyterlab-spellchecker = "^0.8.4" ## Spellchecker

# Code support
#jupyterlab-lsp = "^5.1.0" # language server protocol
jupyterlab-code-formatter = "^2.2.1" # Code formatter
black = "^24.4.2" # code formatting
isort = "^5.13.2" # code formatting

# Language packs
jupyterlab-language-pack-fr-fr = "^4.1.post2" # French
jupyterlab-language-pack-zh-cn = "^4.1.post2" # Chinese

# File browsing and handling
jupyterlab-unfold = "^0.3.0" # tree view in files sidebar
jupyter-archive = "^3.4.0" # archive file download
jupyterlab-filesystem-access = "^0.6.0" # local filesystem access
jupyterlab-git = "^0.50.0" # Git/Github tools
jupytext = "^1.16.0" # text notebook formats

# Renderers
jupyterlab-geojson = "^3.3.1" # geojson renderer
jupyter-compare-view = "^0.2.4" # compare images

# Resource monitoring
#jupyter-resource-usage = "^1.0.2" # memory/CPU
jupyterlab_execute_time = "^3.1.2" # cell execution time
```

See the [docs]().

Check the installation by running:

```python
import ou_tm351_jl_extensions as ou
ou.check_install()
```

__Maintenance__

Update packages in `pyproject.toml` by running: `poetry update`

__Formal tests for use in CI will be added soon.__

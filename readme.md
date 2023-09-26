# head_switcher: Flask Single Page App Frontend Packaging Tool

This package simplifies the process of packaging and loading frontend assets for your headless flask app.
In another word, this package install and switch **head** for your
**[headless](https://en.wikipedia.org/wiki/Headless_software)** flask apps.

## Usage

You need to package your single page app (SPA) frontend assets into a `.frontend` file using our cli tool, and then you
can ship the `.frontend` file with your python packages or simply load it from the file system.

### Package frontend

Assuming you are using create-react-app(CRA), and are using the default build configurations.

```shell
npm run build
# This will create a `build/` folder for the product build.
build-frontend-pack build/ -o path-to-frontend.frontend
```

### How to ship frontend assets with your python project

The following guide assumes that you are using a similar setup with this
[tutorial: Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

And we assume your package is called `example_package`.

After using the cli tool to package your frontend assets,
i.e. `build-frontend-pack build/ -o spa_ui.frontend`, you can save the `spa_ui.frontend` file to the
following location `src/example_package/assets/ui.frontend`, and create an empty
file `src/example_package/assets/__init__.py`.

In your `pyproject.toml` file, under `tool.hatch.build` section, make sure the artifacts field contains the
entry `"*.frontend"`

```toml
[tool.hatch.build]
artifacts = [
    "*.frontend"
]
```

Now in your application, you can load the front assets
using `load_from_package_resources('example_package.assets', 'ui.frontend')`.

```python
from head_switcher import install_to_flask, load_from_package_resources

from flask import Flask

assets = load_from_package_resources('example_package.assets', 'ui.frontend')

app = Flask(__name__)
install_to_flask(assets, app)
```

### Install frontend from a file

If you choose to load frontend from a file, you can do it like this.

```python
from head_switcher import install_to_flask, load_from_file_path

from flask import Flask

assets = load_from_file_path('path-to-frontend.frontend')

app = Flask(__name__)
install_to_flask(assets, app)
```

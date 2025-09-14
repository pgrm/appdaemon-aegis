# AppDaemon Aegis

**Strong and reliable automations for AppDaemon.** ![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/pgrm/appdaemon-aegis?utm_source=oss&utm_medium=github&utm_campaign=pgrm%2Fappdaemon-aegis&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)

AppDaemon Aegis is a Python framework that supercharges AppDaemon, providing strong typing, powerful testing utilities, and higher-level abstractions to make your smart home automation journey more enjoyable and productive.

## Why Aegis?

AppDaemon is a fantastic tool for writing automations in Python, but it can be challenging to work with, especially for larger and more complex setups. Aegis aims to solve these common pain points:

- **Lack of Typing:** AppDaemon's dynamic nature can lead to runtime errors that are hard to debug. Aegis introduces strong typing to catch errors early.
- **Difficult Testing:** Testing automations can be a real chore. Aegis provides a suite of testing helpers, including support for property-based testing, to make your automations more robust.
- **Boilerplate Code:** Writing AppDaemon apps often involves a lot of repetitive boilerplate code. Aegis provides higher-level abstractions to reduce this boilerplate and let you focus on the automation logic.

## Features ✨

- **Strongly Typed:** Catch bugs before they happen with full type hinting for the AppDaemon API.
- **Testable:** Write unit and integration tests for your automations with ease, with built-in support for `pytest` and `hypothesis`.
- **Modern Python:** Write your automations using modern Python features like `async`/`await`.
- **Extensible:** Aegis is designed to be extensible, so you can easily add your own helpers and abstractions.
- **Focus on Automation:** Spend less time on boilerplate and more time creating the smart home of your dreams.

## Getting Started

Getting started with Aegis is easy.

### Installation

First, install Aegis using pip:

```bash
pip install appdaemon-aegis
```

### Writing Your First App

To create a new app, simply inherit from `appdaemon-aegis.AegisApp` instead of `hass.Hass`:

```python
# my_app.py
from appdaemon-aegis import AegisApp

class MyFirstApp(AegisApp):
    async def initialize(self):
        self.log("Hello from Aegis!")

        # Your automation logic here...
```

### Installation and Configuration

To use your Aegis apps with AppDaemon, you need to install Aegis and configure AppDaemon to find it. There are two main ways to do this:

**1. Using a Virtual Environment (Recommended)**

The recommended way to use Aegis is to let AppDaemon manage a virtual environment for your apps. This keeps your dependencies isolated.

First, create a `requirements.txt` file in your AppDaemon `apps` directory and add `appdaemon-aegis` to it:

```
appdaemon-aegis
# any other dependencies you need
```

Then, in your `appdaemon.yaml` file, point to this file:

```yaml
appdaemon:
  ...
  app_dir: /path/to/your/apps
  python_packages:
    - -r
    - requirements.txt
```

**2. Manual Installation**

If you prefer not to use a virtual environment, you can install Aegis manually in the same Python environment that AppDaemon is running in:

```bash
pip install appdaemon-aegis
```

### Running your App

Once Aegis is installed and available to AppDaemon, you can configure your apps in `apps.yaml` as you normally would:

```yaml
# apps.yaml
my_first_app:
  module: my_app
  class: MyFirstApp
```

That's it! You're now ready to start crafting your smart home automations with AppDaemon Aegis.

## Development

To set up a local development environment, you'll need [Poetry](https://python-poetry.org/docs/#installation) installed.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/pgrm/appdaemon-aegis.git
    cd appdaemon-aegis
    ```

2.  **Set up the environment:**
    This command will install all dependencies and set up `lefthook` git hooks.

    ```bash
    make setup
    ```

### Development commands

This project uses a `Makefile` to streamline common development tasks. Here are the available commands:

- `make setup`: Set up the development environment.
- `make format`: Format the code using `ruff`.
- `make lint`: Run linter checks using `ruff` and auto-fix issues.
- `make test`: Run the test suite using `pytest`.
- `make ci`: Run all CI checks (formatting, linting, and testing).

## Contributing

Contributions are welcome! If you have an idea for a new feature or have found a bug, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

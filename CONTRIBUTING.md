# Contributing to TaskingAI

We welcome contributions from the community and are pleased to have you join us. This document will help you get started.

## Developing Locally with Poetry

[Poetry](https://python-poetry.org/) is a dependency management and packaging tool in Python that makes it easy to manage virtual environments. It's particularly useful when you need to test changes to the TaskingAI client in a local development setup.

Whether you're looking to fix a bug, add a new feature, or just improve the TaskingAI client, you'll want to be able to:

1. Test your changes in isolation from your system Python installation.
2. See your changes reflected immediately in any local code that imports the TaskingAI client.
3. Keep track of your changes in git to enable collaboration and code review through GitHub pull requests.

### Step 1: Fork and Clone the Repository

First, create a fork of the TaskingAI client repository on GitHub, and then clone your fork locally:

```bash
git clone https://github.com/<your-username>/taskingai-python-client.git
cd taskingai-python-client
```

### Step 2: Install Poetry

You can install Poetry by following the instructions on [the official website](https://python-poetry.org/docs/).

### Step 3: Install Dependencies

Once Poetry is installed, you can install all the required dependencies by running:

```bash
poetry install
```

### Step 4: Activate the Virtual Environment

Enter the virtual environment shell created by Poetry:

```bash
poetry shell
```

Verify the setup:

```bash
poetry env info
```

### Step 5: Make Changes and Test

Now you can start making changes to the TaskingAI client. To test your changes, you may want to:

- Write unit tests.
- Run the TaskingAI client in your local applications or Jupyter Notebooks.

### Step 6: Push Changes and Create a Pull Request

After making your changes, push them to your fork and [create a pull request](https://github.com/taskingai/taskingai-python-client/compare) on the original TaskingAI repository.

## Load Your Virtualenv in Another Shell

To use your development version of the TaskingAI client in another application or Jupyter Notebook:

### Get the Path to Your Virtualenv

Run:

```bash
poetry env info --path
```

### Activate Your Virtualenv

Source the `activate` script in your virtualenv:

```bash
source <your-virtualenv-path>/bin/activate
```

### Test Your Virtualenv

Create a test file in your TaskingAI client code directory and another in your second shell to verify that changes to the client are reflected immediately.

## Need Help?

If you have any questions or run into issues, please [file an issue](https://github.com/taskingai/taskingai-python-client/issues/new) on GitHub.

Thank you for contributing to TaskingAI!

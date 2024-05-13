<picture align="center">
  <img alt="Pandas Logo" src="doc/_static/logo-pybandit.png">
</picture>

-----------------
[![PyPI Downloads](https://img.shields.io/pypi/dm/pybandit.svg?label=PyPI%20downloads)](
https://pypi.org/project/pybandit/)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/pybandit.svg?label=Conda%20downloads)](
https://anaconda.org/conda-forge/pybandit)

# PyBandit : powerful multiarmed bandit toolkit

Welcome to PyBandit, an open-source Python library designed to make experimenting with and deploying multi-armed bandit algorithms simple and accessible. Whether you're a researcher, data scientist, or enthusiast, PyBandit offers a robust platform for exploring bandit algorithms, optimizing decision-making processes, and enhancing your applications with the power of reinforcement learning.

## Features

- **Ease of Use**: Simple, clear APIs make it easy to integrate and experiment with different bandit algorithms.
- **Extensive Documentation**: Comprehensive guides and examples to help you get started quickly.
- **Community Driven**: PyBandit is developed and supported by an enthusiastic community of contributors.
- **Flexibility**: From basic to advanced bandit algorithms, PyBandit supports a wide range of use cases.
- **Scalability**: Built to scale from small projects to large-scale deployments.

## Installation

You can install PyBandit using pip:

```bash
pip install pybandit
```

## Quick Start

```python
from pybandit import Bandit

# Create a Bandit instance with three arms
bandit = Bandit(arms=3)

# Simulate choosing an arm
reward = bandit.pull(arm=1)

print(f"Reward from chosen arm: {reward}")
```

## Contributing to PyBandit

Thank you for your interest in contributing to PyBandit! We are thrilled to have you join our community of developers and researchers dedicated to advancing the field of reinforcement learning through accessible multi-armed bandit algorithms. This document provides guidelines for contributing to PyBandit and should be followed to ensure a smooth collaboration process.
Contributions can take various forms, from bug fixes and feature additions to documentation improvements and example tutorials. Here's how you can get started:

### Reporting Issues

Before submitting an issue, please check that it has not already been reported. If you are reporting a bug, please include:

- A clear and descriptive title
- A concise description of the problem
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Your environment information (e.g., OS, Python version)

### Pull Requests

Pull requests are always welcome. Follow these steps to submit your code:

1. **Fork the repository** and clone it locally. Connect your repository to the original 'upstream' repo by adding it as a remote. Pull in changes not present in your local repository, if necessary.
2. **Create a branch** for your edits.
3. **Develop your feature** or bug fix based on the `main` branch. Keep your changes as focused as possible. If there are multiple unrelated fixes or features, consider submitting them as separate pull requests.
4. **Write a compelling commit message**. Each commit message should describe why the change was made.
5. **Run the tests** to ensure your changes do not break existing functionality. Add new tests if necessary.
6. **Push your branch** and open a pull request against the `main` branch. Provide a clear description of the problem and solution, including any relevant issue numbers.
7. **Wait for feedback** from the maintainers. They may suggest changes or improvements to your contribution.

### Development Environment

Setting up your development environment is easy:

```bash
git clone https://github.com/your_username/pybandit.git
cd pybandit
pip install -r requirements_dev.txt
```

### Writing Documentation

Good documentation is crucial for any project. Help us improve and expand our docs. Documentation changes can be proposed in the same way as code changes, through a pull request.

### Code of Conduct

Participation in the PyBandit community is governed by our Code of Conduct. Please read [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) before participating to help us maintain a safe and welcoming environment for everyone.

### Asking for Help

If you need help at any point, feel free to ask questions in our community forum or on the GitHub issue tracker. We value your contributions and will do our best to provide support.

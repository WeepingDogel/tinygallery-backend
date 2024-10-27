# Contributing to TinyGallery Backend

We welcome contributions to the TinyGallery Backend project! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct (to be defined).

## How Can I Contribute?

### Reporting Bugs

- Ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/WeepingDogel/tinygallery-backend/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/WeepingDogel/tinygallery-backend/issues/new). Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements

- Open a new issue with a clear title and detailed description of the suggested enhancement.
- Provide any relevant examples or mock-ups if applicable.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

1. Follow the "Get Started" guide in `docs/Get-Started.md` to set up your development environment.
2. Make your changes in a new git branch:
     ```shell
     git checkout -b my-fix-branch main
     ```
3. Create your patch, including appropriate test cases.
4. Run the full test suite and ensure that all tests pass.
5. Commit your changes using a descriptive commit message.

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Python Styleguide

- Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
- Use 4 spaces for indentation rather than tabs.
- Use docstrings for all public classes, methods, and functions.

### Documentation Styleguide

- Use [Markdown](https://daringfireball.net/projects/markdown/) for documentation.
- Reference function names, variable names, and filenames using backticks: \`like this\`.

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests.

* `bug` - Issues for bugs in the code
* `enhancement` - Issues for new features or improvements
* `documentation` - Issues related to documentation
* `good first issue` - Good for newcomers

## Questions?

Don't hesitate to ask questions if something is unclear. You can open an issue with the label `question` or reach out to the maintainers directly.

Thank you for contributing to TinyGallery Backend!

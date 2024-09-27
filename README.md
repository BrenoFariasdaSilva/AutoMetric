<div align="center">
  
# [AutoMetric.](https://github.com/BrenoFariasdaSilva/AutoMetric) <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

<div align="center">

---

# Welcome to the **AutoMetric** Repository!

**AutoMetric** is an enhanced tool that automates the extraction of metadata from GitHub and GitLab repositories, providing comprehensive insights into Open-Source Software (OSS) quality metrics. This project is a fork of [AutoMetric](https://github.com/HckEX/AutoMetric), incorporating substantial enhancements, including:

- Improved **AutoMetric.py** code quality.
- Execution arguments for customized functionality.
- Virtual environments for isolated package management.
- Makefiles for easy execution.
- Detailed code comments and documentation for better understanding.
- A thorough README for clear guidance on usage.
- A detailed contribuing guide.

With **AutoMetric**, you can measure vital OSS quality metrics, including the number of contributors (NC), mean time to update (MTTU), mean time to commit (MTTC), branch protection status (BP), and inactive periods (IP) for repositories.

---

</div>

<div align="center">

![GitHub Code Size in Bytes Badge](https://img.shields.io/github/languages/code-size/BrenoFariasdaSilva/AutoMetric)
![GitHub Last Commit Badge](https://img.shields.io/github/last-commit/BrenoFariasdaSilva/AutoMetric)
![GitHub License Badge](https://img.shields.io/github/license/BrenoFariasdaSilva/AutoMetric)
![Wakatime Badge](https://wakatime.com/badge/github/BrenoFariasdaSilva/AutoMetric.svg)

</div>

<div align="center">
  
![RepoBeats Statistics](https://repobeats.axiom.co/api/embed/2b842aa456af773c314a8de80273eb20d81e77dd.svg "Repobeats analytics image")

</div>

## Table of Contents
- [AutoMetric. ](#autometric-)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup](#setup)
    - [Python and Pip](#python-and-pip)
      - [Linux](#linux)
      - [MacOS](#macos)
      - [Windows](#windows)
    - [Clone the repository](#clone-the-repository)
    - [Dependencies](#dependencies)
    - [Virtual Environment](#virtual-environment)
    - [Setup of the .env File](#setup-of-the-env-file)
      - [Creating the .env File](#creating-the-env-file)
      - [Example](#example)
    - [Using the Makefile](#using-the-makefile)
  - [Run AutoMetric.py](#run-autometricpy)
    - [Using the Makefile](#using-the-makefile-1)
      - [With Execution Arguments](#with-execution-arguments)
      - [Without the Execution Arguments](#without-the-execution-arguments)
    - [Without Using the Makefile](#without-using-the-makefile)
      - [Input File Example](#input-file-example)
  - [Metadata Extraction](#metadata-extraction)
    - [Original Text Reference](#original-text-reference)
  - [Contributing](#contributing)
    - [Step 1: Set Up Your Environment](#step-1-set-up-your-environment)
    - [Step 2: Make Your Changes](#step-2-make-your-changes)
    - [Crafting Your Commit Messages](#crafting-your-commit-messages)
    - [Navigating Commits](#navigating-commits)
    - [Step 3: Submit Your Contribution](#step-3-submit-your-contribution)
    - [Step 4: Stay Engaged](#step-4-stay-engaged)
    - [Step 5: Celebrate Your Contribution](#step-5-celebrate-your-contribution)
  - [License](#license)
    - [Apache License 2.0](#apache-license-20)

## Introduction

The **AutoMetric** program is designed to assist developers and researchers in assessing the quality of open-source software projects. By automating the extraction of key metrics from GitHub and GitLab repositories, AutoMetric helps users evaluate the health and activity of repositories, ultimately contributing to better decision-making in software development.

## Setup

This section provides instructions for installing the Python Language and Pip Python package manager, as well as the project's dependencies. It also explains how to run the scripts using the provided `makefile`. The `makefile` automates the process of creating a virtual environment, installing dependencies, and running the scripts.

### Python and Pip

In order to run the scripts, you must have python3 and pip installed in your machine. If you don't have it installed, you can use the following commands to install it:

#### Linux

In order to install python3 and pip in Linux, you can use the following commands:

```
sudo apt install python3 -y
sudo apt install python3-pip -y
```

#### MacOS

In order to install python3 and pip in MacOS, you can use the following commands:

```
brew install python3
```

#### Windows

In order to install python3 and pip in Windows, you can use the following commands in case you have `choco` installed:

```
choco install python3
```

Or just download the installer from the [official website](https://www.python.org/downloads/).

Great, you now have python3 and pip installed. Now, you need to clone the repository (if you haven't done it yet) and install the dependencies.

### Clone the repository

1. Clone the repository with the following command:

	```bash
		git clone https://github.com/BrenoFariasdaSilva/AutoMetric.git
		cd AutoMetric
	```

### Dependencies

1. Install the project dependencies/requirements with the following command:

```bash
make dependencies
```

This project depends on the following libraries:

- [Git](https://git-scm.com/)  
  Git is used to clone repositories and perform operations such as switching branches. It is a critical dependency for the code execution. As the installation process varies depending on the operating system, please refer to the official Git documentation for detailed instructions on how to install it on your machine. You can typically install it using the package manager of your operating system, such as `sudo apt install git -y` in Linux, `brew install git` in macOS, and `choco install git` in Windows.

- [GitHub API for Python](https://pygithub.readthedocs.io/en/latest/)  
  This library is used to interact with GitHub repositories programmatically, allowing you to fetch repository information and manipulate data efficiently.

- [GitLab API for Python](https://python-gitlab.readthedocs.io/en/stable/)  
  Similar to the GitHub library, this dependency allows interaction with GitLab repositories, providing functionalities to manage repositories and their metadata.

- [Colorama](https://pypi.org/project/colorama/)  
  Colorama is used for coloring the terminal output, enhancing the visual appeal and readability of log messages.

- [Python Dotenv](https://pypi.org/project/python-dotenv/)  
  This library loads environment variables from a `.env` file, making it easier to manage configuration settings.

- [JSON](https://docs.python.org/3/library/json.html)  
  The built-in JSON module is utilized to parse and manipulate JSON data, facilitating communication with APIs.

- [TQDM](https://tqdm.github.io/)  
  TQDM is employed to display progress bars for long-running operations, enhancing the user experience.

- [Datetime](https://docs.python.org/3/library/datetime.html)  
  This built-in module provides classes for manipulating dates and times, crucial for timestamping commits and logs.

- [Argparse](https://docs.python.org/3/library/argparse.html)  
  Argparse is used for parsing command-line arguments, enabling flexible input configurations for the scripts.

- [OS](https://docs.python.org/3/library/os.html)  
  The OS module provides functions for interacting with the operating system, such as running terminal commands.

- [Platform](https://docs.python.org/3/library/platform.html)  
  This module is used to determine the underlying platform on which the code is running, allowing for platform-specific operations.

- [Sys](https://docs.python.org/3/library/sys.html)  
  The Sys module provides access to some variables used or maintained by the interpreter and to functions that interact with the interpreter.

### Virtual Environment

Furthermore, this project requires a virtual environment to ensure all dependencies are installed and managed in an isolated manner. A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, along with a number of additional packages. Using a virtual environment helps avoid conflicts between project dependencies and system-wide Python packages.

### Setup of the .env File

To run this project, you need to create a `.env` file that contains the necessary environment variables. This file will hold sensitive information such as your GitHub token, which is required for authentication when accessing GitHub APIs.

#### Creating the .env File

1. **Create the `.env` File**: In the root directory of your project, create a new file named `.env`. You can do this using any text editor or by running the following command in your terminal:

  ```bash
  touch .env
  ```

2. **Fill the .env File**: Open the `.env` file in your text editor and add the following line, replacing `YOUR_GITHUB_TOKEN` with your actual GitHub token:

  ```plaintext
  GITHUB_TOKEN=YOUR_GITHUB_TOKEN
  ```

#### Example

Your `.env` file should look like this:

```plaintext
GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

By following these steps, you will set up the `.env` file correctly, allowing your project to access the necessary environment variables.

### Using the Makefile

To set up and use a virtual environment for this project, we leverage Python's built-in `venv` module. The `makefile` included with the project automates the process of creating a virtual environment, installing the necessary dependencies, and running scripts within this environment.

Follow these steps to prepare your environment:

1. **Create and Activate the Virtual Environment:** 

   The project uses a `makefile` to streamline the creation and activation of a virtual environment named `venv`. This environment is where all required packages, such as `GitHub API for Python`, `GitLab API for Python`, `colorama`, `python-dotenv`, `json`, `tqdm`, `datetime`, `argparse`, `os`, and `platform`, will be installed. 

   This process will also be handled by the `Makefile` during the dependencies installation, so no additional commands need to be executed to create the virtual environment.

2. **Install Dependencies:** 
   
   Run the following command to set up the virtual environment and install all necessary dependencies on it:

    ```
    make dependencies
    ```

   This command performs the following actions:
  - Creates a new virtual environment by running `python3 -m venv venv`.
  - Installs the project's dependencies within the virtual environment using `pip` based on the `requirements.txt` file. The `requirements.txt` file contains a list of all required packages and their versions. This is the recommended way to manage dependencies in Python projects, as it allows for consistent and reproducible installations across different environments.

      If you need to manually activate the virtual environment, you can do so by running the following command:

      ```
      source venv/bin/activate
      ```

3. **Running Script:**
   
   The `makefile` also defines commands to run every script with the virtual environment's Python interpreter. For example, to run the `AutoMetric.py` file, use:

   ```
   make auto_metric_script
   ```

   This ensures that the script runs using the Python interpreter and packages installed in the `venv` directory.

4. **Generate the requirements.txt file:**

   If you changed the project dependencies and want to update the `requirements.txt` file, you can run the following command:

   ```
   make generate_requirements
   ```

   This command will generate the `requirements.txt` file in the root of the tool directory (`PyDriller/`), which will contain all the dependencies used in the virtual environment of the project.

5. **Cleaning Up:**

	To clean your project directory from the virtual environment and Python cache files, use the `clean` rule defined in the `makefile`:

	```
	make clean
	```

	This command removes the `venv` directory and deletes any cached Python files in the project directory, helping maintain a clean workspace.

## Run AutoMetric.py

In this project, we developed a Python script named `AutoMetric.py` designed to extract metadata from repositories hosted on GitHub and GitLab. The following results were obtained from the implementation:

1. **Input**:
   - The script reads a list of repository URLs from an input file (`input.txt`) or accepts them as command-line arguments.

### Using the Makefile

#### With Execution Arguments

To run the `AutoMetric.py` script with the Makefile, ensure you are in the project directory and have the virtual environment activated. Use the following command:

```bash
make auto_metric_script args="--repos_urls https://github.com/username/repository1 https://gitlab.com/username/repository2"
```

#### Without the Execution Arguments

```bash
make auto_metric_script
```

This command executes the script using the Python interpreter and packages installed in the venv directory, as specified in the Makefile. Ensure that the input.txt file is present in the project directory.

### Without Using the Makefile

Before running the `AutoMetric.py` script, you need to activate the virtual environment where the necessary dependencies are installed. This ensures that all required libraries are available for the script. To do this, you can use the `source` command to activate the virtual environment:

```bash
source venv/bin/activate
```

Once the virtual environment is activated, you can directly run the AutoMetric.py script using the Python interpreter:

```bash
python3 ./AutoMetric.py --repos_urls "https://github.com/username/repository1" "https://gitlab.com/username/repository2"
```

In this case, replace `username` and `repository` with the actual GitHub or GitLab usernames and repository names. This command allows you to provide repository URLs directly as command-line arguments.

Remember to always activate the virtual environment before running the script to ensure that all dependencies are properly loaded.

#### Input File Example

If you choose to use an input file (`input.txt`), ensure that it is formatted with one repository URL per line, such as:

```
https://github.com/username/repository1
https://gitlab.com/username/repository2
```

This will allow the script to read all listed repositories during execution

## Metadata Extraction

For each repository, the script retrieves several key metrics, including:

- **Mean Time to Update (MU)**: This metric measures the average time between releases of a repository. The value is calculated using the `created_at` timestamp from the releases API of GitHub and GitLab, averaged over the total number of releases. A lower MU indicates more frequent updates, while a higher MU may suggest infrequent updates. Repositories with high MU values typically exhibit fewer vulnerabilities.

- **Mean Time to Commit (MC)**: This metric indicates how frequently commits are made to the repository, with the frequency reflecting the level of activity. The MC is calculated by counting the total number of commits obtained from the Commits API and dividing it by the time since the first commit. Higher MC values generally correlate with fewer vulnerabilities.

- **Inactive Period (IP)**: This metric measures the duration since the last commit. A higher IP indicates a longer period of inactivity, which may not necessarily degrade the security of completed projects but suggests less ongoing development. Repositories with high IP values often show fewer vulnerabilities, contrary to the expectation that active management leads to better security.

- **Number of Contributors (NC)**: This metric quantifies the number of contributors participating in the repository. A higher NC may suggest better security, although the relationship is not always clear. 

- **Branch Protection (BP)**: This metric determines whether branch protection settings are applied in the repository. The protected status can influence the repository's security, with higher averages of vulnerabilities found in repositories without branch protection.

These metrics collectively provide insights into the quality and security of open-source software projects.

### Original Text Reference
The information for these metrics is extracted from the following paper:
T. Lee, H. Park, and H. Lee, "AutoMetric: Towards Measuring Open-Source Software Quality Metrics Automatically," 2023 IEEE/ACM International Conference on Automation of Software Test (AST), Melbourne, Australia, 2023, pp. 47-55, doi: 10.1109/AST58925.2023.00009.

3. **Output**:
	- Extracted metadata is stored in an output JSON file (`output.json`), facilitating easy access and analysis.

Overall, the `AutoMetric` program successfully automates the collection of important repository metrics, enabling users to gain insights into the state of their projects with minimal manual effort.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. If you have suggestions for improving the code, your insights will be highly welcome. Please follow these guidelines to make your contributions smooth and effective:

### Step 1: Set Up Your Environment

Before you can contribute, you need to set up your development environment. This steps are already explained in the [Setup](#setup) section.

### Step 2: Make Your Changes

Now that your environment is set up, you're ready to start making changes. It's a good idea to start with a clear goal in mind. Are you fixing a bug, adding a feature, or improving documentation?

1. **Create a Branch**: Before diving into code changes, start by creating a new branch for your updates. This strategy helps keep your modifications neatly organized and distinct from the main project line, facilitating a smoother integration and review process later on. Choose a branch name that is both descriptive and reflective of the changes you're proposing.
    ```sh
    git checkout -b feature/AmazingFeature
    ```

2. **Make Your Changes**: With your branch ready, you can now focus on implementing your proposed changes, be it additions, modifications, or fixes. Here are some key points to keep in mind during this stage:
   
   - **Test Thoroughly**: Ensure your changes work as intended and don't introduce new problems. Adequate testing is crucial for maintaining the integrity and reliability of the project.
   
   - **Commit Wisely**: Large changes can make the review process daunting. Aim to break down big updates into smaller, more manageable commits. This approach not only eases the review process but also keeps the project history clear and understandable.
   
   - **Follow Standards**: Adhere to the project's coding conventions and standards. Consistency in coding practices ensures code readability and eases maintenance for all contributors. If you want to know a great commit standards, read the convention below, which is very similar to the [Conventional Commits](http://conventionalcommits.org) specification.

### Crafting Your Commit Messages

Your commit messages play a vital role in documenting the project's development history. They should be clear, concise, and informative. Here are some common types of commits and how to format their messages effectively:

   - **Features**: Introducing new features.
     ```
     FEAT: Add <FeatureName>
     ```
   
   - **Bug Fixes**: Resolving issues or errors.
     ```
     FIX: Resolve <IssueDescription>. Closes #<IssueNumber>
     ```
   
   - **Documentation**: Updating or adding to the documentation, including both code comments and README files.
     ```
     DOCS: Update <Section/Topic> documentation
     ```
   
   - **Refactor**: Enhancing the code without changing its functionality, usually for readability, efficiency, or structure improvements.
     ```
     REFACTOR: Enhance <Component> for better <Aspect>
     ```
   
   - **Snapshot**: Temporarily saving the current state of the project. Useful for marking specific points in development or experimentation and save it into git instead of simply using your IDE Stash feature, which is not visible to others and can be lost if not properly managed.
     ```
     SNAPSHOT: Temporary commit to save the current state for later reference
     ```

### Navigating Commits

If you need to revert to a previous state after making a snapshot or any commit, you can use the following commands:

- To undo the last commit and return your workspace to the state just before that commit (keeping your changes in the working directory):
    ```sh
    git reset --soft HEAD^
    ```
- To completely remove the last commit, including all changes (use with caution):
    ```sh
    git reset --hard HEAD^
    ```

These commands are invaluable for refining your contributions, allowing you to adjust your approach before finalizing your commit.

By following these guidelines for your commits, you help ensure that your contributions are easily integrated and appreciated by the project team and community.

3. **Commit Your Changes**: After making sure your changes are thorough and well-organized, commit them to your branch. Use clear and concise commit messages that accurately describe the changes you've made and their impact on the project.
    ```sh
    git commit -m "FEAT: Add some AmazingFeature"
    ```
Remember, the quality of your commits and their messages significantly affects the review process and the overall development flow. It's always worth taking the extra time to review your changes and craft meaningful commit messages.

### Step 3: Submit Your Contribution

After making your changes, you're ready to contribute them back to the original project.

1. **Push to GitHub**: Push your changes to your fork on GitHub.
    ```sh
    git push origin feature/AmazingFeature
    ```
2. **Open a Pull Request**: Go to the original repository on GitHub, and you should see a prompt to open a pull request from your new branch. Click the "Compare & pull request" button to begin the process.
3. **Describe Your Changes**: Provide a title and detailed description of your changes in the pull request. Explain the rationale behind your changes, any issues they address, and any testing you've performed.
4. **Submit the Pull Request**: Submit your pull request. The project maintainers will then review your contribution. Be open to feedback and ready to make further tweaks or improvements based on their suggestions.

### Step 4: Stay Engaged

After submitting your pull request, stay engaged in the conversation. The project maintainers may have questions or request changes before your contribution can be merged.

- **Respond to Feedback**: Be responsive to comments and feedback from the project's maintainers. If changes are requested, make them promptly and update your pull request.
- **Update Your Branch if Needed**: If your pull request has conflicts with the base branch, you may need to update your branch. You can do this by merging or rebasing your branch with the latest version of the base branch.

### Step 5: Celebrate Your Contribution

Once your pull request has been reviewed and merged, your contribution is now part of the project! Be proud of your work and celebrate your contribution to the open-source community.

---

By following these steps, you can contribute effectively to projects and make a positive impact on the open-source ecosystem. Thank you for contributing!

## License

### Apache License 2.0

This project is licensed under the [Apache License 2.0](LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](LICENSE) file in this repository.

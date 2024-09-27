<div align="center">
  
# [AutoMetric.](https://github.com/BrenoFariasdaSilva/AutoMetric) <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to the **AutoMetric** program! This tool automates the extraction of metadata from GitHub and GitLab repositories that measures Open-Source Software (OSS)quality metrics. It provides insights such as the number of contributors (NC), mean time to update (MTTU), mean time to commit (MTTC), branch protection status (BP), and inactive periods (IP) for repositories.

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

# Task Manager

Based on [HyperionDev](https://www.hyperiondev.com/portfolio/120349/) Task 26 - Capstone Project III

## Description

Task Manager is a software solution for effective team coordination. Its primary purpose is to provide administrators with a user-friendly platform for effortlessly adding team members, granting them access to task lists, enabling task editing capabilities, and generating comprehensive statistics. These statistics encompass the count of pending tasks yet to be completed and the number of tasks that have exceeded their designated deadlines.

## Features

- Login page <br> Checks if user exists (10 attempts max),<br> and for matching password (3 attempts max)
- Main Menu
  - Registering a user <font color=red>(Admin only)</font>
    - Check for existing username
  - Adding a task
    - Select user for the task
    - Enter task name
    - Enter task description
    - Enter a due date for the task
  - View all tasks<br>Shows all the tasks recorded
  - View the logged user tasks<br>Shows all the task assigned to the logged user
    - Edit the task assigned to the user
    - Edit the due date of the task
    - Mark the task as complete
  - Generate Reports <font color=red>(Admin only)</font>
  - Display Statistics <font color=red>(Admin only)</font>
    <br>Shows:<br>Tasks Overview
    - Number of total Tasks
    - Number of Completed
    - Number of Incomplete
    - Number of Overdue
    - Percent of Incomplete
    - Percent of Overdue
    
    Users Overview
    - Number of total users
    - Number of total tasks
    <br>Then for every user
      - Number of assigned tasks
      - Percent of total tasks
      - Percent of Completed
      - Percent of Incomplete
      - Percent of Overdue

---------------------------------------------------------------------------------------------

<!-- ## Latest Version -->

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Parameters](#parameters)
  - [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

In order to utilise this software, you need to follow a few simple steps. Firstly, ensure that you have the latest version of [Python](https://www.python.org/downloads/) installed on your system. It is also recommended to have a Python integrated development environment (IDE) installed, such as [Visual Studio Code](https://code.visualstudio.com/). Once you have completed these installations, open the program file, and execute it. Upon launching, you will receive a series of prompts guiding you to input the required information.
This script relies on the Python standard library, and the library **```borders```**.

### Installation

...

## Usage

Type ```python task_manager.py``` to start the program, then follow the prompts.  
If the file ```users.txt``` does not exist, the program generates a new one creating an administrator user with default login and password set to admin.  
**At the moment it is not possible to add other users to the admin group.**

### Parameters

...

### Examples

...

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub.
2. Clone the fork to your local machine.
3. Create a new branch for your feature or bug fix.
4. Make your changes and commit them.
5. Push the changes to your fork on GitHub.
6. Create a pull request to the original repository.

## License

![GitHub License](https://img.shields.io/github/license/scalvaruso/task_manager?color=blue&link=https://github.com/scalvaruso/task_manager/blob/main/LICENSE.md)


This project is licensed under the MIT License - see the [LICENSE](https://github.com/scalvaruso/task_manager/blob/main/LICENSE.md) file for details.

# init-flask

init-flask is a Python package that helps you setup your [Flask](https://flask.palletsprojects.com/) development environment. Whether you just want to want to create a simple endpoint or you're cooking a large scale project, you choose how much `init-flask` does for you.


## USAGE
### Basic Usage
- `PATH`: Optional(`''` should be specified as optional value of `PATH`). Specifies the directory path where the project will be created. If not provided, the project will be created in the current working directory.

- `PROJECT_NAME`: Required. Specifies the name of the project directory to be created.

### Options

- `--showpg`: Flag. If provided, progress messages will be displayed during execution.

- `--libs LIBS`: Optional. Specifies a comma-separated list of additional Python libraries to install. Example: `--libs "Flask, requests"`

- `--hardcore`: Flag. If provided, enables hardcore mode, which creates additional folders and files for advanced project setup.


## Use Cases

### Basic Initialization
Create a basic Flask project without any additional options:

```bash
init-flask '' my_project
```


## Specify Custom Directory Path

### Create a project in a custom directory path:
```bash
init-flask --showpg D:/Projects my_project
```


## Install Additional Libraries

### Install additional Python libraries during project initialization:
```bash
init-flask --libs "Flask-WTF, SQLAlchemy" '' my_project
```


## Hardcore Mode

### Enable hardcore mode to create additional folders and files:
```bash
init-flask --hardcore '' my_project
```


## Show Progress Messages

### Display progress messages during project initialization:
```bash
init-flask --showpg '' my_project
```


## Combining Options

### Combine multiple options:
```bash
init-flask --showpg --libs "Flask-WTF, SQLAlchemy" --hardcore '' D:/Projects my_project
```
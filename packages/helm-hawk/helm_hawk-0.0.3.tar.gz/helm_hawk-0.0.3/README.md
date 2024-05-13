Control all your operations with helm-hawk!
===========================================

Introduction
------------

helm-hawk is build on top of helm. This CLI provides you with a set of commands to manage your resources. You can use the following commands:

*   **diff**: Group of commands for comparing two versions of helm chart
    
*   **get**: Group of commands to retrieve information from the server
    
*   **history**: Command related to the history of changes in a project.
    
*   **rollback**: This command rolls back a release to a previous revision.
    
*   **status**: This command shows the status of a named release.
    
*   **upgrade**: This command upgrades a release to a new version of a chart.
    
*   **uninstall**: This command takes a release name and uninstalls the release.
    

Global Options
------------


*   **\--context (-c)**: Specify the name of the context you want to use
    
*   **\--namespace (-n)**: Indicate the namespace for which you want to see the resources
    

Requirements
------------

[Helm3](https://helm.sh/docs/intro/install/) \
[Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)



## Installation

Install `helm-hawk` using pip:

```bash
pip install helm-hawk
```

## Usage

```bash
helm-hawk [OPTIONS] COMMAND [ARGS]...
```

### Options

- `-c, --context`: Name of the context you want to use
- `-n, --namespace`: Namespace for which you want to see the resources.
- `--help`: Show this message and exit.

### Commands

#### `diff`

Group of commands for comparing two versions of Helm chart

```bash
helm-hawk diff [OPTIONS] COMMAND [ARGS]...
```

##### Options

- `--help`: Show this message and exit.

##### Commands

- `revision`: Show a diff of a specific revision against the last known one.
- `upgrade`: Show a diff explaining what a Helm upgrade would change.

#### `get`

Group of commands to retrieve information from the server

```bash
helm-hawk get [OPTIONS] COMMAND [ARGS]...
```

##### Options

- `--help`: Show this message and exit.

##### Commands

- `values`: Fetches values for a specific release

#### `history`

Commands related to the history of changes in a project.

```bash
helm-hawk history [OPTIONS] RELEASE_NAME
```

##### Options

- `--max INTEGER`: Maximum number of revisions to include in history (default 256)
- `-c, --context TEXT`: Context that you want to use
- `-n, --namespace TEXT`: Namespace you want to use
- `--help`: Show this message and exit.

#### `rollback`

This command rolls back a release to a previous revision.

```bash
helm-hawk rollback [OPTIONS] RELEASE_NAME REVISION
```

##### Options

- `-c, --context TEXT`: Context that you want to use
- `-n, --namespace TEXT`: Namespace you want to use
- `--dry-run`: Simulate a rollback
- `--no-hooks`: Prevent hooks from running during rollback
- `--help`: Show this message and exit.

#### `status`

This command shows the status of a named release.

```bash
helm-hawk status [OPTIONS] RELEASE_NAME
```

##### Options

- `-c, --context TEXT`: Context that you want to use
- `-n, --namespace TEXT`: Namespace you want to use
- `--revision TEXT`: If set, display the status of the named release with revision
- `-o, --output TEXT`: Prints the output in the specified format. Allowed values: table, json, yaml (default table)
- `--show-desc`: If set, display the description message of the named release
- `--help`: Show this message and exit.

#### `uninstall`

This command takes a release name and uninstalls the release.

```bash
helm-hawk uninstall [OPTIONS] RELEASE_NAME
```

##### Options

- `-c, --context TEXT`: Context that you want to use
- `-n, --namespace TEXT`: Namespace you want to use
- `--dry-run`: Simulate the upgrade
- `--help`: Show this message and exit.

#### `upgrade`

This command upgrades a release to a new version of a chart.

```bash
helm-hawk upgrade [OPTIONS] RELEASE_NAME CHART_PATH
```

##### Options

- `-f, --values TEXT`: Specify values in a YAML file (can specify multiple)
- `-c, --context TEXT`: Context that you want to use
- `-n, --namespace TEXT`: Namespace you want to use
- `--dry-run`: Simulate the upgrade
- `--help`: Show this message and exit.

```
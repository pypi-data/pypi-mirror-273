# cdbt

`cdbt` is a CLI (Command Line Interface) tool developed to enhance and manage DBT (Data Build Tool) builds, particularly focusing on state management and build optimizations. It provides functionalities to refresh, select, and test models efficiently, adding enhancements like conditional child or parent builds directly from the command line.

## Features
- **Full Refresh Control:** Toggle full refreshes on all models.
- **Selective Model Builds:** Use the DBT-style select strings to run specific models.
- **Failure Handling:** Customizable behavior on failures including fast failing options.
- **State Based Builds:** Enhanced state management for efficient DBT runs.
- **Real-Time Output:** Stream output in real-time for better monitoring.

## Installation

To install `cdbt` with pip, run the following command in your terminal:

```bash
pip install cdbt
```

Ensure that you have Python 3.8 or higher installed, as it is required for `cdbt` to function properly.

## Usage

### Basic DBT Shadowed Commands
These commands act as a pass-through to DBT, and are provided for convenience. They are not the primary focus of `cdbt`.

- `cdbt run`
- `cdbt test`
- `cdbt build`

### `trun` (Run and Test)

This command runs the `run` and `test` commands in sequence. It is useful for running both commands in a single step. without executing a snapshot and seed.

```bash
cdbt trun --select my_model
```

### State Build Commands

#### Important Notes

##### Auto Full Refresh

Both the `sbuild` and `pbuild` commands will scan the models to be built and automatically initiate a full refresh if an incrementally materialized model is found in the list (as per `dbt ls`). If you wish to force a `--full-refresh` for other reasons such as a column being added to a seed, add the `--full-refresh` flag.  

##### State Build Commands with Parent and Child Modifiers

Both the `sbuild` and `pbuild` commands can include modifications to build parent or child dependencies by appending a `+` and an optional integer to the command.

- `+` or `+<number>` at the end of the command includes child dependencies up to the specified depth.
- `+<number>` at the beginning of the command includes parent dependencies up to the specified depth.

Example:

- `cdbt pbuild+` and `cdbt pbuild+3` will build all state based variance models along with all child models up to 3 levels deep, respectively.
- `cdbt 3+pbuild` will include parent models up to 3 levels up in the build.

#### Production Build `pbuild`
This command initiates a state based build based on the manifest.json file associated with the master branch. This will use the DBT macro provided by Datacoves `get_last_artifacts` to pull the artifacts from the Snowflake file stage and save to the `./logs` folder. Then comparison is made against this file. This file is updated during the production deployment CI process.

   ```bash
   cdbt pbuild
   ```

#### Local State Build `sbuild`   
Initiates a production state build. 

** Error Handling: **

If an error occurs duing an sbuild operation, the manifest file copied to the `_artifacts` location will be moved back to `target`. This avoids an issue where after executing a state based build with a failure, the next build will not properly compare the state of the models.
```bash
cdbt sbuild
```

## License
Distributed under the MIT License. See `LICENSE` for more information.

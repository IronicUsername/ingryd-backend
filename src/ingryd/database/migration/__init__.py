from glob import glob
import os
from typing import List


def get_ordered_migration_steps() -> List[str]:
    """Retrieve a list of schema changes that reflect base schema evolution.

    This method uses `glob('./migration_steps_*.sql')` to retrieve the migration files,
    this ensures consistency and the right order (at least in migration execution, NOT SQL commands).

    One MUST follow the following naming schema for migration files:
        * File for migration step `i` is called:
            `migration_step_i.sql`
    Note that we start at `migration_step_001.sql` on purpose, as `migration_step_000.sql`, isn't a migration step,
    but the base schema `schema.sql`.

    To add a migration step, do the following:
        1) Create file `migration_step_i.sql` and add alteration queries.
        2) Once done, add your file name to the end of `glob('./migration_steps_*.sql')`.
    While creating your `migration_step_i.sql` file, you can assume that the currently used schema version has
    all `migration_steps` from `glob('./migration_steps_*.sql')` applied to it.


    Returns
    -------
    migration_steps: List[str]
        `migration_steps` is a list of already read SQL schemas, each of which represents a step in the evolution of our base schema: `../schema.sql`.
        The `migration_steps` MUST be applied consecutively.
        Each step MAY consist out of an almost arbitrary magnitute of well formed SQL queries, that change our schema or migrate data.
        Each step MUST at least consist out of one query.

    """
    migration_steps: List[str] = []
    for file_name in sorted(_migration_files()):
        with open(file_name, 'r', encoding='utf-8') as migration_schema:
            migration_steps.append(migration_schema.read())
    return migration_steps


def get_required_version() -> int:
    """Get SHOULD BE version of current production schema.

    Useful for validating that all changes/migration steps were correctly applied.

    Returns
    -------
    version: int
        Version the current DB schema SHOULD have.

    """
    return len(_migration_files())


def _work_dir() -> str:
    """Get current working directory."""
    return os.path.dirname(os.path.abspath(__file__))


def _migration_files() -> List[str]:
    """Get all migration_steps in `migration` directory."""
    return glob(f'{_work_dir()}/migration_step_*.sql')

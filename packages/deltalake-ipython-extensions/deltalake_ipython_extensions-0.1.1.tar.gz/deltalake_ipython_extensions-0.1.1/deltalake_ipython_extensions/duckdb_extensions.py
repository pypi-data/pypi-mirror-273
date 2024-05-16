import json
import os
from IPython.core.magic import register_line_magic, register_cell_magic
import sqlparse
import duckdb
from deltalake import DeltaTable, write_deltalake


duckdb_conn = duckdb.connect(':memory:', config={"allow_unsigned_extensions": "true"})


@register_cell_magic
def sql(line, cell):
    for query in sqlparse.split(cell):
        result = duckdb_conn.execute(query)
    return result.df()


@register_cell_magic
def write_delta(line, cell):
    if not line:
        raise ValueError('No path provided')
    try:
        path, mode = line.split()
    except ValueError:
        raise ValueError('Invalid arguments. Expected path and mode')
    
    storage_options = json.loads(os.environ.get('STORAGE_OPTIONS', '{}'))
    write_deltalake(path, duckdb_conn.execute(cell).fetch_record_batch(rows_per_batch=100000), storage_options=storage_options, mode=mode)
    return f'Written delta table to {path}'


@register_line_magic
def register_delta(line):
    if not line:
        raise ValueError('No path provided')
    try:
        path, name = line.split()
    except ValueError:
        raise ValueError('Invalid arguments. Expected path and name')

    storage_options = json.loads(os.environ.get('STORAGE_OPTIONS', '{}'))
    table = DeltaTable(path, storage_options=storage_options).to_pyarrow_dataset()
    duckdb_conn.register(name, table)
    return f'Registered delta table {name} from {path}'


def load_ipython_extension(ipython):
    """This function is called when the extension is
    loaded. It accepts an IPython InteractiveShell
    instance. We can register the magic with the
    `register_magic_function` method of the shell
    instance."""
    ipython.register_magic_function(sql, 'cell')
    ipython.register_magic_function(write_delta, 'cell')
    ipython.register_magic_function(register_delta, 'line')

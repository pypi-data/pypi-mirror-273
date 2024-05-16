def load_ipython_extension(ipython) -> None:
    from deltalake_ipython_extensions.duckdb_extensions import load_ipython_extension
    load_ipython_extension(ipython)
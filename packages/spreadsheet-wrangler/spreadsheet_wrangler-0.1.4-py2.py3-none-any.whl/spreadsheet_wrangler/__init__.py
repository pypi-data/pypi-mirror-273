"""Top-level package for spreadsheet_wrangler."""

__author__ = """Simon Hobbs"""
__email__ = "simon.hobbs@electrooptical.net"
__version__ = "0.1.4"


from .spreadsheet_wrangler import (
    read_pseodonyms,
    make_unique,
    extract_columns_by_pseudonyms,
    read_csv_to_df,
    read_ods_format_to_df,
    get_supported_file_types_df,
    get_supported_file_formats,
    write,
    read_file_to_df,
    uncluster_ast,
    uncluster_regex,
    uncluster,
    cluster,
    compare,
    select_on_value,
    filter_df,
)  #  noqa

__all__ = [
    "read_pseodonyms",
    "make_unique",
    "extract_columns_by_pseudonyms",
    "read_csv_to_df",
    "read_ods_format_to_df",
    "get_supported_file_types_df",
    "get_supported_file_formats",
    "write",
    "read_file_to_df",
    "uncluster_ast",
    "uncluster_regex",
    "uncluster",
    "cluster",
    "compare",
    "select_on_value",
    "filter_df",
]

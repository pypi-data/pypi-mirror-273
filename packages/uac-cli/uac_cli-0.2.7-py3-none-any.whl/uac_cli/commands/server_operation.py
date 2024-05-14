import click
from uac_api import UniversalController
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids, output_option_binary

@click.group(help='Commands for server operations, such as log rolling and temporary property changes.')
def server_operation():
    pass

@server_operation.command('roll_log', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def roll_log(uac: UniversalController, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.server_operations.roll_log(**vars_dict)
    process_output(output, select, response)


@server_operation.command('temporary_property_change', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value value=value')
@click.pass_obj
@output_option
@select_option
def temporary_property_change(uac: UniversalController, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.server_operations.temporary_property_change(**vars_dict)
    process_output(output, select, response)


@server_operation.command('bulk_export', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def bulk_export(uac: UniversalController, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.server_operations.bulk_export(**vars_dict)
    process_output(output, select, response)

@server_operation.command('bulk_export_with_versions', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def bulk_export_with_versions(uac: UniversalController, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.server_operations.bulk_export_with_versions(**vars_dict)
    process_output(output, select, response)

@server_operation.command('bulk_import', short_help='None')
@click.argument('args', nargs=-1, metavar='path=[path of bulk import files]')
@click.pass_obj
@output_option
@select_option
def bulk_import(uac: UniversalController, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.server_operations.bulk_import(**vars_dict)
    process_output(output, select, response)

@server_operation.command('list_log', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_log(uac: UniversalController, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.server_operations.list_log(**vars_dict)
    process_output(output, select, response)

@server_operation.command('download_log', short_help='None')
@click.argument('args', nargs=-1, metavar='name=log_name')
@click.pass_obj
@output_option_binary
def download_log(uac: UniversalController, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.server_operations.download_log(**vars_dict)
    process_output(output, select, response, text=False, binary=True)
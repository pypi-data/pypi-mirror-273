from pathlib import Path
import click
from uac_api import UniversalController
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids
from uac_cli.utils.config import write_config, read_config, ask_profile, read_profile, write_profile
import json

@click.group()
def config():
    """Manage UAC CLI configuration."""

@config.command(name="add")
@click.option('--profile_name', prompt='Profile Name', type=str)
def add_profile(profile_name):
    """Adds a new profile."""
    profile = read_profile(profile_name)
    if profile is None:
        profile = ask_profile({})
    else:
        if click.confirm("The profile already exists. Do you want to update it?", abort=True):
            profile = ask_profile(profile)
        else:
            return
    
    write_profile(profile_name, profile)

@config.command(name="get")
@click.option('--profile_name', prompt='Profile Name', type=str)
def profile_read(profile_name):
    """Read the profile."""
    profile = read_profile(profile_name)
    if profile is None:
        click.echo(click.style("Profile doesn't exists.", fg="red"))
    else:
        profile['password'] = '***'
        click.echo(click.style(profile, fg="yellow"))
    
@config.command(name="get-all")
def read_all_profiles():
    """Read the profile."""
    profiles = read_config()
    if profiles is None:
        click.echo(click.style("Profile doesn't exists.", fg="red"))
    else:
        for k,v in profiles.items():
            if "password" in v:
                profiles[k]['password'] = "***"
            elif "token" in v:
                profiles[k]['token'] = "***"
        click.echo(click.style(json.dumps(profiles, indent=4), fg="yellow"))

def deactivate_prompts(ctx, param, value):
    if value:
        for p in ctx.command.params:
            if isinstance(p, click.Option) and p.prompt is not None:
                p.prompt = None
    return value

@config.command()
@click.option('--url', type=str)
@click.option('--token', type=str)
@click.option('--username', type=str)
@click.option('--password',  type=str, hide_input=True)
def init(url, token, username, password):
    """Initialize the UAC CLI."""
    config = read_config()
    if config is not None:
        click.echo(f"Profile file already exists. (Path: {Path.home() / '.uac' / 'profiles.yml'})", color="red")
        click.echo("Use `uac config add` command to add a new profile")
        return 

    profile = {
        "url": url,
        "token": token,
        "username": username,
        "password": password
    }
    ask = False
    if url is None:
        ask = True
    if token is None:
        if username is None and password is None:
            ask = True
        
    if ask:
        profile = ask_profile(profile)
    write_profile("default", profile)

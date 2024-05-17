from typing import Dict, List
from metaflow._vendor import click
from .flow_generator import FlowGenerator, PARSE_TYPES, AdditionalDeco
import json

GENERATE_META = ".generate_config"


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.group(help="Commands for DBT on Metaflow")
def dbt():
    pass


@dbt.command(help="Generate a Flow from an existing DBT project")
@click.option(
    "--ci",
    default=False,
    type=bool,
    is_flag=True,
    help="CI mode, which generates based on predefined defaults and values stored in '.generate_config'",
)
@click.pass_obj
def generate(obj, ci=False):
    conf = {
        "project_dir": "./",
        "flow_name": "DBTFlow",
        "remote_config": False,
        "flow_decorators": {
            # TODO: make this configurable
            "conda_base": {"attr": 'packages={"dbt-postgres": ">=1.7.0"}'}
            # "trigger_event": False
        },
        "step_decorators": {
            # "secrets": False,
            # "environment": False,
            # "retry": False
        },
        "parse_type": "raw",
    }
    try:
        with open(GENERATE_META, "r") as f:
            conf = {**conf, **json.load(f)}
    except Exception:
        pass  # cached config load error, not important.

    # Prompt user for configuration if not in CI mode.
    if not ci:
        conf = prompt_config_options(conf)

        # record answers for conf
        with open(GENERATE_META, "w+") as f:
            json.dump(conf, f)

    from ..plugins.dbt.dbt_executor import DBTExecutor

    with DBTExecutor(project_dir=conf["project_dir"]) as executor:
        click.secho("Parsing DBT Project...", bold=True)
        executor.parse()

        click.secho("Generating Flow %s..." % conf["flow_name"], bold=True)

        manifest = executor.manifest()
        generator = FlowGenerator(
            manifest,
            conf["flow_name"],
            conf["project_dir"],
            [
                AdditionalDeco(name=name, **args)
                for name, args in conf["flow_decorators"].items()
                if args
            ],
            [
                AdditionalDeco(name=name, **args)
                for name, args in conf["step_decorators"].items()
                if args
            ],
            conf["parse_type"],
        )
        generator.generate()

        filename = generator.write()
        click.secho(f"Flow has been saved as {filename}")


def prompt_config_options(conf):
    conf["project_dir"] = click.prompt(
        "Path to the DBT project: ", default=conf["project_dir"], show_default=True
    )
    conf["flow_name"] = click.prompt(
        "Name for generated Flow: ", default=conf["flow_name"], show_default=True
    )

    # Configure decorators

    # RETRY
    if click.confirm(
        "Do you want to retry DBT steps in case it fails?",
        default=bool(conf["step_decorators"].get("retry", False)),
    ):
        retries = click.prompt("How many times do you want to retry?", type=int)
        conf["step_decorators"]["retry"] = {"attr": f"times={retries}"}

    # Config for remote execution environments.
    conf["remote_config"] = click.confirm(
        "Do you need to supply values to your DBT Profile?",
        default=conf["remote_config"],
    )
    if conf["remote_config"]:
        # SECRETS
        if click.confirm(
            "Read values from a secrets provider? (Suggested for sensitive information, such as database credentials)",
            default=conf["step_decorators"].get("secrets", False),
        ):
            secret_key = click.prompt(
                "What is the name of the secret that you want to use?", type=str
            )
            conf["step_decorators"]["secrets"] = {
                "attr": "sources=SECRET_SRC",
                "constant": f'SECRET_SRC=["{secret_key}"]',
            }

        # ENVIRONMENT
        if click.confirm(
            "Supply values as environment variables?",
            default=conf["step_decorators"].get("environment"),
        ):
            inputs = keep_prompting(
                "Enter a value for the environment in the form of VARIABLE='some value'"
            )
            envs = dict(ip.split("=") for ip in inputs)
            conf["step_decorators"]["environment"] = {
                "attr": "vars=ENVS",
                "constant": f"ENVS={envs}",
            }

    else:
        # reset values as they might be true from previous generate.
        conf["step_decorators"].pop("secrets")
        conf["step_decorators"].pop("environment")

    conf["parse_type"] = click.prompt(
        "How should we parse the project?", type=click.Choice(PARSE_TYPES)
    )

    return conf


def keep_prompting(prompt, acc=[]):
    click.echo(acc)
    val = click.prompt(f"{prompt} (Empty to confirm.)", default="", show_default=False)
    if val == "":
        return acc
    acc.append(val)
    return keep_prompting(prompt, acc)

import os
import click
import notify


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config", default="config.json", help="Path to config file.")
def weekly_sammary_report(config):
    report = notify.Community(config)
    report.weekly_sammary_report()


@cli.command()
@click.option("--config", default="config.json", help="Path to config file.")
def delay_report(config):
    report = notify.Community(config)
    report.delay_report()


@cli.command()
@click.option("--config", default="config.json", help="Path to config file.")
def due_soon_report(config):
    report = notify.Community(config)
    report.get_upcoming_due_cards()


@click.command()
@click.option("--config", default="config.json", help="Path to config file.")
def create_monthly_card(config):
    report = notify.Community(config)
    pass


@click.command()
@click.option("--config", default="config.json", help="Path to config file.")
def create_specfic_date_card(config):
    report = notify.Community(config)
    pass


if __name__ == "__main__":
    cli()

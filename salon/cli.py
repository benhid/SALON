import click

from salon.command import enrich, load, export, parse


@click.group()
def entry_point():
    pass


entry_point.add_command(load.load)
entry_point.add_command(load.create)
entry_point.add_command(enrich.enrich)
entry_point.add_command(export.export)
entry_point.add_command(parse.parse)

if __name__ == "__main__":
    entry_point()

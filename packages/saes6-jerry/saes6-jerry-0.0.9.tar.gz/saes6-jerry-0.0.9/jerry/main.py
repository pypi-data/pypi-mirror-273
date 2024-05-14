import click

@click.command()
@click.argument("name")
def main(name):
    print(f'Hello {name}')


@click.command()
@click.argument("aa")
def hello(aa):
    print(f'Hello {aa}')
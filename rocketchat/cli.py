import click
import cosmicray
import rocketchat

from cosmicray import pprint


USER_FORMAT = '{0.username}'
CHANNEL_FORMAT = '{0.name}'
MESSAGE_FORMAT = '{0.ts}|{0.u[username]}: {0.msg}'
INFO_FORMAT = ('Server API Version: {0[info][version]}\n'
               'Client API Version: {1}')


def status_color(user_status):
    if user_status == 'online':
        return pprint.FG_GREEN
    elif user_status == 'offline':
        return pprint.FG_RED
    return pprint.FG_YELLOW


@click.group()
def cli():
    rocketchat.load_config()


@click.command()
def info():
    click.echo(INFO_FORMAT.format(
        rocketchat.v1.info().get(), rocketchat.__version__))

@click.command()
def whoami():
    pprint.pprint(
        rocketchat.models.User(),
        formattings=[pprint.Formatting('me', formatter=USER_FORMAT)])


@click.group()
def configure():
    pass


@click.command()
@click.option('--domain', '-d', help='Specify domain')
@click.option('--verbose/--no-verbose', '-v', help='Enable verbose logging', default=False)
@click.option('--verify/--no-verify', help='Disable SSL checking', default=False)
def domain(domain, verbose, verify):
    rocketchat.configure(
        monkey_patch=not verify,
        config={'debug': verbose},
        domain=domain,
        verify=verify)
    rocketchat.store_config()


@click.command()
@click.option('--username', help='Rocketchat username')
@click.option('--prompt-password', help='Rocketchat password prompt',
              prompt=True, hide_input=True)
def password(username, password):
    rocketchat.create_creds_file(
        username=username,
        password=password)


@click.command()
def channels():
    pprint.pprint(
        rocketchat.models.Channel(),
        formattings=[
            pprint.Formatting(
                'channels', formatter=CHANNEL_FORMAT, is_sequence=True,
                formattings=[
                    pprint.Formatting(
                        'last_message', formatter=MESSAGE_FORMAT)
                ])])


@click.command()
@click.option('--status/--no-status', help='Show user status', default=False)
@click.option('--name/--no-name', help='Show user name', default=False)
@click.option('--id/--no-id', help='Show user id', default=False)
def users(status, name, id):
    extra_formattings = []
    if status:
        extra_formattings.append(
            pprint.Formatting('status', color_if=status_color))
    if name:
        extra_formattings.append(
            pprint.Formatting('name'))
    if id:
        extra_formattings.append(
            pprint.Formatting('_id'))
    pprint.pprint(
        rocketchat.models.User(),
        formattings=[
            pprint.Formatting(
                'users', formatter=USER_FORMAT, is_sequence=True,
                formattings=extra_formattings)])


@click.group()
def ls():
    pass


cli.add_command(info)
cli.add_command(configure)
cli.add_command(whoami)
cli.add_command(ls)
configure.add_command(domain)
configure.add_command(password)
ls.add_command(channels)
ls.add_command(users)


if __name__ == '__main__':
    cli(obj={})

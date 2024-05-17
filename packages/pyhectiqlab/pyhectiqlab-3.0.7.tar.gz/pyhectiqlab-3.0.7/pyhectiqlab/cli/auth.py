import click


@click.group()
def auth_group():
    pass


@auth_group.command("authenticate", help="Authenticate to the Hectiq Lab.")
def authenticate():
    """Authenticate to the Hectiq Console."""
    import httpx
    import os
    import toml
    from pyhectiqlab.auth import is_authenticated
    from pyhectiqlab import API_URL
    from pathlib import Path

    is_logged = is_authenticated()
    click.secho("👋 Welcome!")

    if is_logged:
        # Ask if the user wants to add a new key
        click.secho("You are already logged in.", fg="green")
        should_continue = click.prompt(
            "Do you still want to continue and create a new API key?",
            default="y",
            show_default=True,
            type=click.Choice(["y", "n"]),
        )
        if should_continue == "n":
            return

    # Accessing the user using basic authentication
    click.secho("Please enter your credentials.")
    email = click.prompt("Email", type=str)
    password = click.prompt("Password", type=str, hide_input=True)

    try:
        import socket

        name = socket.gethostname()
    except:
        name = "[unknown hostname]"
    credentials_path = os.getenv(
        "HECTIQ_LAB_CREDENTIALS_FILE",
        os.path.join(Path.home(), ".hectiq-lab", "credentials.toml"),
    )
    os.makedirs(os.path.dirname(credentials_path), exist_ok=True)

    # Get the API key
    auth = httpx.BasicAuth(username=email, password=password)
    body = dict(name=name)
    res = httpx.post(f"{API_URL}/app/auth/api-keys", json=body, auth=auth)
    if res.status_code != 200:
        click.echo("Authentication failed.")
        click.echo(res)
        return
    api_key = res.json()

    # Save the key in .hectiq-lab/credentials
    with open(credentials_path, "a") as f:
        # Dump as TOML
        data = {}
        data[name] = api_key
        toml.dump(data, f)
        f.write("\n")

        click.echo(f"A new API key has been added to {credentials_path}.")
    click.secho("You are now logged in.", fg="green")


@auth_group.command("show-secret-key", help="Show the secret key.")
def show_key():
    from pyhectiqlab.auth import load_credentials

    data = load_credentials()
    click.echo(f"Your secret key is: {data['value']}")

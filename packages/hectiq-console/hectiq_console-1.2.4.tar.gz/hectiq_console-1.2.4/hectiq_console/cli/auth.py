import click


@click.group()
def auth_group():
    pass

@auth_group.command("authenticate")
@click.option("--replace", 
              is_flag=True, 
              default=False, help="If the key already exists, replace it.")
@click.option("--generate", '-g', 'only_generate', 
              is_flag=True, 
              default=False, 
              help="If True, the key is only generated and not saved on your computer. Use this option if you want to use the key on another device.")
def cli_authenticate(replace: bool, only_generate: bool):
    """Authenticate to the Hectiq Console."""
    from hectiq_console.functional import authenticate
    from hectiq_console import CONSOLE_APP_URL
    from pathlib import Path
    import requests
    import os
    import toml

    if only_generate:
        click.secho("🚨 Mode is set to generate only. The key will not be saved on your computer.", fg="cyan")
    is_logged = authenticate()
    
    if is_logged and not only_generate:
        # Ask if the user wants to add a new key
        click.secho("You are already logged in.", fg="green")
        should_continue = click.prompt("Do you still want to continue and create a new API key?",
                                        default="y", 
                                        show_default=True, 
                                        type=click.Choice(["y", "n"]))
        if should_continue=="n":
            return
    
    email = click.prompt("Email address", type=str)
    password = click.prompt("Password", type=str, hide_input=True)
    try:
        import socket
        name = socket.gethostname()
    except:
        name = "[unknown hostname]"
    
    name = click.prompt("Alias for the API key:", type=str, default=name)

    # Get the organizations
    res = requests.post(f"{CONSOLE_APP_URL}/app/auth/login", 
                 json={"email": email, "password": password})
    if res.status_code!=200:
        click.echo("Authentication failed.")
        return
    
    user = res.json()
    if user.get("organizations") is None:
        click.echo("You are not part of any organization. Please contact your administrator.")
        return
    
    click.echo("Select an organization:")
    for i, org in enumerate(user.get("organizations")):
        click.echo(f"[{i}] - {org.get('name')}")
    index = click.prompt("Enter the index of the organization:", 
                 type=click.Choice([str(i) for i in range(len(user.get("organizations")))]))
    organization_slug = user.get("organizations")[int(index)]["slug"]

    if not only_generate:
        path = os.getenv("HECTIQ_CONSOLE_CREDENTIALS_FILE", 
                            os.path.join(Path.home(),".hectiq-console", "credentials.toml"))
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Load the existing keys
        if os.path.exists(path):
            with open(path, "r") as f:
                current_auth_data = toml.load(f)
        else:
            current_auth_data = {}

        should_replace = True
        if organization_slug in current_auth_data:
            if not replace:
                click.secho(f"⚠️ A key for {organization_slug} already exists. Use --replace to replace it.", err=True, fg="red")
                return
            else:
                should_replace = True

    # Get the API key
    res = requests.post(f"{CONSOLE_APP_URL}/app/auth/api-keys", 
                  json={"email": email, "password": password, "name": name, "organization": organization_slug})
    if res.status_code!=200:
        click.echo("Authentication failed.")
        return
    api_key = res.json()

    if only_generate:
        click.secho(f"Your API key:")
        click.secho(f"{api_key['value']}", bold=True)
        click.secho(f"⚠️ The value above is your API key for {organization_slug}. It won't be show again and the key has not been saved on your computer.", bg="red", fg="white", bold=True)
        click.echo(f"Use HECTIQ_CONSOLE_API_KEY to authenticate or visit https://hectiq-console.surge.sh/authenticate.html to learn how to use the key.")
        return
    
    if should_replace:
        api_key["email"] = email
        current_auth_data[organization_slug] = api_key
        with open(path, "w") as f:
            toml.dump(current_auth_data, f)
        click.echo(f"The API key for {organization_slug} has been replaced at {path}.")
    else:
        # Save the key in .hectiq-console/credentials
        with open(path, "a") as f:
            # Dump as TOML
            data = {}
            api_key["email"] = email
            data[organization_slug] = api_key
            toml.dump(data, f)
            f.write("\n")

        click.echo(f"A new API key has been added to {path}.")
    click.secho("You are now logged in.", fg="green")

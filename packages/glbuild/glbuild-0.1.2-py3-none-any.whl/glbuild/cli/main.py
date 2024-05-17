"""Main CLI tool module."""

import click
from glbuild import GitLabBuild


@click.group(invoke_without_command=True)
@click.option("--token", "-t", type=str, required=True)
@click.option("--project", "-p", type=int, required=True, multiple=True)
@click.option("--output", "-o", required=True, help="Output directory")
@click.option("--base-url", "-b", type=str, default="https://gitlab.com")
@click.option("--api-version", type=int, default=4)
@click.option("--ssl-verify", type=bool, default=False)
def cli(token, projects, output, base_url, api_version, ssl_verify):
    """Glbuild CLI.

    Collect historical GitLab build data easily.
    """
    glb = GitLabBuild(
        base_url=base_url,
        token=token,
        projects=list(projects),
        api_version=api_version,
        ssl_verify=ssl_verify,
    )
    glb.start(output=output)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()

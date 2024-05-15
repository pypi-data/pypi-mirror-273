import click

from .helpers import xnatpy_login_options, connect_cli


@click.group()
def download():
    """
    Commands to download XNAT objects to your machine.
    """
    pass


@download.command()
@click.argument('project')
@click.argument('targetdir')
@xnatpy_login_options
def project(project, targetdir, **kwargs):
    """Download XNAT project to the target directory."""
    with connect_cli(**kwargs) as session:
        xnat_project = session.projects.get(project)

        if xnat_project is None:
            session.logger.error('[ERROR] Could not find project!'.format(project))
            return

        result = xnat_project.download_dir(targetdir)
        session.logger.info("Download complete!")


@download.command()
@click.argument('project')
@click.argument('experiments', nargs=-1)
@click.argument('targetdir')
@xnatpy_login_options
def experiments(project, experiments, targetdir, **kwargs):
    """Download XNAT project to the target directory."""
    with connect_cli(**kwargs) as session:

        if project not in session.projects:
            session.logger.error(f"[ERROR] Could not find project: '{project} for user {kwargs.get('user')}'")
            return

        xnat_project = session.projects[project]

        for experiment in experiments:
            if experiment not in xnat_project.experiments:
                session.logger.warning(f"[WARNING] Could not find experiment '{experiment}'")
                continue

            xnat_project.experiments[experiment].download_dir(targetdir)
        session.logger.info("Download complete!")

from pathlib import Path

import click

from nastranio.readers.gmsh.study import Study


@click.command()
@click.argument("meshfile", type=click.Path(exists=True))
@click.argument("params", type=click.Path(exists=True))
@click.option("--overwrite/--no-overwrite", default=False)
def study(meshfile, params, overwrite):
    study = Study(meshfile, autobuild=False)
    study.load_user_params(params)
    study.build()
    study.run(exist_ok=overwrite)


@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)


@main.command()
@click.argument("meshfile", type=click.Path(exists=True))
@click.option("-p", "params", type=click.Path(exists=True), default=None)
@click.option("-o", "output", type=click.Path(exists=False), default=None)
def msh2nas(meshfile, params, output):
    meshfile = Path(meshfile)
    study = Study(meshfile, autobuild=False)
    if params is not None:
        params = Path(params)
    study.load_user_params(params)
    study.build()
    if output is not None:
        output = Path(output)
        if output.suffix in (".nas", ".dat", ".bulk"):
            study.to_nastran(target=output)
        elif output.suffix in (".msh", ".mesh"):
            study.reg.mesh.to_gmsh(filename=output)
    study.run()

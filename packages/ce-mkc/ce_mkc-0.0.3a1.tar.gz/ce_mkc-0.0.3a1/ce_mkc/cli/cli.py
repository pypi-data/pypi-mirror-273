from enum import Enum
from pathlib import Path

import typer
from typing import Optional
from typing_extensions import Annotated

from ce_mkc.main.ce_mkc import main

from ce_mkc import __app_name__, __version__

class LogLevels(str, Enum):
    none = "none"
    info = "info"
    verbose = "verbose"

class Arguments:
    def __init__(self, config, connectors, schemas, forceDownload, launchFullStack, logLevel):
        self._config = config
        self._connectors = connectors
        self._schemas = schemas
        self._forceDownload = forceDownload
        self._launchFullStack = launchFullStack
        self._logLevel = logLevel

    @property
    def config(self):
        return self._config
    
    @property
    def connectors(self):
        return self._connectors
    
    @property
    def schemas(self):
        return self._schemas
    
    @property
    def forceDownload(self):
        return self._forceDownload
    
    @property
    def launchFullStack(self):
        return self._launchFullStack
    
    @property
    def logLevel(self):
        return self._logLevel

    def __repr__(self):
        return (f"Arguments = {{ 'config' : {self._config!r}, 'connectors' : {self._connectors!r},"
            f"'schemas' : {self._schemas!r}, 'forceDownload' : {self._forceDownload!r},"
            f"'launchFullStack' : {self._launchFullStack!r}, 'logLevel' : {self._logLevel!r}}}")



app = typer.Typer(no_args_is_help=True)

@app.command(
        name="provision"
        )
def provision(
        config: Annotated[Path, typer.Option(    
                exists=True, file_okay=True, dir_okay=False, writable=False, readable=True, resolve_path=True,
                help="A string representing the path to the config.json file"
            )] = 'config/config.json',
        connectors: Annotated[str, typer.Option(help="A comma separated string of paths to the configs describing the MongoDB connectors to install")] = None,
        schemas: Annotated[str, typer.Option(help="A comma separated string of paths to the configs describing the schemas to register")] = None,
        forceDownload: Annotated[bool, typer.Option("--forceDownload", help="Include this flag to force mkc to download the mongodb kafka connector")] = False,
        launchFullStack: Annotated[bool, typer.Option("--launchFullStack", help="Include this flag to launch the full stack (kafka/zookeeper, kafka connect, schema registry, akhq, mongod)")] = False,
        logLevel: Annotated[LogLevels, typer.Option(help="Log level. Possible values are [none, info, verbose]")] = LogLevels.info,
        ):
    """
    Welcome to mkc, a command line utility to set up Kafka, MongoDB, and MongoDB Kafka Connector environments.
    """
    args = Arguments(
        config=config,
        connectors=connectors,
        schemas=schemas,
        forceDownload=forceDownload,
        launchFullStack=launchFullStack,
        logLevel=logLevel
    )

    main(args)

@app.command()
def version() -> None:
    """Print version information about the application"""
    _version_callback(True)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    

@app.callback()
# @use_yaml_config(default_value="config.yaml")
def version_callback_hack(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
): 
    return

def run():
    app(prog_name= __app_name__)

if __name__ == "__main__":
    run()
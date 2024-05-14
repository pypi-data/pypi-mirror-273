import sys
import logging
import click
from . import __version__


class CtmCli:
    def __init__(self, log_level='ERROR'):
        self.log_level = log_level
        self.setup_logging()
        
    def setup_logging(self):
        if self.log_level != "DEBUG":
            sys.tracebacklimit = 0
        logging.basicConfig(level=self.log_level)
        logging.info(f'CTM CLI is running... (Version: {__version__})')
        self.log = logging

    def main(self):
        pass

@click.group()
@click.version_option(version=__version__)
@click.option('--log-level', '-l', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']), default='ERROR')
@click.option('--debug', '-d', is_flag=True, default=False, help='Enable debug mode')
@click.pass_context
def main(ctx, log_level, debug):
    if debug:
        log_level = 'DEBUG'

    cli = CtmCli(log_level=log_level)
    ctx.obj = cli.main()


def run():
    main(auto_envvar_prefix='CTM')

if __name__ == '__main__':
    main(auto_envvar_prefix='CTM')
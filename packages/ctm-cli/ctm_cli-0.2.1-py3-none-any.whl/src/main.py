import sys
import logging
import click
import os
import re
from pathlib import Path
from . import __version__
import ctm_cli.errors as errors



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
        self.os_type = self.determine_os_type()
        self.log.info(f'OS type: {self.os_type}')

    def main(self):
        self.check_log_files()

    def determine_os_type(self):
        # Check the OS type
        if sys.platform == 'win32':
            os_type = 'windows'
        elif sys.platform == 'linux':
            os_type = 'linux'
        else:
            os_type = 'unknown'
        
        return os_type
    
    def check_log_files(self):
        if self.os_type == 'windows':
            self.log.info('Windows not supported')
            sys.exit(1)

        self.log.info('Checking Linux log files...')
        if os.path.exists('/var/opt/universal/log/unv.log'):
            self.log.info('Found /var/opt/universal/log/unv.log')
            with open('/var/opt/universal/log/unv.log', 'r') as f:
                error_list = set()
                for line in f:
                    if 'UNV' in line:
                        self.log.info(line)
                        match = re.search(r'(UNV\d\d\d\dE) \[\d*]', line)
                        if match:
                            if match.group(1) not in error_list:
                                error_list.add(match.group(1))
                                
                print(f'Found {len(error_list)} UNV errors')
                print(list(error_list))





@click.command()
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
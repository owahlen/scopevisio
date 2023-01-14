import argparse

from accounting import retrieve_accounting
from logger import configure_logger
from scopevisio_config import get_scopevisio_config


def main(config_filename: str, export_folder_name: str, skip_document_download: bool):
    config = get_scopevisio_config(config_filename)
    retrieve_accounting(config=config,
                        export_folder_name=export_folder_name,
                        skip_document_download=skip_document_download)


if __name__ == '__main__':
    configure_logger()
    parser = argparse.ArgumentParser(description='Extract all accounting data of a company from Scopevisio')
    parser.add_argument('-c', '--configfile', default='scopevisio.ini',
                        help='Path of the file containing the Scopevisio configuration [scopevisio.ini]')
    parser.add_argument('-e', '--exportfolder', default='export',
                        help='Path of the folder that will contain the export [export]')
    parser.add_argument('-s', '--skipdocumentdownload', action='store_true',
                        help='Skip downloading of document files [false]')
    args = parser.parse_args()
    main(config_filename=args.configfile,
         export_folder_name=args.exportfolder,
         skip_document_download=args.skipdocumentdownload)

import sys
import os
import importlib.metadata
import argparse


from . import PACKAGE_NAME
from . import ROOT_MODULE_NAME


def main():

    this_file_path = __file__

    assert '__main__.py' == os.path.basename(this_file_path)

    root_module_dir_path = os.path.dirname(this_file_path)

    assert ROOT_MODULE_NAME == os.path.basename(root_module_dir_path)

    installation_dir_path = os.path.dirname(root_module_dir_path)

    assert os.path.basename(installation_dir_path) in [PACKAGE_NAME, 'site-packages']


    metadata = None
    try:
        metadata = importlib.metadata.metadata(PACKAGE_NAME)
    except importlib.metadata.PackageNotFoundError:
        pass

    summary = metadata['Summary'] if metadata else 'summary_not_available'
    version = metadata['Version'] if metadata else 'version_not_available'


    arg_parser = argparse.ArgumentParser(
        prog                  = ROOT_MODULE_NAME,
        description           = summary,
        formatter_class       = argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars = '@'
    )
    
    arg_parser.add_argument(
        '-V', '--version',
        action  = 'version',
        version = PACKAGE_NAME + ' ' + version
    )
    
    args = arg_parser.parse_args()


    data_dir_path = os.path.join(root_module_dir_path, 'data')

    assert os.path.isdir(data_dir_path)

    quote_file_path = os.path.join(data_dir_path, 'quote.txt')

    assert os.path.isfile(quote_file_path)

    with open(quote_file_path, 'r') as quote_file:

        quote_str = quote_file.read().strip()

    print(quote_str)
    
    return 0


if '__main__' == __name__:
    sys.exit(main())



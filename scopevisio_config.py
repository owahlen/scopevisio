import configparser


def get_scopevisio_config(config_filename):
    config = configparser.ConfigParser()
    config.read(config_filename)
    return config['SCOPEVISIO']

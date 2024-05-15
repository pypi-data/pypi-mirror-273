# This file is used to store the bookshelf of the project.
# Get the path of the bin files and check if the files exist.
import pathlib


class BaseSpamLanguage(object):
    pass


LOCAL_PATH = pathlib.Path(__file__).parent.joinpath('bin')
LOCAL_BIN = {
    "cn_pornographic": LOCAL_PATH.joinpath('cn_pornographic.bin'),
    "cn_politics": LOCAL_PATH.joinpath('cn_politics.bin'),
    "cn_advertisement": LOCAL_PATH.joinpath('cn_advertisement.bin'),
    "cn_general": LOCAL_PATH.joinpath('cn_general.bin'),
    "cn_netease": LOCAL_PATH.joinpath('cn_netease.bin'),
}

# Check if the files exist
for key, value in LOCAL_BIN.items():
    if not value.exists():
        raise FileNotFoundError(f"File {value} not found.")


class CN(BaseSpamLanguage):
    PORNOGRAPHIC = LOCAL_BIN['cn_pornographic']
    ADVERTISEMENT = LOCAL_BIN['cn_advertisement']
    POLITICS = LOCAL_BIN['cn_politics']
    GENERAL = LOCAL_BIN['cn_general']
    NETEASE = LOCAL_BIN['cn_netease']


class SpamShelf(object):
    CN = CN()

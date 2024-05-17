VERSION = (6, 1, "16a2")
__version__ = ".".join([str(s) for s in VERSION])

__title__ = "zhixin"
__description__ = (
    "Your Gateway to Embedded Software Development Excellence. "
    "Unlock the true potential of embedded software development "
    "with ZhiXin's collaborative ecosystem, embracing "
    "declarative principles, test-driven methodologies, and "
    "modern toolchains for unrivaled success."
)
__url__ = "https://zhixin.org"

__author__ = "ZhiXin Labs"
__email__ = "contact@zxlabs.com"

__license__ = "Apache Software License"
__copyright__ = "Copyright 2014-present ZhiXin Labs"

__accounts_api__ = "https://api.accounts.zhixin.org"
__registry_mirror_hosts__ = [
    "registry.zhixin.org",
    "registry.nm1.zhixin.org",
]
__zxremote_endpoint__ = "ssl:host=remote.zhixin.org:port=4413"

__check_internet_hosts__ = [
    "185.199.110.153",  # Github.com
    "88.198.170.159",  # zhixin.org
    "github.com",
] + __registry_mirror_hosts__

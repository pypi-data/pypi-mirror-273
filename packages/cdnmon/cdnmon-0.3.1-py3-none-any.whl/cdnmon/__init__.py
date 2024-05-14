import coloredlogs
import logging
import requests
import yaml
import functools

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

class CDN:
    def __init__(self, name):
        self._data = self._fetch_cdn_data(name)
        self.name = self._data["name"]
        self.cname_suffixes = self._data["cname_suffixes"]
        self.asn_patterns = self._data["asn_patterns"]

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _fetch_cdn_data(name):
        url = f"https://cdnmon.vercel.app/{name}.yaml"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch CDN data from {url}")
        raw = response.content
        return yaml.safe_load(raw)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

def main():
    cdn_names = [
        "akamai",
        "alibaba-cdn",
        "alibaba-dcdn",
        "alibaba-waf",
        "asia-isp",
        "baidu",
        "baishan",
        "cloudflare",
        "cloudfront",
        "ctyun",
        "douyin",
        "fastly-edge-compute",
        "fastly",
        "frontdoor",
        "huawei",
        "jd",
        "kingsoft",
        "qiniu",
        "tencent",
        "ucloud",
        "upyun",
        "volc",
        "wangsu",
    ]
    for cdn_name in cdn_names:
        cdn = CDN(cdn_name)
        print(cdn)

if __name__ == "__main__":
    main()
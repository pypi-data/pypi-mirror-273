from cdnmon.model.cdn import AbstractCDN
from cdnmon.util.cidr import deduplicate_networks


class CDN(AbstractCDN):
    def __init__(self):
        self.abbreviation = "cloudflare"
        self.ipv4_url = "https://www.cloudflare.com/ips-v4"
        self.ipv6_url = "https://www.cloudflare.com/ips-v6"
        self.asn_patterns = [
            "cloudflare",
        ]
        self.cname_suffixes = [
            ".cdn.cloudflare.net",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

    def extract(self):
        import requests

        return {
            "ipv4": requests.get(self.ipv4_url).text,
            "ipv6": requests.get(self.ipv6_url).text,
        }

    def transform(self, response):
        ipv4_networks = [line.strip() for line in response["ipv4"].split("\n") if line.strip() != ""]
        ipv6_networks = [line.strip() for line in response["ipv6"].split("\n") if line.strip() != ""]
        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks, filter_version=4),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks, filter_version=6),
        }

from cdnmon.model.cdn import AbstractCDN
from cdnmon.util.cidr import deduplicate_networks


class CDN(AbstractCDN):
    def __init__(self):
        self.abbreviation = "fastly"
        self.ipv4_url = "https://api.fastly.com/public-ip-list"
        self.ipv6_url = self.ipv4_url
        self.asn_patterns = [
            "fastly",
        ]
        self.cname_suffixes = [
            ".fastly.net",
            ".fastlylb.net",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

    def extract(self):
        """
        [1] https://api.fastly.com/public-ip-list
        """
        import requests
        import ipaddress

        data = requests.get(self.ipv4_url).json()

        ipv4_networks = []
        for ipv4_prefix in data["addresses"]:
            ipv4_networks.append(str(ipaddress.IPv4Network(ipv4_prefix, strict=False)))

        ipv6_networks = []
        for ipv6_prefix in data["ipv6_addresses"]:
            ipv6_networks.append(str(ipaddress.IPv6Network(ipv6_prefix, strict=False)))

        return {
            "ipv4": "\n".join(ipv4_networks),
            "ipv6": "\n".join(ipv6_networks),
        }

    def transform(self, response):
        ipv4_networks = [line.strip() for line in response["ipv4"].split("\n") if line.strip() != ""]
        ipv6_networks = [line.strip() for line in response["ipv6"].split("\n") if line.strip() != ""]
        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks, filter_version=4),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks, filter_version=6),
        }

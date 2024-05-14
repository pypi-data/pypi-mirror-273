from cdnmon.model.cdn import AbstractCDN
from cdnmon.util.cidr import deduplicate_networks


class CDN(AbstractCDN):
    def __init__(self):
        self.abbreviation = "google"
        self.ipv4_url = "https://www.gstatic.com/ipranges/cloud.json"
        self.ipv6_url = self.ipv4_url
        self.asn_patterns = [
            "google",
        ]
        self.cname_suffixes = []
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

    def extract(self):
        """
        [1] https://support.google.com/a/answer/10026322
        [2] https://www.gstatic.com/ipranges/goog.json
        [3] https://www.gstatic.com/ipranges/cloud.json
        """
        import requests
        import ipaddress

        data = requests.get(self.ipv4_url).json()

        ipv4_networks = []
        ipv6_networks = []

        prefixes = data["prefixes"]
        for prefix in prefixes:
            if "ipv4Prefix" in prefix:
                ipv4_networks.append(str(ipaddress.IPv4Network(prefix.get("ipv4Prefix"), strict=False)))

            if "ipv6Prefix" in prefix:
                ipv6_networks.append(str(ipaddress.IPv6Network(prefix.get("ipv6Prefix"), strict=False)))

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

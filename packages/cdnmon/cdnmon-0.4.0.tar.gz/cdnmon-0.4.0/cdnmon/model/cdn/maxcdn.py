from cdnmon.model.cdn import AbstractCDN
from cdnmon.util.cidr import deduplicate_networks


class CDN(AbstractCDN):
    def __init__(self):
        self.abbreviation = "maxcdn"
        self.ipv4_url = "https://support.maxcdn.com/hc/en-us/article_attachments/360051920551/maxcdn_ips.txt"
        self.ipv6_url = self.ipv4_url
        self.asn_patterns = [
            "maxcdn",
        ]
        self.cname_suffixes = [
            ".netdna-cdn.com",
            ".netdna-ssl.com",
            ".netdna.com",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

    def extract(self):
        """
        [1] https://support.maxcdn.com/one/tutorial/ip-blocks/
        [2] https://support.maxcdn.com/one/assets/ips.txt (302 Redirected to [3])
        [3] https://support.maxcdn.com/hc/en-us/article_attachments/360051920551/maxcdn_ips.txt
        """
        import requests

        text = requests.get(self.ipv4_url).text
        return {
            "ipv4": text,
            "ipv6": text,
        }

    def transform(self, response):
        ipv4_networks = [line.strip() for line in response["ipv4"].split("\n") if line.strip() != ""]
        ipv6_networks = [line.strip() for line in response["ipv6"].split("\n") if line.strip() != ""]
        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks, filter_version=4),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks, filter_version=6),
        }


def main():
    cdn = CDN()
    print(cdn.transform(cdn.extract()))


if __name__ == "__main__":
    main()

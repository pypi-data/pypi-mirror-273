from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="keycdn",
        )
        self.asn_patterns = [
            "keycdn",
        ]
        self.cname_suffixes = [
            ".kxcdn.com",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

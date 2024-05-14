from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="baidu",
        )
        self.asn_patterns = [
            "baidu",
        ]
        self.cname_suffixes = [
            ".a.bdydns.com",
            ".yjs-cdn.com",
            ".yunjiasu-cdn.net",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

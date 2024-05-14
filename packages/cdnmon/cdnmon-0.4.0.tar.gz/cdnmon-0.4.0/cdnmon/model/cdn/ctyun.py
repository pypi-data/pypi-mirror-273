from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="ctyun",
        )
        self.asn_patterns = [
            "chinanet",
        ]
        self.cname_suffixes = [
            ".ctadns.cn",
            ".ctacdn.cn",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

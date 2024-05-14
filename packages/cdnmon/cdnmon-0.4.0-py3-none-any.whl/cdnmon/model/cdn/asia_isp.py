from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="asia-isp",
            query_term="asia-isp",
        )
        self.asn_patterns = [
            "asia-isp",
        ]
        self.cname_suffixes = [
            ".cy-isp.com",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

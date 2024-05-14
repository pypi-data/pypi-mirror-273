from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="kingsoft",
            query_term="ksyun",
        )
        self.asn_patterns = [
            "kingsoft",
        ]
        self.cname_suffixes = [
            ".download.ks-cdn.com",
            ".ksyuncdn.com",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

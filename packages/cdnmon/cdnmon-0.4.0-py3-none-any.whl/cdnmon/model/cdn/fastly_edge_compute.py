from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(abbreviation="fastly-edge-compute", query_term="fastly")
        self.asn_patterns = [
            "fastly",
        ]
        self.cname_suffixes = [
            ".edgecompute.app",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

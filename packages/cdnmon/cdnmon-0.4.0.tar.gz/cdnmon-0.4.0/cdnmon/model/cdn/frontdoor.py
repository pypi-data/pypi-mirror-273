from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(abbreviation="frontdoor", query_term="azure")
        self.asn_patterns = [
            "azure",
            "microsoft",
        ]
        self.cname_suffixes = [
            ".azurefd.net",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

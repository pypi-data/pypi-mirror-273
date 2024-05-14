from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="alibaba-waf",
        )
        self.asn_patterns = [
            "alibaba",
            "taobao",
        ]
        self.cname_suffixes = [
            ".yundunwaf1.com",
            ".yundunwaf2.com",
            ".yundunwaf3.com",
            ".yundunwaf4.com",
            ".yundunwaf5.com",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

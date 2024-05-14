from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="wangsu",
        )
        self.asn_patterns = [
            "wangsu",
        ]
        self.cname_suffixes = [
            ".lxdns.com",
            ".wscdns.com",
            ".wscvip.cn",
            ".wscvip.com",
            ".wsdvs.com",
            ".wsglb0.cn",
            ".wsglb0.com",
            ".wsssec.com",
            ".wswebpic.com",
            ".cdn20.com",
            ".cdn30.com",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

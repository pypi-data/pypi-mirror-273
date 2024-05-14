from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="tencent",
        )
        self.asn_patterns = [
            "tencent",
        ]
        self.cname_suffixes = [
            ".dsa.dnsv1.com",
            ".dsa.dnsv1.com.cn",
            ".cdn.dnsv1.com",
            ".cdn.dnsv1.com.cn",
            ".eo.dnse0.com",
            ".eo.dnse1.com",
            ".eo.dnse2.com",
            ".eo.dnse3.com",
            ".eo.dnse4.com",
            ".eo.dnse5.com",
            ".cdn.qcloudcdn.cn",
            ".txlivecdn.com",
            ".ovscdns.com",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

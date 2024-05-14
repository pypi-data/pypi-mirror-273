from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="alibaba-dcdn",
        )
        self.asn_patterns = [
            "alibaba",
            "taobao",
        ]
        self.cname_suffixes = [
            ".m.alikunlun.com",
            ".w.kunlunaq.com",
            ".w.kunlunar.com",
            ".w.kunlunca.com",
            ".w.kunluncan.com",
            ".w.kunlunea.com",
            ".w.kunlungem.com",
            ".w.kunlungr.com",
            ".w.kunlunhuf.com",
            ".w.kunlunle.com",
            ".w.kunlunno.com",
            ".w.kunlunpi.com",
            ".w.kunlunsl.com",
            ".w.kunlunso.com",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

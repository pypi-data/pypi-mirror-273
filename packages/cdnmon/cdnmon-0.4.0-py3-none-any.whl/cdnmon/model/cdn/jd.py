from cdnmon.model.cdn import AbstractBGPViewCDN


class CDN(AbstractBGPViewCDN):
    def __init__(self):
        super(CDN, self).__init__(
            abbreviation="jd",
        )
        self.asn_patterns = [
            "jingdong",
        ]
        self.cname_suffixes = [
            ".dy.galileo.jcloud-cdn.com",
            ".cdn.jcloudcdn.com",
            ".jcloudcache.com",
            ".cdn.jcloudcache.com",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

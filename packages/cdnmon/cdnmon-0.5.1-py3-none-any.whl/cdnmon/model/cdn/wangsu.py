from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="wangsu",
    asn_patterns=["wangsu"],
    cname_suffixes=[
        CNAMEPattern(suffix=".lxdns.com", pattern=r"${domain}.lxdns.com"),
        CNAMEPattern(suffix=".wscdns.com", pattern=r"${domain}.wscdns.com"),
        CNAMEPattern(suffix=".wscvip.cn", pattern=r"${domain}.wscvip.cn"),
        CNAMEPattern(suffix=".wscvip.com", pattern=r"${domain}.wscvip.com"),
        CNAMEPattern(suffix=".wsdvs.com", pattern=r"${domain}.wsdvs.com"),
        CNAMEPattern(suffix=".wsglb0.cn", pattern=r"${domain}.wsglb0.cn"),
        CNAMEPattern(suffix=".wsglb0.com", pattern=r"${domain}.wsglb0.com"),
        CNAMEPattern(suffix=".wsssec.com", pattern=r"${domain}.wsssec.com"),
        CNAMEPattern(suffix=".wswebpic.com", pattern=r"${domain}.wswebpic.com"),
        CNAMEPattern(suffix=".cdn20.com"),
        CNAMEPattern(suffix=".cdn30.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["wangsu"]),
)

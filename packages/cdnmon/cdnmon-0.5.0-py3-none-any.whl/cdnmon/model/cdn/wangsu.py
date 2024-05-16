from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="wangsu",
    asn_patterns=["wangsu"],
    cname_suffixes=[
        CNAMEPattern(suffix=".lxdns.com"),
        CNAMEPattern(suffix=".wscdns.com"),
        CNAMEPattern(suffix=".wscvip.cn"),
        CNAMEPattern(suffix=".wscvip.com"),
        CNAMEPattern(suffix=".wsdvs.com"),
        CNAMEPattern(suffix=".wsglb0.cn"),
        CNAMEPattern(suffix=".wsglb0.com"),
        CNAMEPattern(suffix=".wsssec.com"),
        CNAMEPattern(suffix=".wswebpic.com"),
        CNAMEPattern(suffix=".cdn20.com"),
        CNAMEPattern(suffix=".cdn30.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["wangsu"]),
)

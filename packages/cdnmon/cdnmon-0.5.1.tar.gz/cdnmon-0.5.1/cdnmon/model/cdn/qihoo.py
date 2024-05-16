from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="qihoo",
    asn_patterns=["qihoo"],
    cname_suffixes=[
        CNAMEPattern(suffix=".360qhcdn.com", pattern=r"${domain}.360qhcdn.com"),
        CNAMEPattern(suffix=".qhcdn-lb.com", pattern=r"${domain}.qhcdn-lb.com"),
        CNAMEPattern(suffix=".qhcdn.com", pattern=r"${domain}.qhcdn.com"),
        CNAMEPattern(suffix=".360imgcdn.com", pattern=r"${domain}.360imgcdn.com"),
        CNAMEPattern(suffix=".qhdlcdn.com", pattern=r"${domain}.qhdlcdn.com"),
        CNAMEPattern(suffix=".qh-cdn.com", pattern=r"${domain}.qh-cdn.com"),
        CNAMEPattern(suffix=".360dlcdn.com", pattern=r"${domain}.360dlcdn.com"),
        CNAMEPattern(suffix=".360tpcdn.com", pattern=r"${domain}.360tpcdn.com"),
    ],
    cidr=BGPViewCIDR(["qihoo"]),
)

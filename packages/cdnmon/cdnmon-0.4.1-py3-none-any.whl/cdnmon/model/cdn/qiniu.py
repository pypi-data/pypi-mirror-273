from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="qiniu",
    asn_patterns=["qiniu"],
    cname_suffixes=[
        CNAMEPattern(suffix=".qiniudns.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["qiniu"]),
)

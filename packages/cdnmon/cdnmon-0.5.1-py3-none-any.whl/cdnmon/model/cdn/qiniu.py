from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="qiniu",
    asn_patterns=["qiniu"],
    cname_suffixes=[
        CNAMEPattern(suffix=".qiniudns.com", pattern=r"${dot2dash-domain}-id[0-9a-z]{5}.qiniudns.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["qiniu"]),
)

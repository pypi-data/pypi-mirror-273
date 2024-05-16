from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="volc",
    asn_patterns=["bytedance"],
    cname_suffixes=[
        CNAMEPattern(suffix=".volcgslb.com", pattern=r"${domain}.volcgslb.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["bytedance"]),
)

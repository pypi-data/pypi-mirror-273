from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="leaseweb",
    asn_patterns=["leaseweb"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(query_term_list=["leaseweb"]),
)

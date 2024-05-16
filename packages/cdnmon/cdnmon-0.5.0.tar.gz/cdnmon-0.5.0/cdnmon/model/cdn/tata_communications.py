from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="tata-communications",
    asn_patterns=["tata"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(query_term_list=["tata"]),
)

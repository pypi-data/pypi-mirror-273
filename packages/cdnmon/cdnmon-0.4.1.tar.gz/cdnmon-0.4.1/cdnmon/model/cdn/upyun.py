from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="upyun",
    asn_patterns=["youpai", "upyun"],
    cname_suffixes=[
        CNAMEPattern(suffix=".aicdn.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["youpai", "upyun"]),
)

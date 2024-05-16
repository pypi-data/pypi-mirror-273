from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="upyun",
    asn_patterns=["youpai", "upyun"],
    cname_suffixes=[
        CNAMEPattern(suffix=".aicdn.com", pattern=r"[0-9a-f]{12}.b0.aicdn.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["youpai", "upyun"]),
)

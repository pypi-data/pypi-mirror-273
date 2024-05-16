from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="ucloud",
    asn_patterns=["ucloud"],
    cname_suffixes=[
        CNAMEPattern(suffix=".ucloud.com.cn", pattern=r"${domain}.ucloud.com.cn"),
        CNAMEPattern(suffix=".ucloudnaming.cn", pattern=r"${domain}.ucloudnaming.cn"),
        CNAMEPattern(suffix=".ucloudnaming.info", pattern=r"${domain}.ucloudnaming.info"),
        CNAMEPattern(suffix=".ugslb.net", pattern=r"${domain}.ugslb.net"),
    ],
    cidr=BGPViewCIDR(query_term_list=["ucloud"]),
)

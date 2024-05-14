import ipaddress
import requests
from cdnmon.util.cidr import deduplicate_networks


class BGPViewClient:
    @staticmethod
    def extract(query_term):
        """
        [1] https://bgpview.docs.apiary.io/#reference/0/asn-prefixes/view-asn-prefixes
        [2] https://api.bgpview.io/search
        [3] https://api.bgpview.io/search?query_term=tencent
        """
        url = f"https://bgpview.execve.workers.dev/search?query_term={query_term}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        print(response.status_code)
        print(response.headers)
        print(response.text)
        print(response.content)
        print(response.json())
        return response.json()

    @staticmethod
    def transform(data):
        ipv4_networks = []
        ipv6_networks = []

        for item in data["data"]["ipv4_prefixes"]:
            ipv4_networks.append(str(ipaddress.IPv4Network(item["prefix"], strict=False)))
        for item in data["data"]["ipv6_prefixes"]:
            ipv6_networks.append(str(ipaddress.IPv6Network(item["prefix"], strict=False)))

        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks),
        }


def main():
    BGPViewClient.transform(BGPViewClient.extract("alicloud"))


if __name__ == "__main__":
    main()

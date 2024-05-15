import functools

import requests


class BGPViewClient:
    @staticmethod
    @functools.lru_cache(maxsize=None)
    def search(query_term: str):
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
        print(f"GET {url} {response.status_code}")
        print(response.json())
        return response.json()


def main():
    BGPViewClient.transform(BGPViewClient.search("alicloud"))


if __name__ == "__main__":
    main()

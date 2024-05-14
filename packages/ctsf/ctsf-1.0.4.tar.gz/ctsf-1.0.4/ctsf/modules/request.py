import re
import requests

version = "1.0.4"  # can i change this in setup.py?


def banner():
    banner = """
.------..------..------..------.
|C.--. ||T.--. ||F.--. ||S.--. |
| :/\: || :/\: || :(): || :/\: |
| :\/: || (__) || ()() || :\/: |
| '--'C|| '--'T|| '--'F|| '--'S|
`------'`------'`------'`------'
	Version: {v}
	""".format(
        v=version
    )
    print(banner)


def clear_url(target):
    return re.sub(".*www\.", "", target, 1).split("/")[0].strip()


def get_request(domain):
    banner()
    subdomains = []
    target = clear_url(domain)

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

    for index, value in enumerate(req.json()):
        subdomains.extend(value["name_value"].split("\n"))

    subdomains = list(sorted(set(subdomains)))  # todo: remove duplicates

    print("=" * 32)

    for subdomain in subdomains:
        print("[+] :: {s}".format(s=subdomain))

    print("=" * 32)

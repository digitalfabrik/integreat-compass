#!/usr/bin/env python3

import argparse
import mimetypes
import os

import requests


def main():
    """
    Create a GitHub release
    """

    parser = argparse.ArgumentParser(description="Create GitHub release")
    parser.add_argument(
        "-p", "--prerelease", action="store_true", help="mark the release as prerelease"
    )
    parser.add_argument("token", metavar="TOKEN", help="GitHub API token")
    parser.add_argument("tag", metavar="TAG", help="tag for the release")
    parser.add_argument(
        "prev_tag", metavar="PREV_TAG", help="the previous tag of the release"
    )
    parser.add_argument(
        "contributors", metavar="CONTRIBUTORS", help="contributors of the release"
    )
    parser.add_argument(
        "assets", metavar="ASSET", help="uploadable asset file", nargs="*"
    )
    args = parser.parse_args()

    logo_url = "https://raw.githubusercontent.com/digitalfabrik/integreat-compass/main/.github/logo.png"
    compare_url = "https://github.com/digitalfabrik/integreat-compass/compare"
    body = (
        f"### ![]({logo_url}) integreat-compass `{args.tag}`"
        f"\n\nCompare changes: [{args.prev_tag} → {args.tag}]({compare_url}/{args.prev_tag}...{args.tag})"
        f"\n\n### Contributors\n\n{args.contributors}"
    )

    response = requests.post(
        "https://api.github.com/repos/digitalfabrik/integreat-compass/releases",
        json={
            "tag_name": args.tag,
            "name": args.tag,
            "body": body,
            "prerelease": args.prerelease,
        },
        headers={"Authorization": f"token {args.token}"},
        timeout=60,
    )
    release = response.json()
    print(f"Created a new release {release['name']}")

    # Upload_url is given in uri-template form.
    upload_url, _, _ = release["upload_url"].partition("{")
    print("Upload url: %r", upload_url)

    for filename in args.assets:
        with open(filename, "rb") as file:
            response = requests.post(
                upload_url,
                data=file,
                params={
                    "name": os.path.basename(filename),
                    "label": "integreat-compass",
                },
                headers={
                    "Authorization": f"token {args.token}",
                    "Content-Type": (
                        mimetypes.guess_type(filename)[0] or "application/octet-stream"
                    ),
                },
                timeout=60,
            )
        print(f"Uploaded asset {filename}")


if __name__ == "__main__":
    main()

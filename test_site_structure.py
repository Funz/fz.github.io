"""Check that the built site (mkdocs build) contains every page of the navigation."""
import sys
from pathlib import Path

import yaml


class _Loader(yaml.SafeLoader):
    pass


# mkdocs.yml uses !!python/name tags (emoji, mermaid fences): accept them as strings
_Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)


def nav_pages(nav):
    for item in nav:
        if isinstance(item, str):
            yield item
        elif isinstance(item, dict):
            for value in item.values():
                if isinstance(value, str):
                    yield value
                else:
                    yield from nav_pages(value)


def main():
    config = yaml.load(Path("mkdocs.yml").read_text(), Loader=_Loader)
    missing = []
    for page in nav_pages(config["nav"]):
        html = Path("site") / (page[:-3] + "/index.html" if not page.endswith("index.md") else page[:-3] + ".html")
        if not html.exists():
            missing.append(str(html))
    redirects = next(p["redirects"]["redirect_maps"] for p in config["plugins"]
                     if isinstance(p, dict) and "redirects" in p)
    for old in redirects:
        html = Path("site") / (old[:-3] + "/index.html")
        if not html.exists():
            missing.append(str(html))
    if missing:
        print("Missing pages:\n  " + "\n  ".join(missing))
        return 1
    print(f"OK: {len(list(nav_pages(config['nav'])))} navigation pages and {len(redirects)} redirects built")
    return 0


if __name__ == "__main__":
    sys.exit(main())

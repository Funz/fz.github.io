import os
from pathlib import Path

# Check key pages exist
key_pages = [
    'site/index.html',
    'site/getting-started/installation/index.html',
    'site/getting-started/quickstart/index.html',
    'site/user-guide/core-functions/fzr/index.html',
    'site/plugins/index.html',
    'site/examples/perfectgas/index.html',
    'site/examples/colab/index.html'
]

print("Checking documentation structure...")
all_exist = True
for page in key_pages:
    exists = os.path.exists(page)
    status = "✓" if exists else "✗"
    print(f"{status} {page}")
    if not exists:
        all_exist = False

if all_exist:
    print("\n✓ All key pages built successfully!")
else:
    print("\n✗ Some pages are missing")

# Count total pages
html_files = list(Path('site').rglob('*.html'))
print(f"\nTotal HTML pages: {len(html_files)}")

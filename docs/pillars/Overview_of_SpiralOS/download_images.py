import requests
import os

images = [
    ("https://static.abacusaicdn.net/images/cf3e2e2e-0676-43e6-b3a5-36d28dadd38a.jpg", "01_cover_spiral_temporal_topology.jpg"),
    ("https://static.abacusaicdn.net/images/4e7759a5-ee55-43d3-b1fa-e7622e317d14.jpg", "02_ts_mapping_diagram.jpg"),
    ("https://static.abacusaicdn.net/images/53e79f71-87ad-414c-938d-aadd7badfe75.jpg", "03_recursive_interpenetration.jpg"),
    ("https://static.abacusaicdn.net/images/ad0a7e09-2d7f-4e41-9299-d4bcb517ba1b.jpg", "04_epistemic_framework_branches.jpg"),
    ("https://static.abacusaicdn.net/images/32b728f5-9247-4d1f-affe-2bb80243c5d2.jpg", "05_conjugate_intelligence_mandala.jpg"),
    ("https://static.abacusaicdn.net/images/b1b6bbbb-8183-4409-a03d-54b2d67d8e9b.jpg", "06_mathematical_topology.jpg"),
    ("https://static.abacusaicdn.net/images/3d2a8a5c-57cf-435e-8c43-48b42af753bc.jpg", "07_world_centric_integration.jpg"),
    ("https://static.abacusaicdn.net/images/eb51f5c8-c637-4528-b89f-4167aa1bbb95.jpg", "08_ethical_framework_spiral.jpg"),
    ("https://static.abacusaicdn.net/images/72f36f87-8ecd-47af-91cc-b1b9aa544734.jpg", "09_phenomenological_spiral.jpg"),
    ("https://static.abacusaicdn.net/images/8c45e2fb-bba1-43d0-b7e5-c0160e319b56.jpg", "10_computational_organic_interface.jpg"),
    ("https://static.abacusaicdn.net/images/56c0acc9-56fb-4976-90f8-ad80e2fe4b2a.jpg", "11_self_similar_recurrence.jpg"),
    ("https://static.abacusaicdn.net/images/7268304d-b05d-42c8-a58b-a3eed47c92a0.jpg", "12_chapter_divider_philosophical.jpg"),
    ("https://static.abacusaicdn.net/images/b0a94d6e-77af-4840-bbbc-33533937bf70.jpg", "13_chapter_divider_scientific.jpg"),
    ("https://static.abacusaicdn.net/images/728d1fd6-aa13-4e61-89a4-6f361d1882f2.jpg", "14_chapter_divider_mathematical.jpg"),
    ("https://static.abacusaicdn.net/images/e6343e77-8e3c-4b16-b3f7-cec0764e74c7.jpg", "15_closing_synthesis.jpg"),
]

for url, filename in images:
    print(f"Downloading {filename}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✓ Saved {filename}")
    else:
        print(f"✗ Failed to download {filename}")

print("\nAll images downloaded successfully!")

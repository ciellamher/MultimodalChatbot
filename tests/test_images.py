import os
from src.image_bot import describe_image

# Use the absolute path or relative path to your existing assets
ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')

def test_cat_image():
    # Make sure cat.jpg exists in tests/assets/
    img_path = os.path.join(ASSET_DIR, "cat.jpg")
    if os.path.exists(img_path):
        result = describe_image(img_path)
        # Check if it identifies it as a cat or animal
        assert "cat" in result.lower() or "tabby" in result.lower() or "siamese" in result.lower()

def test_missing_file():
    # This should return a graceful error, not crash
    result = describe_image("ghost_file.jpg")
    assert "Could not read image" in result
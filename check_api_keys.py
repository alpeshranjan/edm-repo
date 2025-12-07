#!/usr/bin/env python3
"""Check API keys configuration"""

from src.utils.config import Config

print("=" * 50)
print("API Keys Configuration Check")
print("=" * 50)
print()

# Check ACRCloud
print("ACRCloud API:")
acr_access = Config.ACRCLOUD_ACCESS_KEY
acr_secret = Config.ACRCLOUD_SECRET_KEY

if acr_access and acr_access != "your_access_key_here":
    print(f"  ✓ Access Key: SET (length: {len(acr_access)} chars)")
    print(f"    Preview: {acr_access[:10]}...{acr_access[-5:]}")
else:
    print("  ✗ Access Key: NOT SET or using placeholder")

if acr_secret and acr_secret != "your_secret_key_here":
    print(f"  ✓ Secret Key: SET (length: {len(acr_secret)} chars)")
    print(f"    Preview: {acr_secret[:10]}...{acr_secret[-5:]}")
else:
    print("  ✗ Secret Key: NOT SET or using placeholder")

print()

# Check Audd.io
print("Audd.io API:")
audd_token = Config.AUDD_API_TOKEN

if audd_token and audd_token != "your_api_token_here":
    print(f"  ✓ API Token: SET (length: {len(audd_token)} chars)")
    print(f"    Preview: {audd_token[:10]}...{audd_token[-5:]}")
else:
    print("  ✗ API Token: NOT SET or using placeholder (optional)")

print()

# Validate
print("Validation:")
is_valid, errors = Config.validate()
if is_valid:
    print("  ✓ Configuration is valid - ready to use!")
else:
    print("  ✗ Configuration has errors:")
    for error in errors:
        print(f"    - {error}")

print()
print("=" * 50)

# Test recognizers
print("\nRecognizer Availability:")
from src.recognizers.acrcloud import ACRCloudRecognizer
from src.recognizers.audd import AuddRecognizer

acr = ACRCloudRecognizer()
audd = AuddRecognizer()

print(f"  ACRCloud: {'✓ Available' if acr.is_available() else '✗ Not available'}")
print(f"  Audd.io:  {'✓ Available' if audd.is_available() else '✗ Not available'}")

if not acr.is_available() and not audd.is_available():
    print("\n⚠️  WARNING: No recognition APIs are available!")
    print("   You need to set at least ACRCloud API keys in .env file")


# Simple solution for MongoDB TLS issues
# 
# Your MongoDB connection is failing because of TLS handshake errors.
# This happens when your network (corporate firewall, antivirus, etc.) 
# interferes with TLS connections to MongoDB Atlas.
#
# SOLUTION OPTIONS:
#
# 1. BYPASS TLS VERIFICATION (DEVELOPMENT ONLY):
#    Set environment variable before starting your server:
#    $env:MONGODB_INSECURE="true"
#    uvicorn app.__main__:app --reload
#
# 2. USE DIFFERENT NETWORK:
#    Try connecting from mobile hotspot or different network
#
# 3. CHECK CORPORATE FIREWALL:
#    If on corporate network, ask IT to whitelist *.mongodb.net:27017
#
# 4. TRY NON-SRV CONNECTION STRING:
#    In MongoDB Atlas, copy the "Standard connection string" 
#    instead of the +srv version

import os

print("MongoDB Connection Troubleshooting")
print("=" * 50)

# Check current environment
mongodb_url = os.getenv("MONGODB_URL")
skip_db = os.getenv("SKIP_DB") 
insecure = os.getenv("MONGODB_INSECURE")

print(f"MONGODB_URL set: {'Yes' if mongodb_url else 'No'}")
print(f"SKIP_DB set: {skip_db}")
print(f"MONGODB_INSECURE set: {insecure}")

print("\nTo start server with TLS bypass (DEV ONLY):")
print("$env:MONGODB_INSECURE='true'")
print("$env:MONGODB_URL='your_connection_string'")
print("uvicorn app.__main__:app --reload")

print("\nTo start server without database:")
print("$env:SKIP_DB='true'")
print("uvicorn app.__main__:app --reload")
import certifi
import os
from pymongo import MongoClient

# Read URI from environment if set, otherwise fallback to example
env_uri = os.getenv('MONGODB_URL')
if env_uri:
    uri = env_uri
else:
    uri = "mongodb+srv://apalak966_db_user:CvWZx3ICMf80PtsB@cluster0.reorq1w.mongodb.net/99acres_db?retryWrites=true&w=majority&appName=Cluster0"

# Redact password for printing
redacted = uri
# crude redact attempt - do not expose password in logs
if '@' in uri:
    parts = uri.split('@')
    left = parts[0]
    if ':' in left:
        left_parts = left.split(':')
        left_parts[-1] = '<REDACTED>'
        redacted = ':'.join(left_parts) + '@' + parts[1]

print("URI (redacted):", redacted)

client = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=10000)
try:
    print('Ping:', client.admin.command('ping'))
except Exception as e:
    import traceback
    traceback.print_exc()
    print('Connection error type:', type(e).__name__, '->', e)

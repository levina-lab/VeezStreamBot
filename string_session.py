
#only for new users who are facing problem, program session generator
#use this only if you are facing problem

from pyrogram import Client as c

API_ID = input("\nEnter Your API_ID:\n > ")
API_HASH = input("\nEnter Your API_HASH:\n > ")

print("\n\n Enter Phone number when asked.\n\n")

i = c(":memory:", api_id=API_ID, api_hash=API_HASH)

with i:
    i.storage.SESSION_STRING_FORMAT=">B?256sQ?"
    ss = i.export_session_string()
    print(f"here is your program session")
    print(f"\n{ss}\n")
    

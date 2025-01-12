from supabase import create_client

url = "https://lynonbmmglvpivolqyrw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx5bm9uYm1tZ2x2cGl2b2xxeXJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUzNTU3MTMsImV4cCI6MjA1MDkzMTcxM30.pYR2Aquu9zmWUSPUt5g5nXvoV1DD2Ba8L7Jh7P7XFWQ"
supabase = create_client(url, key)
uid ="kJRoumGMSsfUKLoxkUqv8kL6YCn2"
name = "rafsi"
def ali(uid, name):
    response = supabase.table("contacts_data").select("email").eq("uid", uid).eq("name", name).execute()

    result=response.data
    contacts = result

    for contact in contacts:
        pass
    test = contact['email']
    
    return test

ali(uid,name)


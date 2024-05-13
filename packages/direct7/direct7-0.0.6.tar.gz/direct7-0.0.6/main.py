from direct7 import Client

if __name__ == "__main__":
    client = Client(api_token="Your API Token")

result = client.whatsapp.send_whatsapp_freeform_message(originator="XXXXXXXXXXX", recipient=["XXXXXXXXXXX", "XXXXXXXXXXXXX"], message_type="CONTACTS", first_name="Amal", last_name="Anu", formatted_name="Amal Anu", phones=["918086757074", "917306445534"], emails = ["amal@gmail.com", "amal@gmail1.com"])
print(result)

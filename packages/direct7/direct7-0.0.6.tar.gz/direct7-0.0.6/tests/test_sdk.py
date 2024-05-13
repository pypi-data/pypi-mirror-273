from src.direct7 import Client

client = Client(
    api_token='Your API Token')


def test_send_messages():
    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="9181XXXXXXXX",
                                                                            recipient="9190XXXXXXXX",
                                                                            message_type="CONTACTS", first_name="Amal",
                                                                            last_name="Anu", formatted_name="Amal Anu",
                                                                            phones=["9181XXXXXXXX", "9181XXXXXXXX"],
                                                                            emails=["amal@gmail.com",
                                                                                    "amal@gmail1.com"])

    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="XXXXXXXXXX",
                                                                            recipient="XXXXXXXXXXXXX",
                                                                            message_type="TEXT", body="Hi")

    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="XXXXXXXXXXXXX",
                                                                            recipients="XXXXXXXXXXXXX",
                                                                            message_type="ATTACHMENT", type="image",
                                                                            url="https://upload.wikimedia.org",
                                                                            caption="Tet")

    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="XXXXXXXXXXX",
                                                                            recipient="XXXXXXXXXXXXX",
                                                                            message_type="LOCATION", latitude="12.93803129081362",
                                                                            longitude="77.61088653615994",
                                                                            name="Mobile Pvt Ltd", address="30, Hosur Rd, 7th Block, Koramangala, Bengaluru, Karnataka 560095")

    response_send_messages = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXX",
                                                                             recipient="XXXXXXXXXXXXX",
                                                                             template_id="limited_time_offer",
                                                                             media_type="image", media_url="https://upload.wikimedia.org",
                                                                             lto_expiration_time_ms="1708804800000",
                                                                             coupon_code="DWS44")
    actions = [
        {
            "action_type": "url",
            "action_index": "0",
            "action_payload": "dashboard"
        }
    ]

    response_send_messages = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXX",
                                                                             recipient="XXXXXXXXXXXXX",
                                                                             template_id="click_me",
                                                                             actions=actions)

    cards = [
        {
            "card_index": "0",
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "link": "https://miro.medium.com/max/780/1*9Wdo1PuiJTZo0Du2A9JLQQ.jpeg"
                            }
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "quick_reply",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "payload",
                            "payload": "2259NqSd"
                        }
                    ]
                }
            ]
        },
        {
            "card_index": "1",
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "link": "https://www.selfdrive.ae/banner_image/desktop/21112023164328_409449002729.jpg"
                            }
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "quick_reply",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "payload",
                            "payload": "59NqSdd"
                        }
                    ]
                }
            ]
        }
    ]

    response_send_messages = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXX",
                                                                             recipient="XXXXXXXXXXXXX",
                                                                             template_id="carousel_card",
                                                                             carousel_cards=cards)

    print(response_send_messages)
    assert response_send_messages is not None
    assert response_send_messages

def test_get_status():
    response_get_status = client.sms.get_status(request_id="00152e17-1717-4568-b793-bd6c729c1ff3")
    print(response_get_status)
    assert response_get_status is not None
    assert response_get_status

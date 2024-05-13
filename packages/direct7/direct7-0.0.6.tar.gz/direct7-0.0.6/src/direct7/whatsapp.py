import logging

log = logging.getLogger(__name__)


class WHATSAPP:

    def __init__(self, client):
        self._client = client

    def send_whatsapp_freeform_message(self, originator: str, recipient: str, message_type: str, first_name: str = None,
                                       last_name: str = None, formatted_name: str = None, birthday: str = None,
                                       phones: list = None,
                                       emails: list = None, urls: list = None, latitude: str = None,
                                       longitude: str = None,
                                       name: str = None, address: str = None,
                                       type: str = None, url: str = None, caption: str = None, body: str = None):
        """
        Send a WhatsApp message to a single/multiple recipients.
        :param originator: str - The message originator.
        :param recipient: str - The message recipient.
        :param message_type: str - The type of message ("CONTACTS", "LOCATION", "ATTACHMENT", "TEXT").
        :param first_name: str - First name for "CONTACTS" message type.
        :param last_name: str - Last name for "CONTACTS" message type.
        :param formatted_name: str - Display name for "CONTACTS" message type.
        :param phones: list - Phone number for "CONTACTS" message type.
        :param emails: list - Email address for "CONTACTS" message type.
        :param urls: list - URL for "CONTACTS" message type.
        :param latitude: str - Latitude for "LOCATION" message type.
        :param longitude: str - Longitude for "LOCATION" message type.
        :param name: str - Location name for "LOCATION" message type.
        :param address: str - Location address for "LOCATION" message type.
        :param type: str - Attachment type for "ATTACHMENT" message type.
        :param url: str - Attachment URL for "ATTACHMENT" message type.
        :param caption: str - Attachment caption for "ATTACHMENT" message type.
        :param body: str - Message text for "TEXT" message type.
        """
        message = {
            "originator": originator,
            "recipients": [{"recipient": recipient}],
            "content": {
                "message_type": message_type
            }
        }

        if message_type == "CONTACTS":
            message["content"]["contacts"] = [{
                "name": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "formatted_name": formatted_name,
                },
                "birthday": birthday,
                "phones": [{"phone": phone} for phone in phones] if phones else None,
                "emails": [{"email": email} for email in emails] if emails else None,
                "urls": [{"url": url} for url in urls if urls] if urls else None
            }]
        elif message_type == "LOCATION":
            message["content"]["location"] = {
                "latitude": latitude,
                "longitude": longitude,
                "name": name,
                "address": address
            }
        elif message_type == "ATTACHMENT":
            message["content"]["attachment"] = {
                "type": type,
                "url": url,
                "caption": caption
            }
        elif message_type == "TEXT":
            message["content"]["text"] = {
                "body": body
            }

        response = self._client.post(
            self._client.host(), "/whatsapp/v2/send", params={"messages": [message]})
        log.info("Message sent successfully.")
        return response

    def send_whatsapp_templated_message(self, originator: str, recipient: str, template_id: str,
                                        body_parameter_values: dict = {}, media_type: str = None,
                                        media_url: str = None,
                                        latitude: str = None, longitude: str = None, location_name: str = None,
                                        location_address: str = None, lto_expiration_time_ms: str = None,
                                        coupon_code: str = None, quick_replies: dict = None, actions: dict = None, carousel_cards: list = []):
        """
        Send a WhatsApp message to a single/multiple recipients.
        :param originator: str - The message originator.
        :param recipient: str - The message recipient.
        :param template_id: str - The template ID for text messages.
        :param body_parameter_values: dict - The body parameter values for text templates.
        :param media_type: str - The type of media (e.g., "image", "video").
        :param media_url: str - The URL of the media content.
        """
        message = {
            "originator": originator,
            "recipients": [{"recipient": recipient}],
            "content": {
                "message_type": "TEMPLATE",
                "template": {"template_id": template_id, "body_parameter_values": body_parameter_values}
            }
        }

        if media_type:
            if media_type == "location":
                message["content"]["template"]["media"] = {
                    "media_type": "location",
                    "location": {
                        "latitude": latitude,
                        "longitude": longitude,
                        "name": location_name,
                        "address": location_address
                    }
                }
            else:
                message["content"]["template"]["media"] = {
                    "media_type": media_type, "media_url": media_url}
        if lto_expiration_time_ms:
            message["content"]["template"]["limited_time_offer"] = {
                "expiration_time_ms": lto_expiration_time_ms
            }
        if coupon_code:
            message["content"]["template"]["buttons"] = {
                "coupon_code": [
                    {
                        "index": 0,
                        "type": "copy_code",
                        "coupon_code": coupon_code
                    }
                ]
            }
        if actions:
            message["content"]["template"]["buttons"] = {
                "actions": actions
            }

        if quick_replies:
            message["content"]["template"]["buttons"] = {
                "quick_replies": quick_replies
            }

        if carousel_cards:
            message["content"]["template"]["carousel"] = {
                "cards": carousel_cards
            }

        response = self._client.post(
            self._client.host(), "/whatsapp/v2/send", params={"messages": [message]})
        log.info("Message sent successfully.")
        return response

    def get_status(self, request_id: str):
        """
        Get the status for a whatsapp message request.
        :param params:
        request_id : str - The request ID of the whatsapp message request.
        :return:
        """
        response = self._client.get(
            self._client.host(),
            f"/whatsapp/v1/report/{request_id}"
        )
        log.info("Message status retrieved successfully.")
        return response

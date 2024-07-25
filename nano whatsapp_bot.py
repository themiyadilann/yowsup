from yowsup.stacks import YowStackBuilder
from yowsup.layers.auth import AuthError
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            message_text = messageProtocolEntity.getBody().lower()
            sender = messageProtocolEntity.getFrom()

            # List of links to be deleted
            banned_links = ["wa.me", "chat.whatsapp.com", "whatsapp.com"]

            # Check if the message contains any banned link
            if any(link in message_text for link in banned_links):
                # Delete the message (You need to be the admin to delete messages)
                self.toLower(messageProtocolEntity.ack())

                # Send notification to the group
                notification_message = f"@{sender} (*No link available...*)"
                notification = TextMessageProtocolEntity(notification_message, to=messageProtocolEntity.getFrom())
                self.toLower(notification)

                print(f"Deleted a message with a link from {sender}")

if __name__ == "__main__":
    credentials = ("your_phone_number", "your_password")  # Replace with your phone number and password
    stackBuilder = YowStackBuilder()

    stack = stackBuilder\
        .pushDefaultLayers()\
        .push(EchoLayer)\
        .build()

    stack.setCredentials(credentials)

    try:
        stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        stack.loop()
    except AuthError as e:
        print("Authentication Error: %s" % e.message)
    except Exception as e:
        print("Error: %s" % e.message)

from twilio.rest import Client
import info

client = Client(info.account_sid, info.auth_token)



message = client.messages \
                .create(
                     body="Thank you for visiting our branch",
                     from_= info.twilio_no,
                     to= info.targe_no
                 )

print(message.body)

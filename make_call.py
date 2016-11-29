# Download the library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Get these credentials from http://twilio.com/user/account
account_sid = "AC97fca194a21624e4e51044500f2b0258"
auth_token = "d36ada8b38931dbbbe8820af83e2c64b"
client = TwilioRestClient(account_sid, auth_token)

# Make the call
def call(number):
    call = client.calls.create(to=number,  # Any phone number
                               from_="+14123200542", # Must be a valid Twilio number
                               url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")

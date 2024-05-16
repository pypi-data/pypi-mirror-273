import enum
import os

from twilio.rest import Client
from twilio.rest.verify.v2.service.verification import VerificationInstance
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance
from twilio.twiml.messaging_response import Message


class OTPLocationEnum(enum.Enum):
    email = 1
    sms = 2
    voice = 3

    def __str__(self):
        if self == OTPLocationEnum.email:
            return "Email"
        elif self == OTPLocationEnum.sms:
            return "SMS"
        elif self == OTPLocationEnum.voice:
            return "Voice"

    def twilio_keyself(self):
        if self == OTPLocationEnum.email:
            return "email"
        elif self == OTPLocationEnum.sms:
            return "sms"
        elif self == OTPLocationEnum.voice:
            return "call"


class TwilioHelper:
    @staticmethod
    def client() -> Client:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        return client

    @staticmethod
    def request_otp(
            to: str,
            via: OTPLocationEnum
    ) -> VerificationInstance:
        service_sid = os.environ['TWILIO_SERVICE_SID']
        client = TwilioHelper.client()

        # verification_check = client.verify \
        #     .v2 \
        #     .services(service_sid) \
        #     .verification_checks \
        #     .create((to=to, code='[Code]'))

        verification = client.verify \
            .v2 \
            .services(service_sid) \
            .verifications \
            .create(to=to, channel=via.twilio_keyself())

        # print(verification.sid)

        return verification

    @staticmethod
    def verify_code(
            to: str,
            code: str
    ) -> VerificationCheckInstance:
        service_sid = os.environ['TWILIO_SERVICE_SID']
        client = TwilioHelper.client()

        verification_check = client.verify \
            .v2 \
            .services(service_sid) \
            .verification_checks \
            .create(to=to, code=code)

        # print(verification_check.status)

        return verification_check

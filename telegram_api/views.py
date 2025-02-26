import asyncio
import os

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from telethon import TelegramClient
import re


class BookingSerializer(serializers.Serializer):
    tel_no = serializers.CharField(max_length=12)
    contact_name = serializers.CharField(max_length=50)
    message = serializers.CharField()
    booking_date = serializers.CharField()


API_ID = '29918269'
API_HASH = '579466851815e58e0d2e82e9a8f7cbbf'
PHONE = '+380 93 615 54 05'
MASTER_NO = os.environ.get("MASTER_NO")
# MASTER_NO = "@pacan_na_million"


def format_tel_no(phone: str) -> str:
    phone = re.sub(r'\D', '', phone)

    if phone.startswith('38'):
        phone = '+38' + phone[2:]
    elif phone.startswith('0'):
        phone = '+380' + phone[1:]
    elif len(phone) == 9:
        phone = '+380' + phone

    return phone


class NotifyAPI(APIView):
    async def send_message(self, tel_no, contact_name, message, booking_date):
        client = TelegramClient('guvesi_pavlo', API_ID, API_HASH)
        await client.start(PHONE)
        await client.send_message(
            MASTER_NO,
            f"""
            <b><u>{contact_name}</u></b>
            {tel_no}
            дата: <i>{booking_date}</i>
            <blockquote> {message} <blockquote/>     
            """,
            parse_mode='html'
        )
        await client.disconnect()

    def post(self, request):
        client_data = BookingSerializer( data=request.data )
        client_data.is_valid( raise_exception=True )

        asyncio.run(self.send_message(
            tel_no = format_tel_no( client_data.data['tel_no'] ),
            contact_name = client_data.data['contact_name'],
            message = client_data.data['message'],
            booking_date = client_data.data['booking_date']
        ))
        return Response(
            status=status.HTTP_200_OK,
            data={"message" : f"Запрос на запись доставлен мастеру!"}
        )

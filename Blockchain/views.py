from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
import hashlib
from rest_framework.views import APIView

def find_hash(text: str):
    return hashlib.sha256(text.encode()).hexdigest()


def find_nonce(current_hash: str, block_number: int, previous_hash='0'):
    nonce = 1
    while True:
        exp = current_hash + str(block_number ** 2 + nonce ** 2) + previous_hash
        hash = find_hash(exp)
        if hash[:4] == '0000':
            return nonce, hash
        nonce += 1


class GenensisBlockAPI(APIView):

    def post(self, request):
        block_number = request.data.get('block_number', 1)
        hash = request.data.get('hash')
        nonce, actual_hash = find_nonce(current_hash=hash, block_number=int(block_number))

        response = {
            'block_number': block_number,
            'nonce': nonce,
            'hash': actual_hash
        }

        return Response(data=response, status=status.HTTP_200_OK)

    def get(self, request):
        nonce, hash = find_nonce(find_hash(''), 1)
        response = {
            'block_number': 1,
            'nonce': nonce,
            'data': '',
            'hash': hash
        }

        return Response(data=response, status=status.HTTP_200_OK)

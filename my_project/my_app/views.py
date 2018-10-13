"""
Create your views here.
"""
import json
import os
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # pylint: disable=unused-import


class BusinessLogic(APIView):
    """
    This is an example of adding/modifying slots using business logic, using
    """
    def post(self, request, _format=None):  # pylint: disable=unused-argument, no-self-use
        """
        Sample post request function.
        """
        
        # Perform Business Logic Here

        # return the business logic payload
        return Response(request.data)

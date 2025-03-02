from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from funds.models import Fund
from funds.serializers import FundSerializer
from funds.utils.utils import log_execution_time
from rest_framework.exceptions import NotFound
from rest_framework.throttling import UserRateThrottle

    
class FundListAPI(APIView):
    throttle_classes = [UserRateThrottle]
    @log_execution_time
    def get(self, request):
        try:
            strategy = request.GET.get("strategy", None)
            queryset = Fund.objects.all()

            if strategy:
                queryset = queryset.filter(strategy=strategy)

            if not queryset.exists():
                raise NotFound("No funds found matching the specified criteria.")

            serialized_data = FundSerializer(queryset, many=True).data
            return Response(serialized_data)

        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FundDetailAPI(APIView):
    throttle_classes = [UserRateThrottle]
    @log_execution_time
    def get(self, request, pk):
        try:
            fund = Fund.objects.get(pk=pk)
            serialized_data = FundSerializer(fund).data
            return Response(serialized_data)

        except ValueError:
            return Response({"error": "Invalid pk value."}, status=status.HTTP_400_BAD_REQUEST)
        except Fund.DoesNotExist:
            return Response({"error": "Fund not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

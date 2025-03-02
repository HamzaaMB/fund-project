from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from funds.form import FundUploadForm
from funds.models import Fund
from funds.services import handle_file_upload
from funds.utils.utils import log_execution_time
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest, JsonResponse

@log_execution_time
def upload_funds(request):
    """View for handling CSV uploads."""
    if request.method == "POST":
        form = FundUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get("csv_file")
            file_name = file.name

            upload_result = handle_file_upload(request, file, file_name)
            if isinstance(upload_result, JsonResponse): 
                return upload_result

            return redirect("fund-list")

    else:
        form = FundUploadForm()

    return render(request, "upload.html", {"form": form})


@log_execution_time
def fund_list(request):
    """View to display all funds, filtered by strategy."""
    try:
        strategy_filter = request.GET.get("strategy")
        funds = Fund.objects.all()

        if strategy_filter:
            funds = funds.filter(strategy=strategy_filter)

        total_aum = Fund.total_aum(strategy_filter)
        total_funds = funds.count()

        unique_strategies = Fund.objects.values_list("strategy", flat=True).distinct()

        return render(request, "fund_list.html", {
            "funds": funds,
            "total_aum": total_aum,
            "total_funds": total_funds,
            "strategies": unique_strategies,
        })

    except Fund.DoesNotExist:
        return HttpResponseNotFound("Funds not found for the given strategy.")
    except Exception as e:
        messages.error(request, f"An error occurred while fetching funds: {str(e)}")
        return HttpResponseServerError("An error occurred while processing your request.")


@log_execution_time
def delete_fund(request, fund_id):
    """View to delete a specific Fund."""
    try:
        fund = get_object_or_404(Fund, id=fund_id) 
        fund.delete()
        messages.success(request, "Fund deleted successfully.")
        return redirect("fund-list")
    except Fund.DoesNotExist:
        return HttpResponseNotFound(f"Fund with UUID {fund_id} not found.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the fund: {str(e)}")
        return HttpResponseBadRequest("An error occurred while deleting the fund.")

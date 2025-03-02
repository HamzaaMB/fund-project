import pandas as pd
from .models import Fund
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib import messages

# 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024  

def process_fund_csv(file, file_name):
    """Process the uploaded CSV file and create Fund objects."""
    try:
        df = pd.read_csv(file)

        required_columns = ["Name", "Strategy", "AUM (USD)", "Inception Date"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        print('missing>', missing_columns)
        
        if missing_columns:
            return JsonResponse({"error": f"Error in file, missing columns: {', '.join(missing_columns)}"}, status=400)

        funds = [
            Fund(
                name=row["Name"],
                strategy=row.get("Strategy", ""),
                aum=row["AUM (USD)"] if pd.notna(row["AUM (USD)"]) else None,
                inception_date=row["Inception Date"] if pd.notna(row["Inception Date"]) else None,
                file_name=file_name 
            )
            for _, row in df.iterrows()
        ]

        Fund.objects.bulk_create(funds)
        return None

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except pd.errors.ParserError:
        return JsonResponse({"error": "Error parsing the CSV file. Please check the file format."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=400)

def handle_file_upload(request, file, file_name):
    """Handles file upload, checks for duplicate files, and processes the CSV."""
    try:
        if not file.name.endswith('.csv'):
            return JsonResponse({"error": "The uploaded file must be a CSV."}, status=400)
        
        if file.size > MAX_FILE_SIZE:
            return JsonResponse({"error": "The file is too large. Maximum allowed size is 10MB."}, status=400)
        
        if Fund.objects.filter(file_name=file_name).exists():
            return JsonResponse({"error": "A file with this name has already been uploaded."}, status=409)

        error_response = process_fund_csv(file, file_name)
        if error_response:
            return error_response  

        messages.success(request, f"File '{file_name}' uploaded successfully!")
        return JsonResponse({"success": f"File '{file_name}' uploaded successfully!"}, status=200)

    except IntegrityError as e:
        messages.error(request, f"Database error: {str(e)}")
        return JsonResponse({"error": f"Database error: {str(e)}"}, status=400)
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=400)

"""
Lambda Function: Excel Generator
Generates Excel sheets from processed data and saves to S3
"""
import json
import os
import boto3
from datetime import datetime
from typing import Dict, Any
import io

try:
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
except ImportError:
    print("Warning: openpyxl not available, using basic Excel generation")
    openpyxl = None

s3_client = boto3.client("s3")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for Excel generation
    
    Expected SQS message format:
    {
        "data": [...],
        "filename": "report.xlsx",
        "metadata": {...}
    }
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Process each SQS record
        for record in event.get("Records", []):
            # Parse SQS message body
            message_body = json.loads(record["body"])
            
            # Extract data from message
            data = message_body.get("data", [])
            filename = message_body.get("filename", f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
            metadata = message_body.get("metadata", {})
            
            print(f"Generating Excel file: {filename}")
            print(f"Data records: {len(data)}")
            
            # Generate Excel file
            excel_buffer = generate_excel(data, metadata, filename)
            
            # Upload to S3
            s3_key = f"excel/{filename}"
            s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=s3_key,
                Body=excel_buffer.getvalue(),
                ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            
            print(f"Excel file saved to S3: {s3_key}")
            
            # Return success response
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Excel file generated successfully",
                    "filename": filename,
                    "s3_key": s3_key,
                    "s3_bucket": S3_BUCKET_NAME,
                    "records": len(data),
                }),
            }
    
    except Exception as e:
        print(f"Error generating Excel: {str(e)}")
        raise


def generate_excel(data: list, metadata: Dict[str, Any], filename: str) -> io.BytesIO:
    """
    Generate Excel file from data
    
    Args:
        data: List of data records (dicts)
        metadata: Additional metadata
        filename: Output filename
    
    Returns:
        BytesIO buffer containing Excel file
    """
    if openpyxl:
        return generate_excel_openpyxl(data, metadata, filename)
    else:
        # Fallback: Create a simple CSV-like structure
        return generate_excel_basic(data, metadata, filename)


def generate_excel_openpyxl(data: list, metadata: Dict[str, Any], filename: str) -> io.BytesIO:
    """Generate Excel using openpyxl library"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    
    if not data:
        ws["A1"] = "No data available"
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer
    
    # Get headers from first record
    headers = list(data[0].keys())
    
    # Style for header row
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # Write headers
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
    
    # Write data rows
    for row_idx, record in enumerate(data, start=2):
        for col_idx, header in enumerate(headers, start=1):
            value = record.get(header, "")
            # Convert complex types to string
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            ws.cell(row=row_idx, column=col_idx, value=value)
    
    # Auto-adjust column widths
    for col_idx, header in enumerate(headers, start=1):
        max_length = len(str(header))
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=col_idx, max_col=col_idx):
            if row[0].value:
                max_length = max(max_length, len(str(row[0].value)))
        ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = min(max_length + 2, 50)
    
    # Add metadata sheet if provided
    if metadata:
        metadata_ws = wb.create_sheet("Metadata")
        metadata_ws["A1"] = "Key"
        metadata_ws["B1"] = "Value"
        metadata_ws["A1"].fill = header_fill
        metadata_ws["A1"].font = header_font
        metadata_ws["B1"].fill = header_fill
        metadata_ws["B1"].font = header_font
        
        for row_idx, (key, value) in enumerate(metadata.items(), start=2):
            metadata_ws.cell(row=row_idx, column=1, value=key)
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            metadata_ws.cell(row=row_idx, column=2, value=value)
    
    # Save to buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer


def generate_excel_basic(data: list, metadata: Dict[str, Any], filename: str) -> io.BytesIO:
    """Basic Excel generation fallback (creates a simple structure)"""
    import csv
    
    buffer = io.BytesIO()
    
    if not data:
        buffer.write(b"No data available")
        buffer.seek(0)
        return buffer
    
    # Convert to CSV format (basic fallback)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    
    buffer.write(output.getvalue().encode("utf-8"))
    buffer.seek(0)
    return buffer


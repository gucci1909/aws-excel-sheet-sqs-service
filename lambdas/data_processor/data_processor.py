"""
Lambda Function: Data Processor
Processes incoming data and prepares it for Excel generation
"""
import json
import os
import boto3
from datetime import datetime
from typing import Dict, Any

s3_client = boto3.client("s3")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for data processing
    
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
            filename = message_body.get("filename", f"processed_data_{datetime.now().isoformat()}.xlsx")
            metadata = message_body.get("metadata", {})
            
            print(f"Processing data for file: {filename}")
            print(f"Data records: {len(data)}")
            
            # Process and validate data
            processed_data = process_data(data, metadata)
            
            # Save processed data to S3 as JSON (intermediate step)
            intermediate_key = f"processed/{filename.replace('.xlsx', '.json')}"
            s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=intermediate_key,
                Body=json.dumps(processed_data, indent=2),
                ContentType="application/json",
            )
            
            print(f"Processed data saved to S3: {intermediate_key}")
            
            # Return success response
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Data processed successfully",
                    "filename": filename,
                    "s3_key": intermediate_key,
                    "records_processed": len(processed_data),
                }),
            }
    
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise


def process_data(data: list, metadata: Dict[str, Any]) -> list:
    """
    Process and validate the incoming data
    
    Args:
        data: List of data records
        metadata: Additional metadata about the data
    
    Returns:
        Processed and validated data
    """
    processed = []
    
    for record in data:
        # Add processing timestamp
        processed_record = {
            **record,
            "processed_at": datetime.now().isoformat(),
            "processor": "data_processor_lambda",
        }
        
        # Add any metadata
        if metadata:
            processed_record["metadata"] = metadata
        
        processed.append(processed_record)
    
    return processed


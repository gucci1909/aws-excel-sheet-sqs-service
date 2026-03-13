#!/usr/bin/env python3
"""
Example script for third-party backend service ttttttttttttttˀˀˀˀˀˀˀˀo send messages This demonstrates how to trigger the SQS service from an external service
"""
import json
import boto3
import sys
from typing import Dict, Any, List

# Initialize SQS client
sqs_client = boto3.client("sqs")


def send_excel_request(
    queue_url: str,
    data: List[Dict[str, Any]],
    filename: str = None,
    metadata: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Send a message to SQS queue to trigger Excel generation
    
    Args:
        queue_url: SQS queue URL
        data: List of data records to include in Excel
        filename: Optional filename for the Excel file
        metadata: Optional metadata dictionary
    
    Returns:
        Response from SQS send_message
    """
    if filename is None:
        from datetime import datetime
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    if metadata is None:
        metadata = {}
    
    # Create message body
    message_body = {
        "data": data,
        "filename": filename,
        "metadata": {
            **metadata,
            "source": "third_party_service",
        },
    }
    
    # Send message to SQS
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message_body),
        MessageAttributes={
            "filename": {
                "StringValue": filename,
                "DataType": "String",
            },
            "record_count": {
                "StringValue": str(len(data)),
                "DataType": "Number",
            },
        },
    )
    
    print(f"Message sent successfully!")
    print(f"Message ID: {response['MessageId']}")
    print(f"Filename: {filename}")
    print(f"Records: {len(data)}")
    
    return response


def example_usage():
    """Example usage of the send_to_sqs function"""
    # Replace with your actual SQS queue URL
    # You can find this in the CDK stack outputs after deployment
    QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/excel-processing-queue"
    
    # Sample data
    sample_data = [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "score": 95},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "score": 87},
        {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "score": 92},
    ]
    
    # Sample metadata
    metadata = {
        "report_type": "user_scores",
        "generated_by": "third_party_service",
        "version": "1.0",
    }
    
    # Send message
    response = send_excel_request(
        queue_url=QUEUE_URL,
        data=sample_data,
        filename="user_scores_report.xlsx",
        metadata=metadata,
    )
    
    return response


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If queue URL provided as argument
        queue_url = sys.argv[1]
        example_usage()
    else:
        print("Usage: python send_to_sqs.py <QUEUE_URL>")
        print("\nExample:")
        print("  python send_to_sqs.py https://sqs.us-east-1.amazonaws.com/123456789012/excel-processing-queue")
        print("\nOr modify the QUEUE_URL in the script and run:")
        print("  python send_to_sqs.py")


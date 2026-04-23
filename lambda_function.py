import boto3
import time

def lambda_handler(event, context):
    glue = boto3.client("glue", region_name="us-east-1")
    athena = boto3.client("athena", region_name="us-east-1")
    
    jobs = ["etl-dim-customer", "etl-dim-track", "etl-fact-sales"]
    for job in jobs:
        glue.start_job_run(JobName=job)
        print(f"Started {job}")
    
    time.sleep(200)
    
    athena.start_query_execution(
        QueryString="MSCK REPAIR TABLE fact_sales",
        QueryExecutionContext={"Database": "chinook_dw"},
        ResultConfiguration={"OutputLocation": "s3://chinook-athena-pc/results/"}
    )
    print("MSCK REPAIR TABLE executed")
    
    return {"ok": True}

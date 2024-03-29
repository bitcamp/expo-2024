import boto3
import json
from botocore.exceptions import ClientError
from frontend.src.algorithm import *

dynamodb = boto3.client('dynamodb')
TABLENAME = "expo-dev-schedule"

def __init(self, dyn_resource):
    self.dyn_resource = dyn_resource
    self.table = None

@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    schedule = generate_schedule()

    # check to see if the table exists, delete if it does
    try:
        dynamodb.describe_table(TableName=TABLENAME)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # create table if it doesn't exist
            create_table(schedule)
        else:

            # reached if another error, raise it
            raise e
    else:
        # delete_table_entries()
        create_table(schedule)


def generate_schedule():
    # change once scheduling algorithm is created
    # example output
    schedule = [
        {
            "name": "Best Hack Ever",
            "table": "A",
            "prizes": [
                {
                    "category": "Bitcamp People's Choice"
                },
                {
                    "category": "Bloomberg Best Booty Hack",
                    "time-start": "2024-03-05T12:30:45Z",
                    "time-end": "2024-03-05T3:30:45Z"
                }
            ]
        },
    ]
    return schedule

def create_table(schedule):
    for item in schedule:
        name = item['name']
        table = item['table']
        
        prizes = []
        if "prizes" in item:
            prizes = item['prizes']
        
        final_item = {
            'name': {'S': name},
            'table': {'S': table},
            'prizes': {'L': []}
        }

        if prizes:
            for prize in prizes:
                category = prize['category']
                time_start = prize.get('time-start', "")
                time_end = prize.get('time-end', "")

                prize_item = {
                    'M': {
                        'category': {'S': category}
                    }
                }

                if time_start:
                    prize_item['M']['time-start'] = {'S': time_start}
                if time_end:
                    prize_item['M']['time-end'] = {'S': time_end}
                
                final_item['prizes']['L'].append(prize_item)

    dynamodb.put_item(
        TableName = TABLENAME,
        Item=final_item
    )


# def delete_table_entries():
#     dynamodb.delete_table(
#         TableName=TABLENAME
#     )

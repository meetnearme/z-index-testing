#!/bin/bash

export AWS_SECRET_ACCESS_KEY="test"
export AWS_ACCESS_KEY_ID="test"
export AWS_REGION="us-east-1"

# echo "start sleep"
# sleep 5
# echo "end sleep"

# # create and seed event information 
# aws dynamodb create-table --cli-input-json file://internal/database/db_seeds/create_event_table.json --endpoint-url http://dynamodb-local:8000 --region us-east-1
# echo "end create table"
# aws dynamodb list-tables --endpoint-url http://dynamodb-local:8000 --region us-east-1
# echo "end list tables"
# aws dynamodb batch-write-item --request-items file://internal/database/db_seeds/seed_event_records.json --endpoint-url http://dynamodb-local:8000 --region us-east-1
# echo "end batch write"
# aws dynamodb scan --table-name Events --endpoint-url http://dynamodb-local:8000 --region us-east-1
# echo "end scan event table"

# echo "database seed complete"

echo "Start creating database tables"


# Create Dynamodb table
aws dynamodb create-table \
    --table-name EventsTable \
    --attribute-definitions \
        AttributeName=EventType,AttributeType=S \
        AttributeName=ZOrderIndex,AttributeType=B \
    --key-schema \
        AttributeName=EventType,KeyType=HASH \
        AttributeName=ZOrderIndex,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --endpoint-url http://dynamodb-local:8000 \
    --region $AWS_REGION

echo "Dynamodb table created"

# Generate mock event data using Python script
events=$(python3 ./generate_event_data.py)

# first_event=$(echo "$events" | head -n 1)
# first_event=${events[0]}

while IFS= read -r event || [ -n "$event"]; do 
    
    # extract event attributes
    city=$(echo $event | jq -r '.city')
    name=$(echo $event | jq -r '.name')
    description=$(echo $event | jq -r '.description')
    start=$(echo $event | jq -r '.start')
    end=$(echo $event | jq -r '.end')
    lon=$(echo $event | jq -r '.lon')
    lat=$(echo $event | jq -r '.lat')
    uuid=$(echo $event | jq -r '.uuid')
    z_order_index=$(echo $event | jq -r '.z_order_index')


    jq_filter=$(cat << "EOF"
{
    "Item": {
        "EventType": {"S": $event_type},
        "ZOrderIndex": {"B": ($z_order_index|@base64)},
        "Name": {"S": $name},
        "Description": {"S": $description},
        "StartTime": {"S": $start},
        "EndTime": {"S": "$end"},
        "Longitude": {"N": $lon},
        "Latitude": {"N": $lat},
        "UUID": {"S": $uuid}
    }
}
EOF
)

    item_json=$(jq -n \
        --arg event_type "MeetNearMeEvent" \
        --arg z_order_index "$z_order_index" \
        --arg name "$name" \
        --arg description "$description" \
        --arg start "$start" \
        --arg end "$end" \
        --arg lon "$lon" \
        --arg lat "$lat" \
        --arg uuid "$uuid" \
        "$jq_filter"
    )

    aws dynamodb put-item \
        --table-name EventsTable \
        --cli-input-json "$item_json" \
        --endpoint-url http://dynamodb-local:8000 \
        --region $AWS_REGION
    
    echo "Event inserted"

done < events.json

echo "Mock evenht data inserted into DynamoDB table" 

aws dynamodb scan --table-name EventsTable --endpoint-url http://dynamodb-local:8000 --region $AWS_REGION


echo "Database seed complete"

if [ $1 == "--forever" ]
then
    echo "staying up to keep dependent services happy"
    sleep 10000
fi

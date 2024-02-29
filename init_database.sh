#!/bin/bash

export AWS_SECRET_ACCESS_KEY="test"
export AWS_ACCESS_KEY_ID="test"
export AWS_REGION="us-east-1"

# echo "database seed complete"
seed_complete_file=".seed_complete"


if [ -f "$seed_complete_file" ]; then
    echo "Seed data already loaded - skipping"
    exit 0
fi

echo "Start creating database tables"
#
# Check if drop table flag is passed 
if [ "$DROP_TABLE" = "true" ]; then
    echo "Dropping the existing Dynamodb Table"
    aws dynamodb delete-table --table-name EventsTable \
        --endpoint-url http://dynamodb-local:8000 \
        --region $AWS_REGION
fi

DB_TABLE_NAME="EventsTable"

if aws dynamodb describe-table \
    --table-name $DB_TABLE_NAME \
    --endpoint-url http://dynamodb-local:8000 \
    --region $AWS_REGION 2>/dev/null; then
    echo "DynamoDB Table: $DB_TABLE_NAME found, Skipping table creation..."
else
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
fi

echo "Dynamodb table created"

# Generate mock event data using Python script
python3 ./python_src/scripts/generate_mock_events.py

# Split items into batches of 25 for BatchWriteItems
split -l 25 events.json events.json.

# batch write function run in parallel
echo "Starting batch write..."
puts=()
batch_write() {
    echo "In batch write"
    local file="$1"

    contents=$(cat "$file")

    # echo "Contents: $contents"

    # parse JSON into array
    items=$(jq --slurp '.' <<< "$contents")

    # Initialize the RequestItems object

    # loop through array 

    while IFS= read -r item; do 
       # parse item to object
       # item_obj=$(echo "$item" | jq -c '.')

       # extract event attributes
       city=$(echo "$item" | jq -r '.city')
       name=$(echo "$item" | jq -r '.name')
       description=$(echo "$item" | jq -r '.description')
       start_time=$(echo "$item" | jq -r '.start_time')
       end_time=$(echo "$item" | jq -r '.end_time')
       lon=$(echo "$item" | jq -r '.lon')
       lat=$(echo "$item" | jq -r '.lat')
       uuid=$(echo "$item" | jq -r '.uuid')
       z_order_index=$(echo "$item" | jq -r '.z_order_index')

       # construct the PutRequest for each item
       put_request=$(jq -n --arg event_type "MeetNearMeEvent" \
           --arg city "$city" \
           --arg name "$name" \
           --arg description "$description" \
           --arg start_time "$start_time" \
           --arg end_time "$end_time" \
           --arg lon "$lon" \
           --arg lat "$lat" \
           --arg uuid "$uuid" \
           --arg z_order_index "$z_order_index" \
           '{
               "PutRequest": {
                   "Item": {
                        "EventType": {"S": $event_type},
                        "ZOrderIndex": {"B": ($z_order_index|@base64)},
                        "Name": {"S": $name},
                        "City": {"S": $city},
                        "Description": {"S": $description},
                        "StartTime": {"S": $start_time},
                        "EndTime": {"S": $end_time},
                        "Longitude": {"N": $lon},
                        "Latitude": {"N": $lat},
                        "UUID": {"S": $uuid}
                   }
               }
           }')
        
        put_request_obj=$(jq --null-input "$put_request")

        puts+=("$put_request_obj")

    done <<< "$(echo "$items" | jq -c '.[]')"


    request_json_string='{"EventsTable": []}'

    for json_item in "${puts[@]}"; do
        request_json_string="$(jq --argjson json_put_request "$json_item" '.EventsTable += [$json_put_request]' <<< "$request_json_string")"
    done

    aws dynamodb batch-write-item \
         --request-items "$request_json_string" \
         --endpoint-url http://dynamodb-local:8000 \
         --region $AWS_REGION

    # Follow section is for use with writing to file and batch requesting from file. 

    # echo "Construct request from file"
    # touch request_items.json 
    # echo "$request_json" > request_items.json 

    # request_json='{"RequestItems": {"EventsTable": []}}'

    # for json_item in "${puts[@]}"; do
    #     request_json="$(jq --argjson json_put_request "$json_item" '.RequestItems.EventsTable += [$json_put_request]' <<< "$request_json")"
    # done

    # Option for using temp file saved for later review if we need different option
    # aws dynamodb batch-write-item \
    #      --cli-input-json file://request_items.json \
    #      --endpoint-url http://dynamodb-local:8000 \
    #      --region $AWS_REGION

} 

# Run batch_write in parallel using xargs
for file in events.json.*; do 
    batch_write "$file" &
done
# file=events.json.aa
# batch_write "$file"

# wait for all processes to finish
wait

rm events.json.*
echo "Finished batch writes"


echo "Now scanning db"
aws dynamodb scan --table-name EventsTable --endpoint-url http://dynamodb-local:8000 --select "COUNT" --region $AWS_REGION
aws dynamodb scan --table-name EventsTable --endpoint-url http://dynamodb-local:8000 --region $AWS_REGION


echo "Database seed complete"
touch $seed_complete_file

if [ $1 == "--forever" ]
then
    echo "staying up to keep dependent services happy"
    sleep 10000
fi

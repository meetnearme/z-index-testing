#!/bin/bash

export AWS_SECRET_ACCESS_KEY="test"
export AWS_ACCESS_KEY_ID="test"
export AWS_REGION="us-east-1"

# export PYTHONPATH=./python_src

# echo "database seed complete"
seed_complete_file=".seed_complete"

# testing pass env vars to drop various tables if wanted
# echo "Hell var: $HELLO"
# echo "Goodbye var: $GOODBYE"

if [ -f "$seed_complete_file" ]; then
    echo "Seed data already loaded - skipping"
    exit 0
fi

echo "Start creating database tables"

echo "Creating Z Order Table"

# Setup and seeding of ZOrder table
DB_TABLE_NAME_Z_ORDER="EventsTableZOrder"

# Check if drop table flag is passed 
if [ "$DROP_TABLE_Z_ORDER" = "true" ]; then
    echo "Dropping the existing Z Order Dynamodb Table"
    aws dynamodb delete-table --table-name $DB_TABLE_NAME_Z_ORDER \
        --endpoint-url http://dynamodb-local:8000 \
        --region $AWS_REGION
fi


if aws dynamodb describe-table \
    --table-name $DB_TABLE_NAME_Z_ORDER \
    --endpoint-url http://dynamodb-local:8000 \
    --region $AWS_REGION 2>/dev/null; then
    echo "DynamoDB Table: $DB_TABLE_NAME_Z_ORDER found, Skipping table creation..."
else
# Create Dynamodb table
aws dynamodb create-table \
    --table-name $DB_TABLE_NAME_Z_ORDER \
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

echo "Dynamodb z order table created"

echo "Creating Composite Index Table"

# Setup and seeding of ZOrder table
DB_TABLE_NAME_COMPOSITE_INDEX="EventsTableCompositeIndex"

# Check if drop table flag is passed 
if [ "$DROP_TABLE_COMPOSITE_INDEX" = "true" ]; then
    echo "Dropping the existing Composite index Dynamodb Table"
    aws dynamodb delete-table --table-name $DB_TABLE_NAME_COMPOSITE_INDEX \
        --endpoint-url http://dynamodb-local:8000 \
        --region $AWS_REGION
fi


if aws dynamodb describe-table \
    --table-name $DB_TABLE_NAME_COMPOSITE_INDEX \
    --endpoint-url http://dynamodb-local:8000 \
    --region $AWS_REGION 2>/dev/null; then
    echo "DynamoDB Table: $DB_TABLE_NAME_COMPOSITE_INDEX found, Skipping table creation..."
else
# Create Dynamodb table
aws dynamodb create-table \
    --table-name $DB_TABLE_NAME_COMPOSITE_INDEX \
    --attribute-definitions \
        AttributeName=EventType,AttributeType=S \
        AttributeName=CompositeIndex,AttributeType=B \
    --key-schema \
        AttributeName=EventType,KeyType=HASH \
        AttributeName=CompositeIndex,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --endpoint-url http://dynamodb-local:8000 \
    --region $AWS_REGION
fi

echo "Dynamodb z order table created"

# Generate mock event data using Python script
python3 -m python_src.scripts.generate_mock_events

# Split items into batches of 25 for BatchWriteItems
split -l 25 events.json events.json.

# batch write function run in parallel
puts=()
batch_write() {
    echo "In batch write"
    local file="$1"
    local table_name="$2"

    contents=$(cat "$file")

    # parse JSON into array
    items=$(jq --slurp '.' <<< "$contents")

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
       composite_index=$(echo "$item" | jq -r '.composite_index')

       # construct the PutRequest for each item
       put_request="$(jq -n --arg event_type "MeetNearMeEvent" \
           --arg city "$city" \
           --arg name "$name" \
           --arg description "$description" \
           --arg start_time "$start_time" \
           --arg end_time "$end_time" \
           --arg lon "$lon" \
           --arg lat "$lat" \
           --arg uuid "$uuid" \
           --arg z_order_index "$z_order_index" \
           --arg composite_index "$composite_index" \
           '{
               "PutRequest": {
                   "Item": {
                        "EventType": {"S": $event_type},
                        "ZOrderIndex": {"B": ($z_order_index|@base64)},
                        "CompositeIndex": {"B": ($composite_index|@base64)},
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
           }')"
        
        put_request_obj=$(jq --null-input "$put_request")

        puts+=("$put_request_obj")

    done <<< "$(echo "$items" | jq -c '.[]')"


    request_json_string="{\"$table_name\": []}"
    filter_string=".${table_name} += [\$json_put_request]"

    for json_item in "${puts[@]}"; do
        request_json_string="$(jq --argjson json_put_request "$json_item" "$filter_string" <<< "$request_json_string")"
    done

    aws dynamodb batch-write-item \
         --request-items "$request_json_string" \
         --endpoint-url http://dynamodb-local:8000 \
         --region $AWS_REGION
} 

echo "Starting batch write to z order table..."
# Run batch_write in parallel using xargs
for file in events.json.*; do 
    batch_write "$file" "$DB_TABLE_NAME_Z_ORDER" &
done
echo "Finished batch write to z order table..."

echo "Start batch write to composite index table.."
for file in events.json.*; do 
    batch_write "$file" "$DB_TABLE_NAME_COMPOSITE_INDEX" &
done
echo "Finish batch write to composite index table..."
# file=events.json.aa
# batch_write "$file"

# wait for all processes to finish
wait

rm events.json.*
echo "Finished batch writes to z order table"


echo "Now scanning db"

echo "Scanning Z Order Table"
aws dynamodb scan --table-name $DB_TABLE_NAME_Z_ORDER --endpoint-url http://dynamodb-local:8000 --select "COUNT" --region $AWS_REGION
# aws dynamodb scan --table-name $DB_TABLE_NAME_Z_ORDER --endpoint-url http://dynamodb-local:8000 --region $AWS_REGION

echo "Scanning Composite Index Table"
aws dynamodb scan --table-name $DB_TABLE_NAME_COMPOSITE_INDEX --endpoint-url http://dynamodb-local:8000 --select "COUNT" --region $AWS_REGION
# aws dynamodb scan --table-name $DB_TABLE_NAME_COMPOSITE_INDEX --endpoint-url http://dynamodb-local:8000 --region $AWS_REGION


echo "Database seed complete "
touch $seed_complete_file

if [ $1 == "--forever" ]
then
    echo "staying up to keep dependent services happy"
    sleep 10000
fi

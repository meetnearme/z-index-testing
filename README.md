# Z Order Indexing Proof of Concept for Meet Near Me Events

## Setup

1. create virtual env
```bash
python3 -m venv venv
```
2. activate the virtual env
```bash
source venv/bin/activate
```

## Seeding Database

1. If there is a need to reseed database after initial startup please delete the .seed_complete file before running 


## Interacting with DynamoDB Local Instance 
1. It is exposed from docker container at http://localhost:8000 and internally from docker compose services
as http://dynamodb-local:8000
2. Dropping table with flag 

```bash
DROP_TABLE=true docker compose up # will drop the Events Table to reset
``` 

## Testing

```bash 
pytest # running from root will find standard tests

# Below cd into python_src to collect benchmark tests
cd python_src
pytest --benchmark-only # will skip all non benchmark tests
pytest # will run all python tests
```

### Resources 

#### JQ 

1. Processing line by line json objects with jq
    https://blog.differentpla.net/blog/2019/01/11/jq-reduce/


#### Concepts 

1. Explanation of the reason for interleaving bits of binary representations 
A. Very simple example 

Consider a 2-dimensional space with coordinates (x, y), where x and y are both represented by 2 bits. Let's calculate the Z-order index for the point (1, 2) using both interleaving and concatenation.

**Interleaving:**
x = 01 (binary representation of 1)
y = 10 (binary representation of 2)
Z-order index = 0101 (interleaved bits from x and y)

**Concatenation:**
x = 01 (binary representation of 1)
y = 10 (binary representation of 2)
Concatenated value = 0110 (x and y concatenated)

Now, let's consider a nearby point (2, 2) and calculate its Z-order index using both methods:

**Interleaving:**
x = 10 (binary representation of 2)
y = 10 (binary representation of 2)
Z-order index = 1010 (interleaved bits from x and y)

**Concatenation:**
x = 10 (binary representation of 2)
y = 10 (binary representation of 2)
Concatenated value = 1010 (x and y concatenated)

With interleaving, the Z-order index for the nearby point (2, 2) is just one bit different from the previous point (1, 2). However, with concatenation, the resulting values (0110 and 1010) are quite different, despite the points being close together in the 2D space.

B. More complex example of preserving locality of four dimensions through interleaving

Let's represent each dimension with 4 bits (1 byte) to keep it simple. 

We'll calculate the Z-order index for two points:

**Point 1:**
Start time: 0110 (binary)  
End time: 1010 (binary)
Latitude: 0101 (binary)
Longitude: 0011 (binary)

**Point 2:** 
Start time: 0111 (binary)
End time: 1011 (binary)  
Latitude: 0100 (binary)
Longitude: 0010 (binary)

If we interleave the bits from the 4 dimensions, the Z-order indexes are:

**Point 1:** 
0110101000110011

**Point 2:**
0110111001001011

As you can see, despite Point 2 having slightly different values in all 4 dimensions, its Z-order index is only 3 bits different than Point 1 due to the interleaving.

Now let's see what happens if we simply concatenate the binary representations:

**Point 1:**
0110101000110011 

**Point 2:**  
0111101100100010

In this case, the concatenated values are completely different despite the points being very close together in the 4-dimensional space.

This example illustrates that concatenating destroys the locality that interleaving preserves. 

With interleaving, small changes in the 4-dimensional coordinates result in small changes in the Z-order index. This keeps nearby points grouped together when indexed, enabling efficient range queries using the Z-order index.




### Possible Further Steps

1. Partition Key

 Use a combination of the start time and geographic coordinates (latitude/longitude) as a composite partition key. For example:

```
partition_key = start_time_bin + lat_bin + lon_bin
```

Where `start_time_bin`, `lat_bin`, and `lon_bin` are binary representations of the start time, latitude, and longitude attributes respectively. 

- The main rationale for including start time in the partition key is that your queries often focus on a specific time range, so this allows efficient access to events within a given time frame.

- Adding latitude/longitude ensures some geographic grouping as well, so events in nearby locations are co-located together in partitions.

- Using binary representations keeps the partition key compact and efficient.

- The combined dimensions in the partition key provide enough variance to distribute data evenly across partitions.

- The Z-order index calculated from (start_time, latitude, longitude) can be used as the sort key within each partition.

- This approach ensures locality is preserved for range queries within each partition via the Z-order index sort key.

- Related events are co-located together via the composite partition key.

- Queries can efficiently access data for a time range across partitions in parallel.

- Point access queries can use partition key + sort key to directly access a specific event.

- A secondary index on the reverse mapping of partition key => event ID can enable reverse lookups if needed.

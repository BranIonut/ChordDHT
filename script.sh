#!/bin/bash

elem_arr=()

for _ in {1..10}; do
  x=$(( ( RANDOM % 32 )  + 1 ))
   elem_arr+=("${x}")
   echo "Creating node \"${x}\""
   docker run -it --name node${x} --network chord-net --ip 172.18.0.$((x + 1)) -e NODE_ID=${x} chord-dht-img:latest
done

sleep 20

for val in "${elem_arr[@]}"; do
   docker stop node"${val}"
   docker rm node"${val}"
done
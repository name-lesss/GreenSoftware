#!/bin/bash
port=3
measure_script="/home//$port.measure_continues.sh"
kill_measurement="/home//$port.kill_script.sh"
output_location_base="/var/scratch//results2/"
output_filename="test.csv"

run() {
    sleep 10
    output_location="$output_location_base$output_filename"
    ssh @fs0.das4.cs.vu.nl $kill_measurement
    ssh @fs0.das4.cs.vu.nl $measure_script -o $output_location -p $port &
    $command > /var/scratch//output.txt
    ssh @fs0.das4.cs.vu.nl $kill_measurement
}

sleep 10
output_location="/var/scratch//results2/idle_before.csv"
ssh @fs0.das4.cs.vu.nl $kill_measurement
ssh @fs0.das4.cs.vu.nl $measure_script -o $output_location -p $port &
sleep 60
ssh @fs0.das4.cs.vu.nl $kill_measurement

for count in {1..30}
do
    file="/var/scratch//while.py"
    output_filename="port$port.while.$count.csv"
    command="python3 $file 10000"
    echo $command
    run
done

for count in {1..30}
do
    file="/var/scratch//for.py"
    output_filename="port$port.for.$count.csv"
    command="python3 $file 10000"
    echo $command
    run
done

for count in {1..30}
do
    file="/var/scratch//sameline.py"
    output_filename="port$port.sameline.$count.csv"
    command="python3 $file 10000"
    echo $command
    run
done

for count in {1..30}
do
    file="/var/scratch//diffline.py"
    output_filename="port$port.diffline.$count.csv"
    command="python3 $file 10000"
    echo $command
    run
done

sleep 10
output_location="/var/scratch//results2/idle_after.csv"
ssh @fs0.das4.cs.vu.nl $kill_measurement
ssh @fs0.das4.cs.vu.nl $measure_script -o $output_location -p $port &
sleep 60
ssh @fs0.das4.cs.vu.nl $kill_measurement

#!/bin/sh

# RUN THIS ON DAS-5
# EXAMPLE: 
# srun -N1 -w "node028" run_continues.sh  -o "primes_300000" -p "3" -f ["python /home//programs/primes.py"]

# PLEASE CHANGE TO YOUR HOME DIRECTORY
measure_script=""
kill_measurement=""
output_location=""

while getopts "o:p:f:" opt; do
  case $opt in
    o)
      output=$OPTARG
      ;;
    p)
      port=$OPTARG
      ;;
    f)
      file=$OPTARG
      ;;
  esac
done

if ! test "$output" ; then
    echo "-o is obligatory (OUTPUT NAME)"
    exit 1
fi

if ! test "$port" ; then
    echo "-p is obligatory (PORT NODE USING [2-7])"
    exit 2
fi

if ! test "$file" ; then
    echo "-f is obligatory file to run"
    exit 3
fi

echo "Measurement script (DAS-4): $measure_script"
echo "Kill script (DAS-4): $kill_measurement"
output="$output_location$output.csv"
echo "Output file (DAS-4): $output"
echo "Program (DAS-5): $file"


# make sure no measurement is running
ssh @fs0.das4.cs.vu.nl $kill_measurement

# Start measurement
ssh @fs0.das4.cs.vu.nl $measure_script -o $output -p $port &

# Run program
FieldSeparator=$IFS
IFS=,
for command in $file;
do
eval $command
done
IFS=$FieldSeparator

# Stop measurement
ssh @fs0.das4.cs.vu.nl $kill_measurement

# Copy to das-t if you want
scp @fs0.das4.cs.vu.nl:$output /home//results


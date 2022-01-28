output="classmate-test-lm-30000-optimised-"
for i in `seq 10`
do
sbatch jobs/classmate-test.sh -o "$output$i"
done

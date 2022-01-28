#!/bin/bash

# run using: nohup prun -v -np [#cpus] -o [name] -t [[[hh:]mm:]ss] -reserve [id] -keep ./run_tests.sh &
# example: nohup prun -v -native "-w "node028"" -np 1 -o outputfile -t 60 -reserve [id] -keep ./run_tests.sh

# Port to node configuration
# port 2: DAS-5/node029
# port 3: DAS-5/node028
# port 4: DAS-5/node027
# port 5: DAS-5/node026
# port 6: DAS-5/node025
# port 7: DAS-5/node024

problems=(binarytrees fannkuchredux fasta mandelbrot nbody revcomp spectralnorm)
#echo ${problems[1]}
#input_small=(10 7 1000 200 1000 "0 < revcomp_small.txt" 100)
#input_large=(21 12 25000000 16000 50000000 "0 < revcomp_large.txt" 5500)
#input=(10 7 1000 200 1000 "0" 100) #change this one for the other output
input=(21 12 25000000 16000 50000000 "0" 5500)
command2="/var/scratch//revcomp/revcomp_large.txt" #needs to be cahnged for large

port=2
counts=(15 16 17 18 19 20 21 22)
#(6 7 8 9 10 11 12 13)
#(1 2 3 4 5) #ALWAYS CHANGE TO MAKE SURE NO DUPLICATE ID's
#24+24+16=64hours(use some extra)
measure_script="/home//$port.measure_continues.sh"
kill_measurement="/home//$port.kill_script.sh"
output_location_base="/var/scratch//results/"
output_filename="test.csv"


run() {
    sleep 10
    output_location="$output_location_base${problems[problem]}/$output_filename"
    ssh @fs0.das4.cs.vu.nl $kill_measurement
    ssh @fs0.das4.cs.vu.nl $measure_script -o $output_location -p $port &
    for ((n=0;n<$times;n++))
    do
        $command > /var/scratch//output.txt
    done
    ssh @fs0.das4.cs.vu.nl $kill_measurement
}

run_rev() {
    sleep 10
    output_location="$output_location_base${problems[problem]}/$output_filename"
    ssh @fs0.das4.cs.vu.nl $kill_measurement
    ssh @fs0.das4.cs.vu.nl $measure_script -o $output_location -p $port &
    for ((n=0;n<$times;n++))
    do
        $command < $command2 > /var/scratch//output.txt
    done
    ssh @fs0.das4.cs.vu.nl $kill_measurement
}

for count in ${counts[*]}
do
    #idle power measure
    sleep 10
    output_location="/var/scratch//results/idle/start.port$port.count$count.csv"
    ssh @fs0.das4.cs.vu.nl $kill_measurement
    ssh @fs0.das4.cs.vu.nl $measure_script -o $output_location -p $port &
    sleep 60
    ssh @fs0.das4.cs.vu.nl $kill_measurement

    #: <<'END'
    #Binarytrees - Java
    problem=0
    ids=(2 3 4 6 7)
    for id in ${ids[*]}
    do
        if [ $id -eq 7 ]
        then
            times=5
        elif [ $id -eq 4 ]
        then
            times=3
        else
            times=2
        fi
        output_filename="port$port.java-$id.problem$problem.$count.csv"
        command="java -cp /var/scratch//${problems[$problem]}/java-$id ${problems[$problem]} ${input[$problem]}"
        echo $command
        run
    done

    #Fannkuchredux - Java
    problem=1
    ids=(1 2 3)
    for id in ${ids[*]}
    do
        if [ $id -eq 2 ]
        then
            times=1
        elif [ $id -eq 1 ]
        then
            times=4
        else
            times=5
        fi
        output_filename="port$port.java-$id.problem$problem.$count.csv"
        command="java -cp /var/scratch//${problems[$problem]}/java-$id ${problems[$problem]} ${input[$problem]}"
        echo $command
        run
    done

    #Fasta - Java
    problem=2
    ids=(2 4)
    times=2
    for id in ${ids[*]}
    do
        output_filename="port$port.java-$id.problem$problem.$count.csv"
        command="java -cp /var/scratch//${problems[$problem]}/java-$id ${problems[$problem]} ${input[$problem]}"
        echo $command
        run
    done

    #Mandelbrot - Java
    problem=3
    ids=(1 2 3 4 6)
    times=8
    for id in ${ids[*]}
    do
        output_filename="port$port.java-$id.problem$problem.$count.csv"
        command="java -cp /var/scratch//${problems[$problem]}/java-$id ${problems[$problem]} ${input[$problem]}"
        echo $command
        run
    done

    #Nbody - Java
    problem=4
    ids=(1 2 3 4 5)
    times=2
    for id in ${ids[*]}
    do
        output_filename="port$port.java-$id.problem$problem.$count.csv"
        command="java -cp /var/scratch//${problems[$problem]}/java-$id ${problems[$problem]} ${input[$problem]}"
        echo $command
        run
    done

    #Revcomp - Java
    problem=5
    ids=(4 5 6 8)
    #exclude 3 because of sometimes run error
    times=8
    for id in ${ids[*]}
    do
        output_filename="port$port.java-$id.problem$problem.$count.csv"
        command="java -cp /var/scratch//${problems[$problem]}/java-$id ${problems[$problem]} ${input[$problem]}"
        echo $command "<" $command2
        run_rev
    done

    #Spectralnorm - Java
    problem=6
    ids=(1 2)
    for id in ${ids[*]}
    do
        if [ $id -eq 1 ]
        then
            times=1
        else
            times=5
        fi
        output_filename="port$port.java-$id.problem$problem.$count.csv"
        command="java -cp /var/scratch//${problems[$problem]}/java-$id ${problems[$problem]} ${input[$problem]}"
        echo $command
        run
    done
    #END

    #: <<'END'
    #Binarytrees - JavaScript
    problem=0
    times=1
    file="/var/scratch//${problems[$problem]}/${problems[$problem]}.js"
    output_filename="port$port.javascript-1.problem$problem.$count.csv"
    command="node $file ${input[$problem]}"
    echo $command
    run

    #Fannkuchredux - JavaScript
    problem=1
    ids=(1 3 4)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.node-$id.js"
        output_filename="port$port.javascript-$id.problem$problem.$count.csv"
        command="node $file ${input[$problem]}"
        echo $command
        run
    done

    #Fasta - JavaScript
    problem=2
    ids=(1 2 3 4)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.node-$id.js"
        output_filename="port$port.javascript-$id.problem$problem.$count.csv"
        command="node $file ${input[$problem]}"
        echo $command
        run
    done

    #Mandelbrot - JavaScript
#    problem=3
#    times=3
#    file="/var/scratch//${problems[$problem]}/${problems[$problem]}.js"
#    output_filename="port$port.javascript.problem$problem.$count.csv"
#    command="node $file ${input[$problem]}"
#    echo $command
#    run

    #Nbody - JavaScript
    problem=4
    ids=(1 2 4 5)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.node-$id.js"
        output_filename="port$port.javascript-$id.problem$problem.$count.csv"
        command="node $file ${input[$problem]}"
        echo $command
        run
    done

    #Revcomp - JavaScript
    problem=5
    ids=(2 7)
    for id in ${ids[*]}
    do
        if [ $id -eq 2 ]
        then
            times=2
        else
            times=3
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.node-$id.js"
        output_filename="port$port.javascript-$id.problem$problem.$count.csv"
        command="node $file ${input[$problem]}"
        echo $command "<" $command2
        run_rev
    done

    #Spectralnorm - JavaScript
    problem=6
    ids=(1 2 3 5)
    times=2
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.node-$id.js"
        output_filename="port$port.javascript-$id.problem$problem.$count.csv"
        command="node $file ${input[$problem]}"
        echo $command
        run
    done
    #END

    #: <<'END'
    #Binarytrees - Python3
    problem=0
    ids=(1 2)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.python3-$id.py"
        output_filename="port$port.python3-$id.problem$problem.$count.csv"
        command="python3 $file ${input[$problem]}"
        echo $command
        run
    done


    #Fannkuchredux - Python3
    problem=1
    ids=(1 2 4 6)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.python3-$id.py"
        output_filename="port$port.python3-$id.problem$problem.$count.csv"
        command="python3 $file ${input[$problem]}"
        echo $command
        run
    done

    #Fasta - Python3
    problem=2
    ids=(1 2 3)
    times=1
    #5 different output
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.python3-$id.py"
        output_filename="port$port.python3-$id.problem$problem.$count.csv"
        command="python3 $file ${input[$problem]}"
        echo $command
        run
    done

    #Mandelbrot - Python3
    problem=3
    ids=(2 5)
    #6 no module numpy
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.python3-$id.py"
        output_filename="port$port.python3-$id.problem$problem.$count.csv"
        command="python3 $file ${input[$problem]}"
        echo $command
        run
    done

    #Nbody - Python3
    problem=4
    ids=(1 2)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.python3-$id.py"
        output_filename="port$port.python3-$id.problem$problem.$count.csv"
        command="python3 $file ${input[$problem]}"
        echo $command
        run
    done

    #Revcomp - Python3
    problem=5
    ids=(4 6)
    times=3
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.python3-$id.py"
        output_filename="port$port.python3-$id.problem$problem.$count.csv"
        command="python3 $file ${input[$problem]}"
        echo $command "<" $command2
        run_rev
    done

    #Spectralnorm - Python3
    problem=6
    ids=(5 6)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.python3-$id.py"
        output_filename="port$port.python3-$id.problem$problem.$count.csv"
        command="python3 $file ${input[$problem]}"
        echo $command
        run
    done
    #END

    #: <<'END'
    #Binarytrees - PHP
    problem=0
    ids=(1 2 3)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.php-$id.php"
        output_filename="port$port.php-$id.problem$problem.$count.csv"
        command="php -n -d memory_limit=4096M $file ${input[$problem]}"
        echo $command
        run
    done

    #Fannkuchredux - PHP
    problem=1
    ids=(1 2 3)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.php-$id.php"
        output_filename="port$port.php-$id.problem$problem.$count.csv"
        command="php -n $file ${input[$problem]}"
        echo $command
        run
    done

    #Fasta - PHP
    problem=2
    ids=(2 3 4)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.php-$id.php"
        output_filename="port$port.php-$id.problem$problem.$count.csv"
        command="php -n $file ${input[$problem]}"
        echo $command
        run
    done

    #Mandelbrot - PHP
    problem=3
    ids=(1 3)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.php-$id.php"
        output_filename="port$port.php-$id.problem$problem.$count.csv"
        command="php -n $file ${input[$problem]}"
        echo $command
        run
    done

    #Nbody - PHP
    problem=4
    id=3
    times=1
    file="/var/scratch//${problems[$problem]}/${problems[$problem]}.php-$id.php"
    output_filename="port$port.php-$id.problem$problem.$count.csv"
    command="php -n $file ${input[$problem]}"
    echo $command
    run

    #Revcomp - PHP
    problem=5
    ids=(1 2 3)
    for id in ${ids[*]}
    do
        if [ $id -eq 3 ]
        then
            times=7
        else
            times=14
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.php-$id.php"
        output_filename="port$port.php-$id.problem$problem.$count.csv"
        command="php -n $file ${input[$problem]}"
        echo $command "<" $command2
        run_rev
    done

    #Spectralnorm - PHP
    problem=6
    ids=(2 3)
    #1 parse error
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.php-$id.php"
        output_filename="port$port.php-$id.problem$problem.$count.csv"
        command="php -n $file ${input[$problem]}"
        echo $command
        run
    done
    #END

    #: <<'END'
    #Binarytrees - C#
    problem=0
    ids=(1 2 3 4)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.csharp-$id.exe"
        output_filename="port$port.cs-$id.problem$problem.$count.csv"
        command="mono $file ${input[$problem]}"
        echo $command
        run
    done

    #Fannkuchredux - C#
    problem=1
    ids=(1 2 3 4 5 6)
    times=1
    for id in ${ids[*]}
    do
        if [ $id -eq 1 ] || [ $id -eq 2 ]
        then
            times=1
        else
            times=3
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.csharp-$id.exe"
        output_filename="port$port.cs-$id.problem$problem.$count.csv"
        command="mono $file ${input[$problem]}"
        echo $command
        run
    done

    #Fasta - C#
    problem=2
    ids=(1 2 3 4)
    for id in ${ids[*]}
    do
        if [ $id -eq 2 ]
        then
            times=2
        else
            times=3
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.csharp-$id.exe"
        output_filename="port$port.cs-$id.problem$problem.$count.csv"
        command="mono $file ${input[$problem]}"
        echo $command
        run
    done

    #Mandelbrot - C#
    problem=3
    ids=(1 2 3 4 5 6)
    for id in ${ids[*]}
    do
        if [ $id -eq 2 ]
        then
            times=2
        elif [ $id -eq 5 ] || [ $id -eq 3 ]
        then
            times=4
        else
            times=3
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.csharp-$id.exe"
        output_filename="port$port.cs-$id.problem$problem.$count.csv"
        command="mono $file ${input[$problem]}"
        echo $command
        run
    done

    #Nbody - C#
    problem=4
    ids=(1 2 3 4 5 6 8)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.csharp-$id.exe"
        output_filename="port$port.cs-$id.problem$problem.$count.csv"
        command="mono $file ${input[$problem]}"
        echo $command
        run
    done

    #Revcomp - C#
    problem=5
    ids=(1 2 3 4 5 6)
    for id in ${ids[*]}
    do
        if [ $id -eq 3 ]
        then
            times=3
        else
            times=7
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.csharp-$id.exe"
        output_filename="port$port.cs-$id.problem$problem.$count.csv"
        command="mono $file ${input[$problem]}"
        echo $command "<" $command2
        run_rev
    done

    #Spectralnorm - C#
    problem=6
    ids=(1 3)
    for id in ${ids[*]}
    do
        if [ $id -eq 1 ]
        then
            times=1
        else
            times=2
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.csharp-$id.exe"
        output_filename="port$port.cs-$id.problem$problem.$count.csv"
        command="mono $file ${input[$problem]}"
        echo $command
        run
    done
    #END

    #: <<'END'
    #Binarytrees - Ruby
    problem=0
    ids=(1 2 3 4)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.yarv-$id.yarv"
        output_filename="port$port.yarv-$id.problem$problem.$count.csv"
        command="ruby -W0 $file ${input[$problem]}"
        echo $command
        run
    done

    #Fannkuchredux - Ruby
    problem=1
    ids=(1 2)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.yarv-$id.yarv"
        output_filename="port$port.yarv-$id.problem$problem.$count.csv"
        command="ruby -W0 $file ${input[$problem]}"
        echo $command
        run
    done

    #Fasta - Ruby
    problem=2
    ids=(2 3 4 5 6)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.yarv-$id.yarv"
        output_filename="port$port.yarv-$id.problem$problem.$count.csv"
        command="ruby -W0 $file ${input[$problem]}"
        echo $command
        run
    done

    #Mandelbrot - Ruby
    problem=3
    ids=(1 2 3 6 7)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.yarv-$id.yarv"
        output_filename="port$port.yarv-$id.problem$problem.$count.csv"
        command="ruby -W0 $file ${input[$problem]}"
        echo $command
        run
    done

    #Nbody - Ruby
    problem=4
    id=2
    times=1
    file="/var/scratch//${problems[$problem]}/${problems[$problem]}.yarv-$id.yarv"
    output_filename="port$port.yarv-$id.problem$problem.$count.csv"
    command="ruby -W0 $file ${input[$problem]}"
    echo $command
    run

    #Revcomp - Ruby
    problem=5
    ids=(2 3)
    for id in ${ids[*]}
    do
        if [ $id -eq 2 ]
        then
            times=2
        else
            times=4
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.yarv-$id.yarv"
        output_filename="port$port.yarv-$id.problem$problem.$count.csv"
        command="ruby -W0 $file ${input[$problem]}"
        echo $command "<" $command2
        run_rev
    done

    #Spectralnorm - Ruby
    problem=6
    ids=(1 4 5)
    times=1
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.yarv-$id.yarv"
        output_filename="port$port.yarv-$id.problem$problem.$count.csv"
        command="ruby -W0 $file ${input[$problem]}"
        echo $command
        run
    done
    #END

    #: <<'END'
    #Binarytrees - C
    problem=0
    ids=(1 5)
    for id in ${ids[*]}
    do
        if [ $id -eq 5 ]
        then
            times=2
        else
            times=1
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-flags_run"
        output_filename="port$port.c-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-noflags_run"
        output_filename="port$port.c-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Fannkuchredux - C
    problem=1
    ids=(1 2 3 4 5)
    for id in ${ids[*]}
    do
        if [ $id -eq 5 ]
        then
            times=3
        else
            times=1
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-flags_run"
        output_filename="port$port.c-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run

        times=1
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-noflags_run"
        output_filename="port$port.c-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Fasta - C
    problem=2
    ids=(1 2 4 5 6 7)
    for id in ${ids[*]}
    do
        if [ $id -eq 2 ]
        then
            times=6
        elif [ $id -eq 6 ] || [ $id -eq 5 ] || [ $id -eq 7 ]
        then
            times=4
        else
            times=2
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-flags_run"
        output_filename="port$port.c-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run

        if [ $id -eq 6 ]
        then
            times=10
        else
            times=2
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-noflags_run"
        output_filename="port$port.c-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Mandelbrot - C
    problem=3
    ids=(1 2 3 6)
    for id in ${ids[*]}
    do
        if [ $id -eq 6 ]
        then
            times=18
        elif [ $id -eq 2 ]
        then
            times=1
        else
            times=4
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-flags_run"
        output_filename="port$port.c-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run

        if [ $id -eq 2 ]
        then
            times=1
        else
            times=2
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-noflags_run"
        output_filename="port$port.c-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Nbody - C
    problem=4
    ids=(1 2 3 4 5 6)
    times=2
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-flags_run"
        output_filename="port$port.c-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-noflags_run"
        output_filename="port$port.c-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Revcomp - C
    problem=5
    ids=(1 2 3 4 5 6)
    times=10
    for id in ${ids[*]}
    do
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-flags_run"
        output_filename="port$port.c-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command "<" $command2
        run_rev
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-noflags_run"
        output_filename="port$port.c-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command "<" $command2
        run_rev
    done

    #Spectralnorm - C
    problem=6
    ids=(1 3 4 5)
    for id in ${ids[*]}
    do
        if [ $id -eq 1 ]
        then
            times=2
        elif [ $id -eq 3 ]
        then
            times=20
        else
            times=32
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-flags_run"
        output_filename="port$port.c-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run

        if [ $id -eq 4 ]
        then
            times=20
        elif [ $id -eq 5 ]
        then
            times=3
        elif [ $id -eq 3 ]
        then
            times=2
        else
            times=1
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gcc-$id-noflags_run"
        output_filename="port$port.c-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done
    #END

    #: <<'END'
    #Binarytrees - C++
    problem=0
    ids=(1 3 8)
    #2 and 6 negative output
    for id in ${ids[*]}
    do
        if [ $id -eq 1 ]
        then
            times=8
        else
            times=10
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-flags_run"
        output_filename="port$port.c++-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run

        times=1
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-noflags_run"
        output_filename="port$port.c++-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Fannkuchredux - C++
    problem=1
    ids=(1 4 6 7)
    for id in ${ids[*]}
    do
        if [ $id -eq 1 ]
        then
            times=5
        else
            times=1
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-flags_run"
        output_filename="port$port.c++-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run

        times=1
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-noflags_run"
        output_filename="port$port.c++-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Fasta - C++
    problem=2
    ids=(1 2 3 4 6)
    for id in ${ids[*]}
    do
        if [ $id -eq 6 ]
        then
            times=6
        else
            times=3
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-flags_run"
        output_filename="port$port.c++-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run

        times=2
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-noflags_run"
        output_filename="port$port.c++-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Mandelbrot - C++
    problem=3
    ids=(2 3 5 6 8 9)
    for id in ${ids[*]}
    do
        if [ $id -eq 9 ]
        then
            times=18
        elif [ $id -eq 6 ]
        then
            times=36
        elif [ $id -eq 8 ]
        then
            times=8
        else
            times=1
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-flags_run"
        output_filename="port$port.c++-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run

        times=1
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-noflags_run"
        output_filename="port$port.c++-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Nbody - C++
    problem=4
    ids=(1 3 4 5 6 7 8)
    for id in ${ids[*]}
    do
        if [ $id -eq 4 ] || [ $id -eq 7 ]
        then
            times=12
        elif [ $id -eq 1 ] || [ $id -eq 6 ]
        then
            times=2
        else
            times=4
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-flags_run"
        output_filename="port$port.c++-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run

        times=1
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-noflags_run"
        output_filename="port$port.c++-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #Revcomp - C++
    problem=5
    ids=(1 2 3 4 5)
    for id in ${ids[*]}
    do
        if [ $id -eq 5 ]
        then
            times=1
        elif [ $id -eq 1 ]
        then
            times=8
        elif [ $id -eq 3 ]
        then
            times=10
        elif [ $id -eq 4 ] || [ $id -eq 2 ]
        then
            times=20
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-flags_run"
        output_filename="port$port.c++-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command "<" $command2
        run_rev

        if [ $id -eq 1 ]
        then
            times=1
        elif [ $id -eq 3 ] || [ $id -eq 2 ]
        then
            times=10
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-noflags_run"
        output_filename="port$port.c++-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command "<" $command2
        run_rev
    done

    #Spectralnorm - C++
    problem=6
    ids=(1 5 6 8)
    for id in ${ids[*]}
    do
        if [ $id -eq 1 ]
        then
            times=2
        elif [ $id -eq 8 ]
        then
            times=20
        else
            times=40
        fi
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-flags_run"
        output_filename="port$port.c++-flags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
        file="/var/scratch//${problems[$problem]}/${problems[$problem]}.gpp-$id-noflags_run"
        output_filename="port$port.c++-noflags-$id.problem$problem.$count.csv"
        command="$file ${input[$problem]}"
        echo $command
        run
    done

    #idle power measure
    sleep 10
    output_location="/var/scratch//results/idle/end.port$port.count$count.csv"
    ssh @fs0.das4.cs.vu.nl $kill_measurement
    ssh @fs0.das4.cs.vu.nl $measure_script -o $output_location -p $port &
    sleep 60
    ssh @fs0.das4.cs.vu.nl $kill_measurement
done


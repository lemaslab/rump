#!/usr/bin/env nextflow
 
input_file = Channel.fromPath('./data/titanic.csv')
python_file_1 = Channel.fromPath('./src/add_noise.py')
python_file_2 = Channel.fromPath('./src/get_stats.py')

process add_noise {

    input:
    file f from input_file
    file p1 from python_file_1

    output:
    file 'out_1.csv' into records
 
    shell:
    """   
    python ${p1} -i ${f} -o "out_1.csv"

    """
}

process get_stats {
    echo true
 
    input:
    file f from records
    file p2 from python_file_2
 
    shell:
    """   
    python ${p2} -i ${f}

    """
 
}

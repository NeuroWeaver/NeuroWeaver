## Usage:

* Clone the repo
* Add the repo to PYTHONPATH env variable
* Configure the Systolic and SIMD config files in the config directory
* The tests directory needs to have the following structure
    - testdir
        - test1
            - instructions
            - json_files
        - test2
            - instructions
            - json_files
        .
        .
        .
        - testN
            - instructions
            - json_files
* Command to run:
    
    python3 genesys_sim/genesys.py <config_path> <testdir> <csv_output_filename>
    Example:
        python3 genesys_sim/genesys.py configs/ testdir

For energy simulations, set --mode energy

python3 genesys_sim/genesys.py configs/ testdir --mode energy

eg. python3 genesys_sim/genesys.py configs/ resnet50_benchmark128x128_1/ --mode energy

For any questions, please email rohan(at)ucsd.edu
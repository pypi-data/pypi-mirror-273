In this repository we have two modules: mosaik_csv and mosaik_csv_writer.

Installation
============

::

    $ pip install mosaik-csv

If installation of psutil fails, installing python developer edition and gcc should help::

    $ sudo apt-get install gcc python3-dev

mosaik_csv
==========

This simulator reads CSV data and sends it to mosaik.

The following code shows an example how to use the mosaik_csv simulator.
The date_format, delimiter parameter and type are optional.
If they are not defined, the standard value is 'YYYY-MM-DD HH:mm:ss' for the date_format, ',' for delimiter and time-based for type.
The first line of the CSV file refers to the model name. If no model name is defined, 'Data' is set as the default::

    sim_config = {
        'CSV': {
            'python': 'mosaik_csv:CSV',
        }
    }
    world = mosaik.World(sim_config)
    csv_sim = world.start('CSV', sim_start='01.01.2016 00:00',
                                 datafile='data.csv',
                                 date_format='DD.MM.YYYY HH:mm',
                                 delimiter=',',type=time-based)
    csv = csv_sim.Data.create(20)


mosaik_csv_writer
=================

This simulator writes simulation results to a CSV file.


The following code shows an example how to use the mosaik_csv_writer simulator.
The date_format, delimiter parameter and print_results are optional.
If they are not defined, the standard value is 'YYYY-MM-DD HH:mm:ss' for the date_format, ',' for delimiter and False for print_results.

While creating the instance of the mosaik_csv_writer (csv_writer = csv_sim_writer.Monitor(buff_size = 30 * 60)) the user can define a
buff_size depending on the simulation time (default buff_size = 500). This buff_size tells the simulator to write the data into a CSV file after every defined buffer duration. This feature speeds up the writing process of the simulator. In the given example the simulator will write the accumulated data into a CSV file after every 30 minutes simulation time (30 * 60 simulation steps)::

    sim_config = {
        'CSV_writer': {
            'python': 'mosaik_csv_writer:CSVWriter',
        }
    }
    world = mosaik.World(sim_config)
    csv_sim_writer = world.start('CSV_writer', start_date = '01.01.2016 00:00',
                                               date_format='%Y-%m-%d %H:%M:%S', 
                                               output_file='results.csv')
    csv_writer = csv_sim_writer.CSVWriter(buff_size = 30 * 60)  # write data after every 30 mins

Tests
=====

You can run the tests with::

    $ git clone https://gitlab.com/mosaik/mosaik-csv.git
    $ cd mosaik-csv
    $ pip install -r requirements.txt
    $ pip install -e .
    $ pytest tests

<h1 align="center">TCP timeout and congestion window implementation 💫</h1>

This project reads a trace file from ns-2 and calculates the TCP congestion window and timeout values
at each packet it receives/sends. For now, it is only implemented for the RFC 793 and Reno agents. 

## Table of contents
- [Dependencies](#dependencies-)
- [Install the requirements](#install-the-requirements-)
- [Usage](#usage-)
- [Testing](#execute-the-tests-)

## Dependencies 📋 

   - docker: since the simulation for reno is done in a docker container using a patched version of ns-2.35
   - ns (2.35.9): for the rfc 793 simulation
   - python (3.11.7): for the analysis. Install the requirements before running it!

### Install the requirements 📦
Install the python dependencies using the following command:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Usage 🚀
NOTE: We messed up the queue limit size for both simulations, so the following commands are with the "wrong" configuration, if you want to run the simulations with the correct queue limit size, you can use the commands on section [usage fixup](#usage-fix-)

You can run the two simulations using the following command:

```bash
$ make
```

Now you can check the plots on the "images" folder.

If you want to run the simulations separately, you can use the following commands:

```bash
$ make rfc  # for the rfc 793 simulation
$ make reno  # for the reno simulation
```

If you want to create folders, and choose every option the program gives, you can execute it with:

```bash
$ python main.py [options]
```

And see the available options with:

```bash
$ python main.py -h
```

## Usage fixup 🚀
If you want to run the simulations with the correct queue limit size, you can use the following commands:

```bash
$ make fixup
```

## Execute the tests! 🧪
I did some tests just to check if some "tricky" parts of the code were working as expected. You can run them using the following command:
```bash
$ make test
```

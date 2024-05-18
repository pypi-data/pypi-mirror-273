[![License](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](https://opensource.org/licenses/GPL-3.0)
[![Documentation Status](https://readthedocs.org/projects/mio-cli/badge/?version=latest)](https://mio-cli.readthedocs.io/en/latest/index.html)

# [Moore.io](https://www.mooreio.com/) [Command Line Interface Client](https://datum-technology-corporation.github.io/mio_cli_client/)


## About

|  | From the [User Manual](https://mio-cli.readthedocs.io/en/latest/)'s [Executive Summary](https://mio-cli.readthedocs.io/en/latest/overview.html#executive-summary) |
|-|-|
| [![Moore.io Logo](https://github.com/Datum-Technology-Corporation/mio_cli_client/blob/gh-pages/assets/img/logo.png?raw=true)](https://pypi.org/project/mio-cli/1.0.1/) | The Moore.io Command Line Interface (CLI) Client orchestrates disparate free and/or open source tools into a single, complete, straightforward and integrated toolchain for hardware engineers.  The CLI consists of a succinct and powerful command set which developers use via a terminal on their operating system (Windows/Linux/OSX). |



## Installation
`mio` can be installed directly from [`pip3`](https://pip.pypa.io/en/stable/):

````
pip3 install mio-cli
````


## [Developer Guide](https://datum-technology-corporation.github.io/mio_cli_client/dev_guide.html)

## [Demo Project](https://github.com/Datum-Technology-Corporation/mio_demo)




## Usage
````
  mio [--version] [--help]
  mio [--wd WD] [--dbg] CMD [OPTIONS]

Options:
  -v, --version
    Prints the mio version and exits.
  
  -h, --help
    Prints the overall synopsis and a list of the most commonly used commands and exits.
    
  -C WD, --wd WD
    Run as if mio was started in WD (Working Directory) instead of the Present Working Directory `pwd`.
   
  --dbg
    Enables debugging outputs from mio.

Full Command List (`mio help CMD` for help on a specific command):
   Help and Shell/Editor Integration
      doctor         Runs a set of checks to ensure mio installation has what it needs to operate properly
      help           Prints documentation for mio commands
   
   Project and Code Management
      init           Starts project creation dialog
      gen            Generates DV source code via the UVMx template engine
   
   IP and Credentials Management
      install        Install all IP dependencies from IP Marketplace
      login          Start session with IP Marketplace
      package        Create a compressed (and potentially encrypted) archive of an IP
      publish        Publish IP to IP Marketplace (must have mio admin account)
   
   EDA Automation
      !              Repeat last command
      regr           Runs regression against an IP
      sim            Performs necessary steps to simulate an IP with any simulator
      
   Manage Results and other EDA Tool Outputs
      clean          Manages outputs from tools (other than job results)
      cov            Manages coverage data from EDA tools
      dox            HDL source code documentation generation via Doxygen
      results        Manages results from EDA tools
````

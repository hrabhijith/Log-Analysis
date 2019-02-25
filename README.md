# Project: log Analysis

Log Analysis is a tool which analyses the database of a frontend end application and generates a detailed report of the usage.

This tool generates three reports on a specific front end application usage using the application's database and logs recorded in it periodically on basis of usage traffic on the console/command line. 

## Installation

Follow each section below to install all the required softwares and tools to run this project.

* To run commands on the terminal on your computer (if you don't have one) install:

In **Windows OS**, you can use the Git Bash terminal program from [Git](https://git-scm.com/download/win).
On **Windows 10 OS**, you can use the bash shell in [Windows Subsystem for Linux](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide).
On **Mac OS**, you can use the built-in **Terminal** program, or another such as **iTerm**.
On **Linux**, you can use any common terminal program such as **gnome-terminal** or **xterm**.

* Install Python 3 locally in your computer.

**Windows and Mac:** Install it from python.org according to you computer's OS: [link](https://www.python.org/downloads/)
**Mac (with Homebrew):** In the terminal, run `brew install python3`
**Debian/Ubuntu/Mint:** In the terminal, run `sudo apt-get install python3`

Use this command from the command line to check the installtion status of python `python3 --version`

* Install **Virtual Box**
VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org, [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

**Ubuntu users:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

* Install **Vagrant**
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com, [here](https://www.vagrantup.com/downloads.html). Install the version for your operating system.

**Windows users:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.
If Vagrant is successfully installed, you will be able to run `vagrant --version` in your terminal to see the version number.

* Once you have VirtualBox and Vagrant installed, open a terminal and run the following commands:

`mkdir project`
`cd project`
`vagrant init ubuntu/trusty64`
`vagrant up`

This will create a new directory for this project and begin downloading a Linux image into this directory. It may take a long time to download, depending on your Internet connection.

When it is complete, you can log into the Linux instance with `vagrant ssh`. You are now ready to continue with the project.

If you log out of the Linux instance or close the terminal, the next time you want to use it you only need to run `cd project` and `vagrant ssh`

* Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the vagrant directory 'project', which is shared with your virtual machine.

To build the reporting tool, you'll need to load the site's data into your local database.

To load the data, cd into the vagrant directory using `cd /vagrant` inside VM from which you will be able to access files in the 'project' directory and use the command `psql -d news -f newsdata.sql`.

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

* If Postgresql is not installed by default in your virtual machine, click [here](https://www.postgresql.org/download/linux/ubuntu/) for details.

## Source Code

The source code is written in the "log.py" file and should be run from linux machine which has PSQL installed.

According to the python version installed, the code can be run 

using either
`python log.py`

or using 
`python3 log.py`


## Database

* This project uses postgresql as database tool and language for queries.
* Before running the code, 'news' database has to be setup and data should be inserted.

## Views

This project needs below three views to be created in the database before start. Queries to create the same are listed below. Run all the queries before running source code and after creating the database.

* For the second part of the report.

`create view auth_log as select a.author as author_id, count(b.path) as view_count from articles as a left join log as b on a.slug = replace(b.path,'/article/','') group by a.author;`

* For the third part of the report.

`create view status_all as select SUBSTRING (TO_CHAR(time, 'YYYY-MM-DD HH24:MI'), 1, 10) as date_all, count(status) as count_all from log group by date_all;`

`create view status_error as select SUBSTRING (TO_CHAR(time, 'YYYY-MM-DD HH24:MI'), 1, 10) as date_error, count(status) as count_error from log where status not like '%200 OK%' group by date_error;`

`create view error_percentage as select a.date_all, b.count_error::decimal/a.count_all*100 as percent_error from status_all as a join status_error as b on a.date_all = b.date_error;`

## Output 

The output will be printed on the command line of the VM.
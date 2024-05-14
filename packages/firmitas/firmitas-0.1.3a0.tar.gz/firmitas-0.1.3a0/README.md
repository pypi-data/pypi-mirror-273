# firmitas

Simple notification service for X.509-standard TLS certificate statuses

## `__usage__`

1. Clone the repository to your local storage and make it the present working directory.
   ```
   $ git clone https://gitlab.com/t0xic0der/firmitas.git
   ```
   ```
   $ cd firmitas
   ```
2. Ensure that [`Poetry`](https://python-poetry.org/) and [Virtualenv](https://pypi.org/project/virtualenv/) are installed and up-to-date on the system.
   ```
   $ sudo dnf install --assumeyes poetry virtualenv
   ```
3. Create a virtual environment within the cloned local directory and enable it.
   ```
   $ virtualenv venv
   ```
   ```
   $ source venv/bin/activate
   ```
4. Install the project and its dependencies in the enabled virtual environment.
   ```
   $ (venv) poetry install
   ```
5. Make a copy of the project configuration file and make your changes to it.
   ```
   $ (venv) cp firmitas/conf/standard.py firmitas/conf/myconfig.py
   ```
   The project configuration file houses the following variables that can be modified according to the requirements of the project user.  
   - `gitforge` - The source code forge on which the issue tickets need to be created. The valid options for this configuration variable are `github`, `gitlab` and `pagure`. The support for `pagure` is implemented while that for `github` and `gitlab` is planned.
   - `repoloca` - The location of the ticketing repository. This is required for source code forges that require the absolute location of the remote ticketing repository for the project to be able to access the API and create notification tickets.
   - `reponame` - The name of the ticketing repository. This is required for source code forges that require the repository name with namespace of the remote ticketing repository for the project to be able to access the API and create notification tickets.
   - `username` - The username to masquerade as in order to create notification tickets. This is required for source code forges that require the username with whom an API token is associated for the project to be authenticated on their behalf.
   - `password` - The password or API token belonging to the aforementioned username. This is required for source code forges that require the password or API token associated with the ticketing repository to authenticate the project on the owner's behalf.
   - `daysqant` - The minimum number of days remaining from the validity expiry date to make notifications for. As a sane default, it is set to open up a notification ticket when the TLS certificate is 30 days away from its validation expiry date.
   - `tagslist` - The list of labels to the tag the notification tickets with. A minimum of one label is required to ensure that there is a way to filter out the automated notification tickets on a shared issue tracker from the manually created ones.
   - `maxretry` - The maximum number of retries to make when the process of opening up a notification ticket fails. As a sane default, it is set to allow up to 5 retries, and it is a good practice to have a value greater than one to compensate for spotty connections.
   - `certloca` - The location where the X.509 standard TLS certificates are stored. Note that this refers to a locally available storage location and not a remotely available storage location. The default is set as "/var/tmp/firmitas/certhere" directory.
   - `hostloca` - The location where the mapping file of service hostnames, maintainers, certificate statistics and notification statistics are stored. As with the previous configuration variable, even this one refers to a locally available storage location.
   - `logrconf` - The configuration variable that sets the logging behaviour for the project. As a sane default, the logging level has been set to "DEBUG" to allow for greater verbosity in details and a custom format to the console handler.
   - `certdict` - The global variable used across the project to share the details of the certificates to be probed into, the statistics of issuing authority, serial number, dates information and much more. Do not change it as this gets overridden.
6. Make a copy of the mapping configuration file and make your changes to it.
   ```
   $ (venv) cp firmitas/conf/certlist.yml firmitas/conf/mytlscts.yml
   ```
   The mapping configuration file houses a list of service hostnames having the following variables that can be either modified according to the requirements of the project user or computed by the project during its runtime.
   - `path`: The location of the X.509 standard TLS certificate file relative to the "certloca" variable previously set in the project configuration file. This helps the project to locate the X.509 standard TLS certificate file is read and acted upon.
   - `user`: The username on the source code forge that was previously set on the "gitforge" variable in the project configuration file. If the username is not available on the stated source code forge, the notification ticket making process will error out.
   - `certstat`: This consists of a list of variables that must not be set manually as they would be overridden by the project during its runtime. Here is a list of those variables with their associated meanings and significance.
     - `cstarted`: A variable of boolean type. This is computed as TRUE if the current datetime is greater than the "not valid before" datetime of the stated X.509 standard TLS certificate and FALSE if the current datetime is lesser than the "not valid before" datetime of the same.
     - `cstopped`: A variable of boolean type. This is computed as TRUE if the current datetime is greater than the "not valid after" datetime of the stated X.509 standard TLS certificate and FALSE if the current datetime is less than the "not valid after" datetime of the same.
     - `daystobt`: A variable of integer type. This is computed as the difference in the number of days from the current datetime to the datetime from when the stated X.509 standard TLS certificate becomes valid. This can either be a positive integer if the "not valid before" datetime has not been reached or a negative integer if the "not valid before" datetime has been passed.
     - `daystodd`: A variable of integer type. This is computed as the difference in the number of days from the current datetime to the datetime to when the stated X.509 standard TLS certificate becomes expired. This can either be a positive integer if the "not valid after" datetime has not been reached or a negative integer if the "not valid after" datetime has been passed.
     - `issuauth`: A variable of string type. This stores the found name of the issuing authority for the stated X.509 standard TLS certificate. This can be useful if the same issuing authority is planned to be used to regenerate a new one from.
     - `serialno`: A variable of string type. This stores the found serial number of the stated X.509 standard TLS certificate. This can be useful to de-validate the existing certificate before opting in to regenerate a new one.
     - `strtdate`: A variable of datetime type. This is computed as the datetime data consisting of the "not valid before" datetime value.
     - `stopdate`: A variable of datetime type. This is computed as the datetime data consisting of the "not valid after" datetime value.
   - `notistat`: This consists of a list of variables that must not be set manually as they would be overridden by the project during its runtime. Here is a list of those variables with their associated meanings and significance.
     - `done`: A variable of boolean type. This stores the flag to state if the notification about the expiry of the stated X.509 standard TLS certificate has been made. The variable is set to TRUE if the notification has been created and FALSE otherwise.
     - `link`: A variable of string type. This stores the location of the notification ticket on the selected source code forge that was previously set on the "gitforge" variable in the project configuration file.
     - `time`: A variable of datetime type. This stores the datetime information of when the previously stated notification ticket was created. This can be useful to track down if there are any repeated notifications made.
7. Make sure that the location of the custom mapping configuration file is pointed correctly at in the custom project configuration file.
8. View the console help menu of the project service by running the following command.
   ```
   $ (venv) firmitas --help
   ```
   Output
   ```
   Usage: firmitas [OPTIONS]
   
   Options:
     -c, --conffile PATH  Read configuration from the specified Python file
     --version            Show the version and exit.
     --help               Show this message and exit.
   ```
9. With the configuration variables set appropriately, run the project service by executing the following command.
   ```
   $ (venv) firmitas --conffile firmitas/conf/myconfig.py
   ```
   Refrain from making any changes in the existing entries of the mapping configuration file after the first successful run unless it is absolutely necessary to do so as the project service writes and references notification creation status from that file. Any unmonitored change to the existing entries in said file after the first successful run of the project service could lead to unintended consequences such as duplicate notification entries, untracked notification tickets pertaining to services etc.

## `__license__`

This project is licensed under GNU General Public License 3.0 or later.

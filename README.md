# swep-ss2019: Software development project

### Topic: Fast and flexible clustering of numerical and categorical data for spatio-temporal social media data analysis

***

### Overview
TBD

### Install and run the code
**Linux**:
 - Mark setup_env.sh as executable (`chmod +x setup_env.sh`)
 - Run `source setup_env.sh`
   - Sets up a virtual environment and installs all required packages
 - Activate the virtual environment by running `source ./env/bin/activate`
 - Run `python main.py` to start the commandline interface

 **Windows**:
  - Run `setup_env.bat`
    - Sets up a virtual environment and installs all required packages
  - Activate the virtual environment by running `env\scripts\activate`
  - Run `python main.py` to start the commandline interface

### Setup Plotly
In order to use the plot functionality, you have to own a plotly account and
configure your local plotly installation.
Start python in the Termnal with `python`. Then type in the following commands.
  - `import plotly`
  - `plotly.tools.set_credentials_file(username='DemoAccount', api_key='lr1c37zw81')`
You have to replace *DemoAccount* with your username and the API key with your own. You can find your API key [here](https://plot.ly/settings/api).

# robo-advisor

Robo Advisor Project

A tool that automates the process of providing clients with stock recommendations.

Prerequisites

Anaconda 3.7+ Python 3.7+ Pip

Installation

Navigate to the repository from the command line (subsequent commands assume you are running them from the local repository's root directory) by using the following command:

cd robo-advisor
(Use cd ~/Desktop/robo-advisor if the repository is stored in the desktop)

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

    conda create -n stocks-env python=3.8 # (first time only)
    conda activate stocks-env

From inside the virtual environment, install package dependencies:

    pip install -r requirements.txt
    pip install plotly 

Setup

Obtain an API Key from AlphaVantage API (www.alphavantage.co) in order to issue request. In the root directory of your local repository, create a new file called ".env", and store the API Key value in the ".env" file (replace "abc123" with the correct API Key):

    ALPHAVANTAGE_API_KEY="abc123"

Usage

Run the project script:

    python app/robo_advisor.py

(Adapted from from Professor Rossetti's markdown)
## Cryptocurrency Price Tracker
Project Overview
This Python project fetches and tracks cryptocurrency prices using the CoinGecko API. The primary functionality revolves around capturing price data for selected cryptocurrencies over a specified period, then analyzing and visualizing the price changes graphically. This tool is useful for anyone interested in monitoring market trends and understanding price 
fluctuations in near real-time.


## Features 
Data Fetching: Retrieves current prices of cryptocurrencies like Bitcoin, Ethereum, and others from the CoinGecko API.
Price Tracking: Tracks price changes at five-minute intervals over a 30-minute period.
Data Visualization: Plots the price data on a time series graph, highlighting percentage changes and visually indicating price increases or decreases.
## How It Works
Fetching Prices: The fetch_price function connects to the CoinGecko API and fetches the current USD price of a specified cryptocurrency.
Tracking Prices: The track_prices function calls fetch_price periodically (every 5 minutes) for 30 minutes, collecting price data for multiple cryptocurrencies.
Analyzing and Visualizing Data: The analyze_and_plot function processes the collected data, plotting it on a graph with time on the x-axis and price in USD on the y-axis. Price changes are calculated and annotated directly on the graph, with increases in green and decreases in red.
## Setup and Usage
Dependencies: Before running this script, ensure you have Python installed along with the requests, pandas, and matplotlib libraries. These can be installed via pip:
Copy code
pip install requests pandas matplotlib
Execution: Run the script by navigating to the directory containing the script and typing the following command:
Copy code
python script_name.py
Limitations
The script is dependent on the availability and rate limits of the CoinGecko API.
Currently, the script tracks prices for a fixed duration and interval. Adjustments can be made in the script to customize these values.
Contributions
Contributions are welcome! If you have ideas for improvements or encounter an issue, please feel free to open an issue or submit a pull request.


## Output

![Ekran görüntüsü 2024-04-15 014053](https://github.com/erent8/Cyrpto-Analyzer/assets/86615310/f079a9a6-73af-487d-a109-b8c73205dbab)
 

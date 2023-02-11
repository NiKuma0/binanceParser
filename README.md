# The BinanceParser
This is a CLI application needs for stream price of XRP/USDT.


Application starts stream the price of a given trading socket, and if the price
falls by more than one percent in one hour, the function yields
the percentage, maximum price in one hour, and current price.


## How to build it:

1. Clone this repo as you like
2. You needs the python, so install it if you don't have it
3. Go to the repo directory and run this command:
    ```shell
    $ python -m pip install .
    ```
    If you need test version you can add `-e` argument.
    But better way is use `poetry`.
4. Now run it:
    ```shell
    $ python -m binanceparser.main
    ```

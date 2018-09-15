# lisk-base64
Lisk Base64 is a tool that allows you to:

- **Encode** user input to Base64 data and broadcast it to the Lisk network
-  Retrieve and **decode**  Base64 data stored on the Lisk network

A `.lsk64` file is created upon encoding an input. You can use this to decode the object back to its original form, using data from the Lisk blockchain.

This is a **proof of concept**. Credits to [Korben3](https://github.com/Korben3) for working on the idea and brainstorming together.

If you like this software, please consider a donation =] `6725360537423611335L`

## Prerequisites (encode mode only)
Considering there’s no Lisk library for Python yet, and the current version of Lisk Commander does not support the data field, [karek314](https://github.com/karek314/)'s awesome [lisk-php](https://github.com/karek314/lisk-php) is used for pushing TXs to the network as a temporary workaround.

**Please install and configure this tool if you’d like to use encode mode**.

## Installation
```
git clone https://github.com/Lemii/lisk-base64
cd lisk-base64
pip install -r requirements.txt
```
Open `config.py` and enter your information. Account information is only required if you wish to use `encode` mode.

## Usage

`lisk-base64.py` expects at least two arguments; **mode** (positional) and **input** (`-i` or `--input`).

Default values will be used for empty arguments (please see command line help for more info).

#### Mode: encode
Use this mode to encode your input to Base64, broadcast it to the Lisk network and create an intermediary file.


Example #1:

`python lisk-base64.py encode -i "example.png"`


Example #2: 

`python lisk-base64.py encode -i "example.png" -o "my-custom-output.lsk64" -r 123L -a 0.00000001`

#### Mode: decode
Use this mode to retrieve Base64 data from the Lisk network using an intermediary `.lsk64` file and decode it to its original form. 

The original file type is detected from the lsk64 file, so it is recommended to only use the output argument (`-o` or `--output`) in exceptional cases.

Example #1:

`python lisk-base64.py decode -i "example.lsk64"`

Example #2:

`python lisk-base64.py decode -i "example.lsk64" -o "im-a-rebel.png"`

#### Command line help
Running `$ python lisk-base64.py -h`:

```
usage: lisk-base64.py [-h] [-i INPUT] [-o OUTPUT] [-r RECIPIENT] [-a AMOUNT]
                      {encode,decode}

positional arguments:
  {encode,decode}       set mode to 'encode' or 'decode'

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        specify input file name
  -o OUTPUT, --output OUTPUT
                        specify output file name
  -r RECIPIENT, --recipient RECIPIENT
                        specify receiving address
  -a AMOUNT, --amount AMOUNT
                        specify LSK amount to be sent per TX
```
## License
Licensed under the [MIT license](https://github.com/Lemii/lisk-base64/blob/master/LICENSE)

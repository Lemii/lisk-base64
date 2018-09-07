import base64
import sys
import subprocess
import re
import requests
import json 
import argparse
import os
import csv
import config


# Configure arguments and options
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="set mode to 'encode' or 'decode'", choices=['encode', 'decode'])
parser.add_argument("-i", "--input", help="specify input file name")
parser.add_argument("-o", "--output", help="specify output file name")
parser.add_argument("-r", "--recipient", help="specify receiving address")
parser.add_argument("-a", "--amount", help="specify LSK amount to be sent per TX", type=float)
args = parser.parse_args()


# Encode input to base64
def base64_encode(input):
	with open(input, 'rb') as f:
		input_encode = base64.encodestring(f.read())
		return input_encode.replace(b'\n', '')


# Retreive data field from transaction
def get_data(tx_id):
	url = "%s/api/transactions?id=%s" % (config.node, tx_id.replace("\n", ""))
	response = requests.get(url)
	json_data = response.json()
	try:
		data_field = json_data['data'][0]['asset']['data']
		return data_field
	except:
		exit("TX %s does not exist or is not valid." % tx_id)


# Build command line to create, sign and broadcast transaction
def build_cmd(data, recipient, amount):
	if recipient == None: 
		recipient = config.recipient
	if amount == None:
		amount = config.amount

	lisk_php_folder = config.lisk_php_folder
	first_passphrase = config.first_passphrase
	second_passphrase = config.second_passphrase

	return "php %slisk-cli.php SendTransaction %s %.8f \"%s\" %s \"%s\"" % (lisk_php_folder, recipient, amount, first_passphrase, second_passphrase, data)


# Confront user with a difficult choice
def brickwall():
	print "Continue? [y/n]"
	while True:
		q = raw_input("> ")
		if q.lower() == "y":
			print
			return None
		elif q.lower() == "n":
			exit("Exiting.")
		else:
			print "Can not compute."


def exit(msg):
	print msg
	sys.exit(0)


# Intro
print "------------"
print "LSK BASE-64"
print "Mode: %s" % args.mode
print "------------"


def main():
	if args.input == None:
		exit("No input specified.")
	else:
		input = args.input


	# Encode input, broadcast to network and write TX data to .lsk64 file
	if args.mode == "encode":
		# Fallback if no output is given
		if args.output == None:
			output = os.path.splitext(args.input)[0] + ".lsk64"
			print "\nNo output file specified. Results will be written to '%s'" % output
		else:
			output = args.output

		# Split base64 encode in chunks of 64 bytes and append to list
		base64_chunks = []
		for chunk in re.findall('.{1,64}', base64_encode(input)):
			base64_chunks.append(chunk)
		total_tx = len(base64_chunks)
		
		# Safety precaution
		print "\nBroadcasting '%s' (%s bytes) will require %d transaction(s) (%.1f LSK)." % (input, '{:0,}'.format(os.path.getsize(input)), total_tx, total_tx * 0.1)
		brickwall()

		# Write extension of input file to .lsk64 output
		try:
			with open(output, 'w') as f:
				f.write(os.path.splitext(args.input)[1] + "\n")
		except:
			exit("Could not write output file.")

		seq_int = 1
		for chunk in base64_chunks:
			# Build command line to create, sign and broadcast TX, and run command in subprocess
			tx = subprocess.Popen(build_cmd(chunk, args.recipient, args.amount), shell=True, stdout=subprocess.PIPE)
			# Retreive TX id from stdout
			ps_output = tx.communicate()[0]
			tx_id = re.search(r'\d{10,20}', ps_output.splitlines()[29])
			
			# Check if broadcast was succesful
			try:
				if "Transaction(s) accepted" in ps_output.splitlines()[41]:
					# Print info to screen and write data to .lsk64 file
					print "Chunk %s (%s) sent in TX %s" % (str(seq_int), chunk, tx_id.group(0))
					with open(output, 'a') as f:
						f.write(str(seq_int) + "," + tx_id.group(0) + "\n")
			except:
				exit("TX(s) could not be broadcasted.")

			seq_int += 1
		
		print "\nScript finished succesfully."
		exit("Transactions saved in '%s'." % output)


	# Decode .lsk64 files and write to output
	if args.mode == "decode":	
		with open(input, 'r') as f1:
			csv_reader = csv.reader(f1)
			# Save extension to variable and skip first line for next use
			ext = next(csv_reader)

			if args.output == None:
				output = os.path.splitext(args.input)[0] + ext[0]
				print "\nNo output specified. Decoded object will be written to '%s'" % output
				brickwall()
			else:
				output = args.output

			tx_number = 0
			encoded_object = ""	
			for line in csv_reader:
				encoded_object += get_data(line[1])
				print "Data %s retreived from TX %s" % (get_data(line[1]), line[1])
				tx_number += 1
	
		with open(output, 'wb') as f2:
			f2.write(base64.decodestring(encoded_object))

		print "\nScript finished succesfully."
		print "Total TX processed: %d" % tx_number
		exit("Decoded object saved as '%s'." % output)


if __name__ == "__main__":
	main()
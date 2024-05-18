# Jsons Library #

## What is this? ##
the module adds new features that are not available in the standard Json module

## Quick Guide ##
The module allows you to create an object of the Jsons class and work with it as with standard json
Create an instance of the Jsons class and pass the path to your JSON file
	jsons = Jsons('test.json')


----------


### Using ###



Using the library is simple:

Let's import it first:
First, import everything from the library (use the `from `...` import *` construct).

Examples of all operations:

Calculate the maximum nesting depth of JSON data using the 'max_depth' function:

	depth = jsons.max_depth()

Find all occurrences of a given value in JSON data using 'find_by_value' function:

	key_results = jsons.find_by_value('key')

Find all occurrences of a given key in JSON data using 'find_by_key' function:

	key_results = jsons.find_by_key('value')
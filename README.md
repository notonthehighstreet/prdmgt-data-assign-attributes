# Assign Attributes to Product Types

## Purpose

This script is intended to provide a way to assign existing Attributes to existing Product Types.

At this point only non-mandatory attributes are supported (not validated by this script yet) as otherwise we'd have to 
enforce default values for existing products.

It will perform some rudimentary checks of the data, as well as generating a few scripts to verify data integrity.

It is NOT designed to add new Attributes or Attribute Values, or create new Product Types (the latter can be done via this
project: https://github.com/notonthehighstreet/prdmgt-data-product-type-upload)

It is also NOT designed to replace a proper UI for the Attribute data. The responsibility for the data provided 
being correct lies with the business users providing the data NOT the engineers.


## Running the script

The script can run on Python 2.7, meaning it should work out of the box on any Mac.

Execute the following command:

    $ python assign_attributes_to_product_type.py -i <input_file>

e.g `python assign_attributes_to_product_type.py -i attribute_data.csv`

The default value for the input file is attribute_data.csv.

The script will produce 3 SQL files as output:

1. product_type_exists.sql: A data integrity check that verifies all the Product Type IDs actually exist.
2. attribute_exists.sql: A data integrity check that verifies all the Attribute IDs actually exist.
3. attribute_insert.sql: The insert statements to create the link between the Attributes and Product Types


## Basic Checks

### Missing Data

The script checks that all the data needed is provided in the CSV file. 
Only Product Type ID and Attribute ID are required but none can be missing.

If the check fails the script will exit with an error and the stakeholder who requested the change should be informed.


## Data Integrity Checks

### Product Type Exists

Script: product_type_exists.sql

To verify that all the Product Type IDs provided actually exist in the PIM database we just need to run the 
script above against the relevant environment.

If any data is returned then it means those Product Type ID(s) are invalid.

### Attribute Exists

Script: attribute_exists.sql

To verify that all the Attribute IDs provided actually exist in the PIM database we just need to run the
script above against the relevant environment.

If any data is returned then it means those Attribute ID(s) are invalid.


### Uploading the Data

Script: attribute_insert.sql

Assuming the basic/data integrity checks pass then we can copy the insert statements generated into SQL file above into 
the PIM project and apply them using the flyway migration scripts. This ensures the data will be added to all environments
in a consistent and repeatable way. An example can be seen here: https://github.com/notonthehighstreet/prdmgt-data-api/pull/1271

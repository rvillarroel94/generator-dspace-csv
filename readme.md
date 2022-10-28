Pythom Genrator for DSpace Simple Archive format from CSV Archives
====================
Takes a simple CSV spreadsheet (with sep ";") and UTF-8 Enconding, and a bunch of files and magically turns them into the DSpace Simple Archive format. 

Some simple rules: 
-------------------
* The first row should be your header, which defines the values you're going to provide. 
* First column is mandatory: 'files'. Files can be organized in any way you want, just provide the proper path relative to the CSV file's location.
* Add one column for each metadata element (eg: dc.title)
* The order of the columns does not matter.
* Only dublin core metadata elements are supported.
* Use the fully qualified dublin core name for each element (eg dc.contributor.author).
* Languages can be specified by leaving a space after the element name and then listing the language (eg dc.title en)..
* Separate multiple values for an element by double-pipes (||).

An Example: 
-----------
<table>
	<tr>
		<th>files</th>
		<th>dc.title en</th>
		<th>dc.contributor.author</th>
		<th>dc.subject</th>
		<th>dc.type</th>
	</tr>
	<tr>
		<td>black.pdf||something2.txt</td>
		<td>Title 1</td>
		<td>LASTNAME, FIRSTNAME</td>
		<td>Subject 1</td>
		<td>Report</td>
	</tr>
	<tr>
		<td>directory/something2.pdf</td>
		<td>Title 2</td>
		<td>LASTNAME1, FIRSTNAME1||LASTNAME2, FIRSTNAME2</td>
		<td>Subject 2</td>
		<td>Article</td>
	</tr>
</table>

Usage
-----
	python main.py file_to_load.csv

Importing into DSpace
---------------------
You need Administration permision for load the the Zip file generate.
Go to "Administration" in the user options, select "Content" and "Import batch file". https://your_dspace_domain/dspace-admin/batchimport

* Select "Simple Archive Format (zip file via upload).
* Select zip file to load.
* Select collection to load items.
* Click to Load buttom.
* Select "My DSpace" in the user options and view report of import batch file.
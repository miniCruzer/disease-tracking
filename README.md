# Disease Tracking

This is a disease tracking program I wrote for a studying friend of mine to
help him with his research project. Maybe it will be useful to others as well.

This program tracks disease codes with a patient count to track the number of
patients encountered with that disease.

## Usage

Upon starting for the first time, a `data.db` file will be created. You should
keep this file in the same directory as the executable, or a new one will be
created if it cannot be found.

### Increment / Decrement

Simply highlight the row(s) you wish to alter, and press either the `++` or
`--` button to decrease or increase the patient count column respectively.

### Filtering

The filter field allows for fast searching of a disease, either by disease code
or by description.

### Altering Data

Data changes are only temporary until the **Save** button is pressed. To cancel
any changes since the last **Save** (or since opening, if no save was made),
press **Undo**. This will reverse any added rows, deleted rows, or changed
rows.

#### Adding Rows

Press **Add Row** to append a blank row to the end of the list. The **Disease
Code** and **Disease Description** columns *may not* be blank, and they must
be *unique*.

### Deleting Rows

Select the row(s) you wish to delete, and press the **Delete Row** button. The
row number will change to a **!**, however the row will not be removed from the
view until **Save** is pressed.

## Importing Data

A CSV list of disease codes and descriptions/names can be imported via
**File > Import**. This file should be an RFC 4180 compliant CSV file. The
first column will be interpeted as an alphanumeric disease code, and the 2nd
column will be interpreted as the description/name. A sample file is included
in this repository.




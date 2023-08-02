import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters

client = bigtable.Client(project="serious-hall-371508", admin=True)
instance = client.instance("js-demo-single-cluster")

#print("Creating the {} table.".format("new-code-table"))
table = instance.table("new-code-table")
print("Creating column family cf1 with Max Version GC rule...")
# Create a column family with GC policy : most recent N versions
# Define the GC policy to retain only the most recent 2 versions
max_versions_rule = column_family.MaxVersionsGCRule(2)
column_family_id = "cf1"
column_families = {column_family_id: max_versions_rule}
if not table.exists():
    table.create(column_families=column_families)
else:
    print("Table {} already exists.".format("new-code-table"))


print("Writing some greetings to the table.")
greetings = ["Hello World!", "Hello Cloud Bigtable!", "Hello Python!"]
rows = []
column = "greeting".encode()
for i, value in enumerate(greetings):
    # Note: This example uses sequential numeric IDs for simplicity,
    # but this can result in poor performance in a production
    # application.  Since rows are stored in sorted order by key,
    # sequential keys can result in poor distribution of operations
    # across nodes.
    #
    # For more information about how to design a Bigtable schema for
    # the best performance, see the documentation:
    #
    #     https://cloud.google.com/bigtable/docs/schema-design
    row_key = "greeting{}".format(i).encode()
    row = table.direct_row(row_key)
    row.set_cell(
        column_family_id, column, value, timestamp=datetime.datetime.utcnow()
    )
    rows.append(row)
table.mutate_rows(rows)
# [START bigtable_hw_create_filter]
    # Create a filter to only retrieve the most recent version of the cell
    # for each column across entire row.
row_filter = row_filters.CellsColumnLimitFilter(1)
    # [END bigtable_hw_create_filter]

    # [START bigtable_hw_get_with_filter]
    # [START bigtable_hw_get_by_key]
print("Getting a single greeting by row key.")
key = "greeting0".encode()

row = table.read_row(key, row_filter)
cell = row.cells[column_family_id][column][0]
print(cell.value.decode("utf-8"))
    # [END bigtable_hw_get_by_key]
    # [END bigtable_hw_get_with_filter]

    # [START bigtable_hw_scan_with_filter]
    # [START bigtable_hw_scan_all]
print("Scanning for all greetings:")
partial_rows = table.read_rows(filter_=row_filter)

for row in partial_rows:
    cell = row.cells[column_family_id][column][0]
    print(cell.value.decode("utf-8"))
    # [END bigtable_hw_scan_all]
    # [END bigtable_hw_scan_with_filter]
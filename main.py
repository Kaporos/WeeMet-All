import sys
import os
print(sys.argv)
if len(sys.argv) < 2:
    import animated
else:
    import csv_generate
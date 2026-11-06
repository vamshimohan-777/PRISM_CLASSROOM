"""Start every test session from empty databases.

The test modules seed into SQLite files in the working directory. Seeding only adds
what is missing, so a file left by an earlier run keeps its old rows, and a change to
seed data then fails tests for no reason visible in the code. Removing the files here
runs before any test module imports the application.
"""
import glob
import os

for leftover in glob.glob("test*.db"):
    try:
        os.remove(leftover)
    except OSError:
        pass  # Windows can hold a handle briefly; the run still seeds what it needs.

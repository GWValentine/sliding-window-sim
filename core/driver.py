import csv

with open("config/config1.txt") as f:
    reader = csv.DictReader(f)
    for row in reader:
        time = int(row["time"])
        cmd = row["cmd"]
        ID = row["ID"]
        loseFrame = row["loseFrame"] == "true"
        loseAck = row["loseACK"] == "true"
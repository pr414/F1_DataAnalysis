import csv

def transform_time(input_csv, output_csv):
    def parse_time_to_seconds(time_str):
        if "+" in time_str:  # Gap time, like "+minutes:seconds.milliseconds" or "+seconds.milliseconds"
            time_str = time_str[1:]  # Remove the '+' sign
        parts = time_str.split(":")
        if len(parts) == 2:  # Format: "minutes:seconds.milliseconds"
            minutes, seconds = map(float, parts)
            return round(minutes * 60 + seconds, 3)
        elif len(parts) == 1:  # Format: "seconds.milliseconds"
            return round(float(parts[0]), 3)
        else:
            raise ValueError(f"Unexpected time format: {time_str}")

    def winner_time_to_seconds(winner_time):
        parts = winner_time.split(":")
        if len(parts) == 3:  # Format: "hours:minutes:seconds.milliseconds"
            hours, minutes, seconds = map(float, parts)
            return round(hours * 3600 + minutes * 60 + seconds, 3)
        elif len(parts) == 2:  # Format: "minutes:seconds.milliseconds"
            minutes, seconds = map(float, parts)
            return round(minutes * 60 + seconds, 3)
        else:
            raise ValueError(f"Unexpected winner time format: {winner_time}")

    with open(input_csv, mode="r", newline="", encoding="utf-8") as infile, \
         open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row["time"] == "\\N":  # Skip rows where the driver has retired or been lapped
                writer.writerow(row)
                continue

            if row["positionOrder"] == "1":  # For the winner
                winner_time = row["time"]
                winner_seconds = winner_time_to_seconds(winner_time)
                row["time"] = winner_seconds
            else:  # For other drivers
                gap_time = row["time"]
                try:
                    gap_seconds = parse_time_to_seconds(gap_time)
                    row["time"] = round(winner_seconds + gap_seconds, 3)  # Add the gap to the winner's total time
                except ValueError as e:
                    print(f"Skipping row with invalid time format: {row}")
                    continue

            writer.writerow(row)

# Example usage
input_csv_path = "f1_data/results.csv"  # Replace with your input file name
output_csv_path = "f1_results_transformed.csv"  # Replace with desired output file name
transform_time(input_csv_path, output_csv_path)

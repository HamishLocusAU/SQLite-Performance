DISCLAIMER: This repo is mostly AI written

# SQLite Performance Comparison: Check Constraints

This project benchmarks the performance impact of using check constraints in SQLite tables. It creates two databases—one with constraints and one without—and measures the time taken to insert a large number of rows into each.

## Features
- Table schema with integer, string, status, email, and ISO datetime fields
- Check constraints for value ranges, string length, allowed status values, email format, and datetime format
- Automated timing and summary output

## Usage

1. Ensure you have Python 3 installed.
2. Run the benchmark script:
   ```powershell
   python sqlite_performance_compare.py
   ```
3. View the timing results in the console.

## Files
- `sqlite_performance_compare.py`: Main benchmarking script
- `README.md`: Project documentation

## Customization
- Change `NUM_ROWS` in the script to adjust the number of rows inserted.
- Modify constraints or add more fields as needed for your own tests.

## License
MIT

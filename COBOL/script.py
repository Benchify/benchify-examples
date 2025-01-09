import subprocess
import csv
import shutil
import os
from dataclasses import dataclass
from typing import List, Tuple
import platform

@dataclass
class EmployeeRecord:
    emp_id: str
    hours_worked: float
    hourly_rate: float
    tax_deduction: float

def install_cobc_and_compile_script():
    """Installs GNU COBOL if it's not already installed."""
    if shutil.which("cobc") is None:
        print("GNU COBOL (cobc) is not installed. Installing it now...")
        try:
            os_name = platform.system()
            if os_name == "Linux":
                distro = platform.linux_distribution()[0].lower()
                if "ubuntu" in distro or "debian" in distro:
                    subprocess.run(["apt", "install", "-y", "gnucobol"], check=True)
                elif "fedora" in distro or "centos" in distro:
                    subprocess.run(["dnf", "install", "-y", "gnucobol"], check=True)
                elif "arch" in distro:
                    subprocess.run(["pacman", "-S", "--noconfirm", "gnucobol"], check=True)
                else:
                    raise Exception("Unsupported Linux distribution. Please install GNU COBOL manually.")
            elif os_name == "Darwin":  # macOS
                subprocess.run(["brew", "install", "gnucobol"], check=True)
            elif os_name == "Windows":
                raise Exception("Please install GNU COBOL manually on Windows.")
            else:
                raise Exception("Unsupported operating system. Please install GNU COBOL manually.")
        except subprocess.CalledProcessError as e:
            print("Failed to install GNU COBOL. Please install it manually.")
            raise e
    else:
        print("GNU COBOL (cobc) is already installed.")
    
    if not os.path.exists("payroll.cbl"):
        raise FileNotFoundError("The COBOL script 'payroll.cbl' was not found.")
    
    if not os.path.exists("payroll"):
        print("Compiling payroll.cbl...")
        compile_command = ["cobc", "-x", "-o", "payroll", "payroll.cbl"]
        try:
            subprocess.run(compile_command, check=True)
            print("Compilation successful.")
        except subprocess.CalledProcessError as e:
            print("Error compiling COBOL script.")
            raise e
    else:
        print("Using existing compiled payroll program.")

def process_payroll_cobol(employee_records: List[EmployeeRecord]) -> List[Tuple[float, float]]:
    """Compiles and runs the COBOL payroll script, then processes its output."""
    # Ensure GNU COBOL is installed
    install_cobc_and_compile_script()

    # Create temporary input file with random name
    temp_file = f"temp_payroll_input_{os.urandom(8).hex()}.csv"
    with open(temp_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['EMP-ID', 'HOURS-WORKED', 'HOURLY-RATE', 'TAX-DEDUCTION'])
        for record in employee_records:
            writer.writerow([record.emp_id, record.hours_worked, record.hourly_rate, record.tax_deduction])

    try:
        # Run the compiled COBOL program with the input file name as an argument
        print("Running the COBOL payroll program...")
        run_command = ["./payroll", temp_file]
        try:
            result = subprocess.run(run_command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running COBOL program. Exit code: {e.returncode}")
            print(f"Command that failed: {' '.join(e.cmd)}")
            print("Standard output:")
            print(e.stdout if e.stdout else "<no output>")
            print("Standard error:")
            print(e.stderr if e.stderr else "<no error output>")
            print(f"Input file contents:")
            with open(temp_file, 'r') as f:
                print(f.read())
            raise e

        # Process the COBOL output
        print("Processing COBOL output...")
        output_lines = result.stdout.splitlines()
        if not output_lines:
            raise ValueError("COBOL program produced no output")
            
        reader = csv.DictReader(output_lines)
        if not reader.fieldnames:
            raise ValueError(f"Invalid CSV output format. Raw output:\n{result.stdout}")

        results = []
        for row in reader:
            try:
                emp_id = row["EMP-ID"]
                gross_pay = float(row["GROSS-PAY"])
                net_pay = float(row["NET-PAY"])
                
                # Display results
                print(f"Employee ID: {emp_id}")
                print(f"Gross Pay: ${gross_pay:.2f}")
                print(f"Net Pay: ${net_pay:.2f}")
                
                # Append to results
                results.append((gross_pay, net_pay))
            except KeyError as e:
                raise ValueError(f"Missing required column in output: {e}. Available columns: {reader.fieldnames}")
            except ValueError as e:
                raise ValueError(f"Invalid number format in output for employee {emp_id}: {e}")
        
        return results

    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Modernized version of process_payroll_cobol.  This is meant to produce exactly the same
# result, but in Python.
def process_payroll(employee_records: List[EmployeeRecord]) -> List[Tuple[float, float]]:
    """Processes payroll directly using Python logic."""
    results = []
    for record in employee_records:
        # Calculate gross pay and net pay
        gross_pay = record.hours_worked * record.hourly_rate
        net_pay = gross_pay - record.tax_deduction
        
        # Display results
        print(f"Employee ID: {record.emp_id}")
        print(f"Net Pay: ${net_pay:.2f}")

        results.append((gross_pay, net_pay))

    return results
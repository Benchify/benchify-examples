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
    
    # Always recompile to ensure we have the latest version
    if os.path.exists("payroll"):
        os.remove("payroll")
    print("Compiling payroll.cbl...")
    compile_command = ["cobc", "-x", "-o", "payroll", "payroll.cbl"]
    try:
        subprocess.run(compile_command, check=True)
        print("Compilation successful.")
    except subprocess.CalledProcessError as e:
        print("Error compiling COBOL script.")
        raise e

def format_pic_9_5_v_99(num: float) -> str:
    """
    For PIC 9(5)V99, we need 7 numeric digits total, with an implied
    decimal point before the last two digits. Example:
      20.0 -> 20.00 -> multiply by 100 = 2000 -> zero-pad to 7 -> "0002000"
    """
    # Multiply by 100, round, then zero-pad to length=7
    value_as_int = int(round(num * 100))
    return f"{value_as_int:07d}"

def process_payroll_cobol(employee_records: List[EmployeeRecord]) -> List[Tuple[float, float]]:
    """Compiles and runs the COBOL payroll script, then processes its output."""

    # 1) Ensure GNU COBOL is installed & compile the COBOL code
    install_cobc_and_compile_script()

    # 2) Create a temporary input file with random name
    temp_file = f"temp_payroll_input_{os.urandom(8).hex()}.txt"

    # 3) Write data in the fixed-length format
    print("=== Debug: Writing the following lines to input file ===")
    with open(temp_file, 'w', newline='') as f:
        for record in employee_records:
            # EMP-ID: 5 chars
            emp_id_str = record.emp_id[:5].ljust(5)

            # HOURS: 3 digits
            hours_str = f"{int(record.hours_worked):03d}"

            # HOURLY-RATE: 7 digits
            hourly_rate_str = format_pic_9_5_v_99(record.hourly_rate)

            # TAX-DEDUCTION: 7 digits
            tax_deduction_str = format_pic_9_5_v_99(record.tax_deduction)

            line = emp_id_str + hours_str + hourly_rate_str + tax_deduction_str
            print(line)  # Print for debug
            f.write(line + "\n")
    print("=======================================================")

    # 4) Run the compiled COBOL program with the input file as an argument
    print(f"Running the COBOL payroll program with file: {temp_file}")
    run_command = ["./payroll", temp_file]

    try:
        result = subprocess.run(run_command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running COBOL program. Exit code: {e.returncode}")
        print(f"Command that failed: {' '.join(e.cmd)}")
        print("=== Standard output ===")
        print(e.stdout if e.stdout else "<no output>")
        print("=== Standard error ===")
        print(e.stderr if e.stderr else "<no error output>")
        print("=== Input file contents ===")
        with open(temp_file, 'r') as input_f:
            print(input_f.read())
        raise e

    # 5) Process the COBOL output
    print("Processing COBOL output...")
    output_lines = result.stdout.splitlines()
    if not output_lines:
        print("=== No output from COBOL ===")
        return []

    print("=== Raw COBOL Output ===")
    for line in output_lines:
        print(line)
    print("=========================")

    # The first line should be: "EMP-ID,GROSS-PAY,NET-PAY"
    reader = csv.DictReader(output_lines)
    if not reader.fieldnames or "EMP-ID" not in reader.fieldnames:
        print(f"=== Invalid CSV output format ===\n{result.stdout}")
        return []

    results = []
    for row in reader:
        try:
            emp_id = row["EMP-ID"]
            gross_pay = float(row["GROSS-PAY"])
            net_pay = float(row["NET-PAY"])
            
            # Debug prints
            print(f"Employee ID: {emp_id}")
            print(f"Gross Pay:  ${gross_pay:.2f}")
            print(f"Net Pay:    ${net_pay:.2f}")
            results.append((gross_pay, net_pay))
        except KeyError as e:
            print(f"Missing required column in output: {e}. Available columns: {reader.fieldnames}")
        except ValueError as e:
            print(f"Invalid number format in output for employee {emp_id}: {e}")

    return results

# Modernized version of process_payroll_cobol.  This is meant to produce exactly
# the same result, but in Python.
def process_payroll(employee_records: List[EmployeeRecord]) -> List[Tuple[float, float]]:
    """Processes payroll directly using Python logic."""
    results = []
    for record in employee_records:
        # Calculate gross pay and net pay
        gross_pay = record.hours_worked * record.hourly_rate
        net_pay = gross_pay - record.tax_deduction
        
        # Display results
        print(f"Employee ID: {record.emp_id}")
        print(f"Gross Pay: ${gross_pay:.2f}")
        print(f"Net Pay:   ${net_pay:.2f}")

        results.append((gross_pay, net_pay))

    return results

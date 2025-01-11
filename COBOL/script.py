import subprocess
import csv
import shutil
import os
from dataclasses import dataclass
from typing import List, Tuple
import platform
import math

@dataclass
class EmployeeRecord: # Class for EmployeeRecords
    """
    Data class representing an employee's payroll record.
    
    Attributes:
        emp_id: Employee ID string
        hours_worked: Number of hours worked in pay period
        hourly_rate: Pay rate per hour
        tax_deduction: Amount to deduct for taxes
    """
    emp_id: str
    hours_worked: float # cannot be an inf or NaN
    hourly_rate: float # cannot be an inf or NaN
    tax_deduction: float # cannot be an inf or NaN

def install_cobc_and_compile_script():
    """
    Installs GNU COBOL compiler if not present and compiles the COBOL payroll script.
    
    This function:
    1. Checks if cobc compiler is installed
    2. If not installed, attempts to install it using the appropriate package manager
    3. Compiles payroll.cbl into an executable
    
    Raises:
        FileNotFoundError: If payroll.cbl is missing
        subprocess.CalledProcessError: If installation or compilation fails
        Exception: If on an unsupported OS or Linux distribution
    """
    if shutil.which("cobc") is None:
        print("GNU COBOL (cobc) is not installed. Installing it now...")
        try:
            os_name = platform.system()
            if os_name == "Linux":
                try:
                    distro = platform.linux_distribution()[0].lower()
                except AttributeError:
                    distro = "ubuntu"
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
    
    # Get the directory where this script resides
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cobol_script_path = os.path.join(script_dir, "payroll.cbl")
    
    if not os.path.exists(cobol_script_path):
        raise FileNotFoundError(f"The COBOL script 'payroll.cbl' was not found in {script_dir}")
    
    # Always recompile to ensure we have the latest version
    output_path = os.path.join(script_dir, "payroll")
    if os.path.exists(output_path):
        os.remove(output_path)
    print("Compiling payroll.cbl...")
    compile_command = ["cobc", "-x", "-o", output_path, cobol_script_path]
    try:
        subprocess.run(compile_command, check=True)
        print("Compilation successful.")
    except subprocess.CalledProcessError as e:
        print("Error compiling COBOL script.")
        raise e

install_cobc_and_compile_script()

def format_pic_9_5_v_99(num: float) -> str: # Function to format data for cobol ingestion
    """
    Formats a number according to COBOL's PIC 9(5)V99 format specification.
    
    This creates a 7-digit string where the last 2 digits represent decimal places.
    The decimal point is implied (not actually present in output).
    
    Args:
        num: The float number to format
        
    Returns:
        A 7-character string with leading zeros
        
    Example:
        20.0 -> "0002000" (represents 20.00)
        15.50 -> "0001550" (represents 15.50)
        
    Raises:
        ValueError: If num is NaN, Inf, -Inf, or would result in a number too large
                   to represent in PIC 9(5)V99 format
    """ 
    if math.isnan(num):
        raise ValueError("Input cannot be NaN")
        
    if math.isinf(num):
        raise ValueError("Input cannot be infinite")
        
    # Check range - PIC 9(5)V99 can only handle 0 to 99999.99
    if num < 0 or num > 99999.99:
        raise ValueError("Number out of range for PIC 9(5)V99 format (0 to 99999.99)")

    try:
        # Multiply by 100, round, then zero-pad to length=7
        value_as_int = int(round(num * 100))
        return f"{value_as_int:07d}"
    except OverflowError:
        raise ValueError("Number too large to represent in PIC 9(5)V99 format")

def process_payroll_cobol(employee_records: List[EmployeeRecord]) -> List[Tuple[float, float]]:
    """
    Processes payroll by running a COBOL program and parsing its output.
    
    This function:
    1. Ensures COBOL compiler is installed
    2. Creates a temporary input file with employee data
    3. Runs the COBOL payroll program
    4. Parses the CSV output to extract gross and net pay
    
    Args:
        employee_records: List of EmployeeRecord objects containing payroll data
        
    Returns:
        List of tuples containing (gross_pay, net_pay) for each employee
        
    Raises:
        Various exceptions from subprocess calls and file operations
    """
    # 1) Ensure GNU COBOL is installed & compile the COBOL code
    install_cobc_and_compile_script()

    # 2) Create a temporary input file with random name
    temp_file = f"temp_payroll_input_{os.urandom(8).hex()}.txt"

    # 3) Write data in the fixed-length format
    print("=== Debug: Writing the following lines to input file ===")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_file_path = os.path.join(script_dir, temp_file)
    with open(temp_file_path, 'w', newline='') as f:
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
    print(f"Running the COBOL payroll program with file: {temp_file_path}")
    run_command = ["./payroll", temp_file_path]

    try:
        result = subprocess.run(run_command, capture_output=True, text=True, check=True, cwd=script_dir)
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

def process_payroll(employee_records: List[EmployeeRecord]) -> List[Tuple[float, float]]: 
    """ 
    Pure Python implementation of the COBOL payroll processing logic.
    
    This function performs the same calculations as the COBOL program but in Python.
    It should perform the exact same result as process_payroll_cobol on all possible inputs,
    and throw the same exceptions in the same scenarios.
    
    Args:
        employee_records: List of EmployeeRecord objects containing payroll data
    
    Returns:
        List of tuples containing (gross_pay, net_pay) for each employee
    
    PLEASE TEST THIS PROPERTY ONLY:
        
        Results should exactly match process_payroll_cobol() output, including thrown exceptions. 
        IE, for all ers: List[EmployeeRecord], process_payroll(er) == process_payroll_cobol(er),
        unless either side throws an Exception, in which case the other side should throw an identical
        exception.

    --> Limit employee_records to 1-10 records for testing, as in the real world there will never be more than 10. 
    
    --> Please do NOT bother testing any other properties of this function.
    """
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
    
    return results # this SHOULD return the same result as process_payroll_cobol(employee_records)

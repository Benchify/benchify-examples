# Code Modernization

Astonishingly, 70% of all existing business logic is in COBOL, and 800 billion lines of COBOL are still in use in industry today [1].
Many (perhaps all) companies that still use COBOL wish they could move off it, since it is massively antiquated and the only living engineers who still know it are in retirement homes.  Obviously, LLMs present a compelling solution to this problem via automated translation.  But how can you be sure the translation is correct?  This demo is meant to illustrate how Benchify can fit into the analysis of a translation from COBOL to Python.

You can see the complete report [here](https://github.com/Benchify/benchify-examples/pull/134).

Example usage of the COBOL wrapper:
```
ipython3
Python 3.9.6 (default, Nov 11 2024, 03:15:38) 
Type 'copyright', 'credits' or 'license' for more information
IPython 8.18.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from script import *
   ...: install_cobc_and_compile_script()
   ...: 
   ...: employee_records = [
   ...:     EmployeeRecord(emp_id="12345", hours_worked=40, hourly_rate=20.0, tax_deduction=50.0),
   ...:     EmployeeRecord(emp_id="67890", hours_worked=35, hourly_rate=15.0, tax_deduction=30.0),
   ...:     EmployeeRecord(emp_id="54321", hours_worked=45, hourly_rate=25.0, tax_deduction=70.0)
   ...: ]
   ...: 
   ...: payroll_results = process_payroll_cobol(employee_records)
   ...: payroll_results
GNU COBOL (cobc) is already installed.
Compiling payroll.cbl...
Compilation successful.
GNU COBOL (cobc) is already installed.
Compiling payroll.cbl...
Compilation successful.
=== Debug: Writing the following lines to input file ===
1234504000020000005000
6789003500015000003000
5432104500025000007000
=======================================================
Running the COBOL payroll program with file: temp_payroll_input_ceacb40a807b19a0.txt
Processing COBOL output...
=== Raw COBOL Output ===
EMP-ID,GROSS-PAY,NET-PAY
12345,0000800.00,0000750.00
67890,0000525.00,0000495.00
54321,0001125.00,0001055.00
=========================
Employee ID: 12345
Gross Pay:  $800.00
Net Pay:    $750.00
Employee ID: 67890
Gross Pay:  $525.00
Net Pay:    $495.00
Employee ID: 54321
Gross Pay:  $1125.00
Net Pay:    $1055.00
Out[1]: [(800.0, 750.0), (525.0, 495.0), (1125.0, 1055.0)]

In [2]: payroll_results_2 = process_payroll(employee_records)
Employee ID: 12345
Gross Pay: $800.00
Net Pay:   $750.00
Employee ID: 67890
Gross Pay: $525.00
Net Pay:   $495.00
Employee ID: 54321
Gross Pay: $1125.00
Net Pay:   $1055.00

In [3]: payroll_results_2
Out[3]: [(800.0, 750.0), (525.0, 495.0), (1125.0, 1055.0)]

In [4]: payroll_results_2 == payroll_results
Out[4]: True

In [5]: exit()
```

[1]: https://cobolcowboys.com/cobol-today/#:~:text=70%25%20of%20all%20critical%20business,use%20today%20by%20various%20industries.
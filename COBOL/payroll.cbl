       $set sourceformat"free"
       IDENTIFICATION DIVISION.
       PROGRAM-ID. PAYROLL.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT EMPLOYEE-FILE ASSIGN TO DYNAMIC-FILE-NAME
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS FILE-STATUS.

       DATA DIVISION.
       FILE SECTION.
       FD EMPLOYEE-FILE
          LABEL RECORDS ARE STANDARD
          BLOCK CONTAINS 0 RECORDS
          DATA RECORD IS EMPLOYEE-RECORD.
       01 EMPLOYEE-RECORD.
           05 EMP-ID              PIC X(5).
           05 HOURS-WORKED        PIC 9(3).
           05 HOURLY-RATE         PIC 9(5)V99.
           05 TAX-DEDUCTION       PIC 9(5)V99.

       WORKING-STORAGE SECTION.
       01 GROSS-PAY              PIC 9(7)V99.
       01 NET-PAY                PIC 9(7)V99.
       01 END-OF-FILE            PIC X VALUE SPACE.
       01 DYNAMIC-FILE-NAME      PIC X(100).
       01 FILE-STATUS            PIC XX.

       PROCEDURE DIVISION.

       *> Retrieve the first argument with C$GETARG
           CALL "C$GETARG" USING
               BY VALUE 1
               BY REFERENCE DYNAMIC-FILE-NAME
       *> Debug: see what we got
           DISPLAY "DEBUG: DYNAMIC-FILE-NAME = [" DYNAMIC-FILE-NAME "]"

       *> Now open the file using DYNAMIC-FILE-NAME
           OPEN INPUT EMPLOYEE-FILE
           DISPLAY "DEBUG: FILE-STATUS AFTER OPEN = " FILE-STATUS
           IF FILE-STATUS NOT = "00"
               DISPLAY "Error opening file: " DYNAMIC-FILE-NAME
               STOP RUN
           END-IF

       *> Output CSV Header
           DISPLAY "EMP-ID,GROSS-PAY,NET-PAY"

       *> Read until EOF
           PERFORM UNTIL END-OF-FILE = "EOF"
               READ EMPLOYEE-FILE INTO EMPLOYEE-RECORD
                   AT END
                       MOVE "EOF" TO END-OF-FILE
                   NOT AT END
                       *> Debug: Show raw data
                       DISPLAY "DEBUG: Raw record read = ["
                               EMP-ID HOURS-WORKED HOURLY-RATE TAX-DEDUCTION "]"

                       COMPUTE GROSS-PAY = HOURS-WORKED * HOURLY-RATE
                       COMPUTE NET-PAY = GROSS-PAY - TAX-DEDUCTION
                       DISPLAY EMP-ID "," GROSS-PAY "," NET-PAY
               END-READ
           END-PERFORM

           CLOSE EMPLOYEE-FILE
           STOP RUN.

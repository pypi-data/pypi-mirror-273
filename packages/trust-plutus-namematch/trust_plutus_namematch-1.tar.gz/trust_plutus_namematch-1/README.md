#### Assumptions: 
1. Column name for Miles and ICRA sheet is "Fund Name"
2. Input and Output file names don't have spaces
3. Sheet names are : "Miles Names" and "ICRA Names"

#### Example: 

from trust_plutus_namematch.match import NameMatch

nm = NameMatch()

inputPath = "C:\\Users\\username\\Documents\\SchemeNamesDump.xlsx"

outputPath = "C:\\Users\\username\\Documents\\Result.xlsx"

nm.run(inputPath,outputPath)

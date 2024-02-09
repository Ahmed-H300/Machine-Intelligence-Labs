# Create a new file or clear the existing one
New-Item -Path .\output.txt -ItemType File -Force

# Run the command 20 times
for ($i=0; $i -lt 20; $i++) {
    # Run the command and append the output to the file
    python autograder.py -q 4 | Out-File -Append -FilePath .\output.txt
}
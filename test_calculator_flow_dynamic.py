import subprocess
import unittest
import os
import glob

class TestCalculatorEndToEnd(unittest.TestCase):
    def clean_output(self, output):
        lines = output.strip().splitlines()
        if lines and lines[-1].strip() == "Press Enter to exit...":
            lines.pop()
        return "\n".join(lines).strip()

    def run_case(self, case_id):
        input_path = f'inputs/case{case_id}.txt'

        with open(input_path,'r') as input_file:
            python_result = subprocess.run(
                ['python', '212150841_325047801.py'], #<---- your script name here
                stdin=input_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        with open(input_path, 'r') as input_file:
            exe_result = subprocess.run(
                ['calculator.exe'],
                stdin=input_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        python_output = self.clean_output(python_result.stdout)
        exe_output = self.clean_output(exe_result.stdout)

        self.assertEqual(
            python_output,
            exe_output,
            msg=f"Mismatch in case {case_id}"
        )

# Dynamically generate test methods
def generate_test(case_id):
    def test(self):
        self.run_case(case_id)
    return test

# Automatically detect all input cases
input_files = glob.glob('inputs/case*.txt')
for file in input_files:
    case_number = os.path.splitext(os.path.basename(file))[0].replace('case', '')
    test_name = f'test_case_{case_number}'
    setattr(TestCalculatorEndToEnd, test_name, generate_test(case_number))

if __name__ == '__main__':
    unittest.main()

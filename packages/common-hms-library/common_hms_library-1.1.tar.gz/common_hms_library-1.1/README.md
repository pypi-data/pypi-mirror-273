step 1: First go to the virtual environment: 

Step 2: Ensure you have setuptools and wheel installed. If not, you can install them using pip:

=> pip install setuptools wheel

Step 3: Navigate to the directory containing your Python package (common_hms_library). Assuming your package is located at /home/softprime/wrk/17/softprime_hms_basic/common_hms_library, you can navigate there using the cd command:

=> cd /home/softprime/wrk/17/softprime_hms_basic/common_hms_library

step 4: Once you're in the correct directory, run the following command to build the distribution package:

=> python setup.py sdist bdist_wheel

Step 5: After successfully building the distribution package, navigate to the dist directory:

=> cd dist

step 6: In the dist directory, install the package using pip:

=> pip install common_hms_library-0.1-py3-none-any.whl





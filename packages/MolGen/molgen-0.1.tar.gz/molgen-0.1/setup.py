from setuptools import setup, find_packages

# Step 1: Read the `requirements.txt` file
with open('requirements.txt') as f:
    requirements = f.readlines()

# Step 2: Clean up the list by stripping whitespace
requirements = [r.strip() for r in requirements]

setup(
    name='MolGen',
    version='0.1',
    description='A Molecular Generation Framework package',
    author='Your Name',
    author_email='vinaysanjay.chaudhari@slu.edu',
    # Uncomment the following lines as needed
    #url='https://github.com/yourusername/MolGen',
    packages=find_packages(),
    install_requires=requirements,  # Use the requirements from `requirements.txt`
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
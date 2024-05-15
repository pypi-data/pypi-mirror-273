from setuptools import setup, find_packages

setup(
    name='HE_Data',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    package_data={'HE_Data': ['*.csv']},
    install_requires=[
        'pandas',  # Ensure pandas is installed with your package
    ],
    author='Gurucharan Raju',
    author_email='Gurucharan.Raju-SA@csulb.edu',
    description='A simple package containing a CSV dataset',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)

from setuptools import setup, find_packages

setup(
    name='montcarlo', 
    description='Monte Carlo simulation framework',  
    author='Zahra Nouri', 
    author_email='zahranouri@email.virginia.edu',  
    url='https://github.com/ZahraaNouri/MonteCarloSimulation',  
    packages=find_packages(), 
    install_requires=[
        'numpy',
        'pandas'
    ],  
    python_requires='>=3.6',  # Minimum Python version requirement
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

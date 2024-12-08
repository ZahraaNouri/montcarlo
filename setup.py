from setuptools import setup, find_packages

setup(
    name='montecarlo',
    version='1.0.0',
    description='Monte Carlo simulation framework',
    author='Zahra Nouri',
    author_email='zahranouri@email.virginia.edu',
    url='https://github.com/ZahraaNouri/MonteCarloSimulation',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    python_requires='>=3.6',
)

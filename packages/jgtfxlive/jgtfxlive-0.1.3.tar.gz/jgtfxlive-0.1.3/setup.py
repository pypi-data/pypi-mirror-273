from setuptools import setup, find_packages

setup(
    name='jgtfxlive',
    version='0.1.3',
    author="GUillaume Isabelle",
    author_email="jgi@jgwill.com",
    url="https://github.com/jgwill/jgtfxlive",
    description='A Python module for live chart data export',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jgtfxlive = jgtfxlive.ptoLiveChartDataExport.LiveChartDataExport:main',
            'jgtfxliveconf = jgtfxlive.config_generator:main'
        ]
    },
    install_requires=[
      'jgtutils',
      'forexconnect',
        # Add any dependencies required by your module here
    ],
)
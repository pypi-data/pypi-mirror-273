import shutil
from setuptools import setup, find_packages, Command

with open('./requirements.package.list', 'r') as f:
    requirements = f.read().splitlines()

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        for directory in ['build', 'dist', 'fidat.egg-info']:
            try:
                shutil.rmtree(directory)
            except OSError:
                pass

setup(
    name='fidat', # Framework for Intelligent Data Analysis and Trends
    version='0.1.0',
    packages=find_packages(include=['fidat', 'fidat.*']),
    install_requires=requirements,
    description="Framework for Intelligent Data Analysis and Trends",
    long_description=open('./README.md').read(),
    long_description_content_type='text/markdown',
    author='Andy Hawkins',
    author_email='projects@hawkins.tech',
    keywords=[
        'data analysis', 'trend analysis', 'data assimilation', 'data visualization',
        'statistical analysis', 'time series', 'predictive modeling', 'machine learning',
        'data mining', 'big data', 'forecasting', 'pattern recognition', 'business intelligence',
        'data science', 'quantitative analysis', 'financial analysis', 'market analysis',
        'economic forecasting', 'data aggregation', 'data trends'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    maintainer='Hawkins.Tech Inc',
    maintainer_email='projects@hawkins.tech',
    cmdclass={
        'clean': CleanCommand,
    }
)
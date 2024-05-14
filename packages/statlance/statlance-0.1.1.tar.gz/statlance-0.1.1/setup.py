from setuptools import setup, find_packages

# Read the content of the LICENSE file
with open('LICENSE.md', 'r', encoding='utf-8') as license_file:
    license_text = license_file.read()

setup(
    name='statlance',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pygwalker==0.4.8.1',
        'openpyxl',
        'numpy',
        'pandas',
        'scikit-learn',
        'seaborn',
        'matplotlib',
        'xgboost',
        'joblib',
        'sqlalchemy',
        'plotly'
        # Add any other dependencies here
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    entry_points={
        'console_scripts': [
            'statlance = statlance.__main__:main'
        ]
    },
    author='Databulance',
    author_email='admin@databulance.com',
    description='A Python library for EDA, visualization, and dashboarding',
    long_description=license_text,
    long_description_content_type='text/markdown',  # Adjusted content type
    url='https://github.com/databulance/statlance',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)

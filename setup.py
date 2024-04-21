from setuptools import setup, find_packages

# ASCII art
art = """
 ____                           ____     __                               
/\  _`\                        /\  _`\  /\ \                __            
\ \ \/\_\     __     _ __    __\ \ \/\_\\ \ \___      __   /\_\    ___    
 \ \ \/_/_  /'__`\  /\`'__\/'__`\ \ \/_/_\ \  _ `\  /'__`\ \/\ \ /' _ `\  
  \ \ \L\ \/\ \L\.\_\ \ \//\  __/\ \ \L\ \\ \ \ \ \/\ \L\.\_\ \ \/\ \/\ \ 
   \ \____/\ \__/.\_\\ \_\\ \____\\ \____/ \ \_\ \_\ \__/.\_\\ \_\ \_\ \_\
    \/___/  \/__/\/_/ \/_/ \/____/ \/___/   \/_/\/_/\/__/\/_/ \/_/\/_/\/_/
                                                                          
                                                                          
"""

setup(
    name='CareChain',
    version='1.0.0',
    author='Bellante Luca, Coccia Giansimone, D’Anna Alessandra, Di Sabatino Walter, Ferretti Laura',
    description=art + '\n\nIn the increasingly digital context of healthcare, effective management and secure access to health data become fundamental to ensure efficient and personalized care. Our project aims to address this challenge through the implementation of an innovative system based on advanced technologies such as Python and Ganache, enabling secure and efficient interaction among doctors, patients, and healthcare workers, promoting telemedicine, and improving access to healthcare.',
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'python-dotenv',
        'solc-select',
        'py-solc-x',
        'slither',
        'bandit',
        'web3',
        'python-abc',
        'keyboard',
        'Faker',
        'mysql-connector-python'
    ],
    entry_points={
        'console_scripts': [
            'CareChain = main:__main__',
        ],
    },

    long_description=art
)


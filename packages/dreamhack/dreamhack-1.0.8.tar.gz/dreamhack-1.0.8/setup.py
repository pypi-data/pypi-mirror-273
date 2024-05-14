from setuptools import setup, find_packages
#type:ignore

VERSION = '1.0.8' 
DESCRIPTION = 'The ultimate PyPi package for cyber-security and many other things.'
LONG_DESCRIPTION = '''The ultimate PyPi package for cyber-security, encryption, and many other things to simplify your code and make more advanced programs.

*DISCLAIMER:* I am not responsible for any damages caused by this package. Please do not use any features of this package for any malicious purposes. 

RELEASE NOTES: \n
v1.0.8: \n
- Added new features to GUI and Windows classes \n
- Fixed a few bugs \n

v1.0.7: \n
- Added new features to the registry class \n
- Added a computer stats class \n
- Refresh explorer.exe when registry is edited \n

v1.0.6: \n
- Fixed a critical error with the registry class \n
- Added message box function to the gui class \n

v1.0.5: \n
- Added new features to GUI class \n
- Added new RegistryEditor class (For Windows only, experimental phase) \n

v1.0.4: \n
- Fixed a few bugs \n
- Added a few more features \n

v1.0.3: \n
- Added logging content \n
- Added the ability to get the public ip of the current machine \n
- Added lots of new features \n
- A few bug fixes \n

v1.0.2: \n
- First official stable version, DO NOT USE PREVIOUS VERSIONS \n
- Added content to encryption and logging \n
- Created networking \n
\n
WARNING: VERSIONS BELOW THIS NOTE ARE UNSTABLE. DO NOT USE THEM.
\n
v1.0.1: \n
- Fixed critical error from v1.0.0 \n
- Working on new version \n

v1.0.0: \n
- Initial release \n
- NOTE: Encryption and logging are both empty for the first few versions. \n
'''
#type:ignore

setup(
        name="dreamhack", 
        version=VERSION,
        author="Jack Burr",
        author_email="BurrJ22@Outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['cryptography', 'tqdm', 'setuptools', 'pyuac', 'requests', 'public-ip', 'keyboard', 'pyautogui', 'customtkinter', 'CTkMessagebox', 'unixreg'],  #type:ignore
        keywords=['python', 'windows', 'encryption'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)
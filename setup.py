from setuptools import setup

version = '0.1.1'

setup(
    name='dashfilebrowser',         # How you named your package folder
    packages=['dashfilebrowser'],   # Chose the same as "name"
    version=version,      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='File browser a Dash app. Load text file into textarea for Grammarly.',
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    author='Ravinder Bhattoo',                   # Type in your name
    author_email='',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/ravinderbhattoo/dashfilebrowser',
    # I explain this later on
    download_url='https://github.com/ravinderbhattoo/dashfilebrowser/archive/{}.tar.gz'.format(
        version),
    # Keywords that define your package best
    keywords=['Browser', 'Grammar', 'Dash app'],
    install_requires=[            # I get to this in a second
        'dash',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)

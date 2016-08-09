from setuptools import setup

setup(
    name='Augmentor',
    packages=['Augmentor'],
    version='0.1',
    description='Image augmentation library for Machine Learning',
    license='MIT',
    author='Marcus D. Bloice',
    author_email='marcus.bloice@medunigraz.at',
    url='https://github.com/mdbloice/Augmentor',  # URL to GitHub repo
    download_url='https://github.com/mdbloice/Augmentor/tarball/0.1',  # Get this using git tag
    keywords=['image', 'augmentation', 'artificial', 'generation', 'machine', 'learning'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Pillow>=3.0.0',
        'terminaltables',
        'future>=0.15.0'
    ]

)

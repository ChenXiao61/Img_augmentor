from setuptools import setup

setup(
    name='Augmentor',
    packages=['Augmentor'],  # this must be the same as the name above
    version='0.1',
    description='Image augmentation library for Machine Learning',
    license='MIT',
    author='Marcus D. Bloice',
    author_email='marcus.bloice@medunigraz.at',
    url='https://github.com/mdbloice/Augmentor',  # use the URL to the github repo
    download_url='https://github.com/mdbloice/Augmentor/tarball/0.1',  #
    keywords=['image', 'augmentation', 'artificial', 'generation', 'machine', 'learning'],  # arbitrary keywords
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
         'Pillow>=3.0.0',
	 'terminaltables'
    ],

)

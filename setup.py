from distutils.core import setup
setup(
  name = 'Augmentor',
  packages = ['Augmentor'], # this must be the same as the name above
  version = '0.1',
  description = 'Image augmentation library for Machine Learning',
  author = 'Marcus D. Bloice',
  author_email = 'marcus.bloice@medunigraz.at',
  url = 'https://github.com/mdbloice/Augmentor', # use the URL to the github repo
  download_url = 'https://github.com/mdbloice/Augmentor/tarball/0.1', # I'll explain this in a second
  keywords = ['image', 'augmentation', 'generation', 'machine', 'learning'], # arbitrary keywords
  CLASSIFIERS = [
      "Development Status :: 1 - Beta",
      "Intended Audience :: Developers",
      "Natural Language :: English",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 2.6",
      "Programming Language :: Python :: 2.7",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.3",
      "Programming Language :: Python :: 3.4",
      "Programming Language :: Python :: 3.5",
      "Programming Language :: Python :: Implementation :: CPython",
      "Programming Language :: Python :: Implementation :: PyPy",
      "Topic :: Software Development :: Libraries :: Python Modules",
  ],
)
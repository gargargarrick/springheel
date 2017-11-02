from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='springheel',
      version='0.1',
      description='Static site generator for webcomics',
      long_description="A simple static site generator designed for webcomics",
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Internet',
      ],
      keywords='website webcomic static',
      url='http://github.com/gargargarrick/springheel',
      author='Garrick',
      author_email='earthisthering@posteo.de',
      license='GPLv3+',
      packages=['springheel'],
      install_requires=[
          'feedgen',
          'arrow',
          'awesome-slugify',
      ],
      scripts=['bin/springheel-init','bin/springheel-build'],
      include_package_data=True,
      zip_safe=False)

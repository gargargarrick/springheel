from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='springheel',
      version='3.0.3',
      description='Static site generator for webcomics',
      long_description="A simple static site generator designed for webcomics",
      classifiers=[
        'Development Status :: 4 - Beta',
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
          'awesome-slugify'
      ],
      entry_points = {
          'console_scripts': ['springheel-init=springheel.command_line:init',
                              'springheel-build=springheel.command_line:build',
                              'springheel=springheel.command_line:version']
          },
      include_package_data=True,
      zip_safe=False)

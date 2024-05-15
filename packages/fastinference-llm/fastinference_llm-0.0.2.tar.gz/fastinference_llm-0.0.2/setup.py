from distutils.core import setup
setup(
  name = 'fastinference-llm',         # How you named your package folder (MyLib)
  packages = ['fastinference'],   # Chose the same as "name"
  version = '0.0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Seamlessly integrate with top LLM APIs for speedy, robust, and scalable querying. Ideal for developers needing quick, reliable AI-powered responses.',   # Give a short description about your library
  author = 'Baptiste Lefort',                   # Type in your name
  author_email = 'lefort.baptiste@icloud.com',      # Type in your E-Mail
  url = 'https://github.com/blefo/FastInference',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/blefo/FastInference/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['api', 'fast', 'inference', 'distributed', 'llm'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
)

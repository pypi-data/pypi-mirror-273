from distutils.core import setup
setup(
  name = 'fastinference-llm',
  packages=[
    'fastinference',
    'fastinference.data_processing',
    'fastinference.managers',
    'fastinference.prompt',
    'fastinference.utils',
  ],
  version = '0.0.5',
  license='MIT',
  description = 'Seamlessly integrate with top LLM APIs for speedy, robust, and scalable querying. Ideal for developers needing quick, reliable AI-powered responses.',   # Give a short description about your library
  author = 'Baptiste Lefort',
  author_email = 'lefort.baptiste@icloud.com',
  url = 'https://github.com/blefo/FastInference',
  keywords = ['api', 'fast', 'inference', 'distributed', 'llm'],
  install_requires=[
        'pandas',
        'numpy',
        'backoff',
        'openai',
        'litellm',
        'tqdm',
      ],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
)

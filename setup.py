from setuptools import setup, find_packages

setup(
    name='django-state-keeper',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description="A Django app that allows you to create backup of project and restore it later.",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url='https://github.com/MMDBadCoder/Django-State-Keeper',
    author='Mohammad Heydari',
    author_email='heidary13794@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=3.2',
        'python-telegram-bot>=20.5'
    ],
)

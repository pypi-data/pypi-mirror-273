import re
from urllib.request import urlopen
d=urlopen("https://raw.githubusercontent.com/ssb22/indexer/master/README.md").read().decode('utf-8')
d=re.sub("[(]also mirrored.*[)]","",re.sub("--(?!help|-)","",'\n'.join(L for L in d[d.index('\nAnemone'):].split('\n') if not L.startswith('* Android') and not L.startswith('* Javascript') and not L.startswith('* Unicode')).replace("Python 3 script","module").replace("mp3-recode","mp3_recode"))).replace("\n\n\n","\n\n")
from setuptools import setup, find_packages
setup(
    name='anemone_daisy_maker',
    version='1.55.8',
    entry_points={"console_scripts":["anemone=anemone.__init__:anemone"]},
    author='Silas S. Brown',
    author_email='ssb22@cam.ac.uk',
    description='Create DAISY digital talking books from HTML text, MP3 audio and JSON time index data',
    long_description=d,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=["mutagen"],
)

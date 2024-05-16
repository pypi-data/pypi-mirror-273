from setuptools import setup, find_packages

# Read the requirements.txt file
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()
    
with open('readme.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='WaveFormer',  
    version='0.1.3', 
    description='A single unified Advanced Audio Processing toolkit, that provides both High-Level and Low-Level approaches to its extensive collection of tools.',
    long_description=long_description,
    url='https://github.com/heleusbrands/WaveForm/tree/main',
    keywords=[
        'Audio', 'Audio Processing', 'Rubberband', 'Pydub', 
        'pytsmod', 'nwaves', 'parselmouth', 'Audio Effects', 
        'Rose', 'Bloom', 'Audio Research', 'Formants', 
        'pyrubberband', 'Audio Features', 'WaveForm', 
        'WaveFormer', 'Sound Design', 'Audio Visualization', 
        'Audio Graph', 'Audio Array'
        ],
    classifiers=[
        'Intended Audience :: Science/Research', 
        'Topic :: Multimedia :: Sound/Audio', 
        'Topic :: Multimedia :: Sound/Audio :: Analysis', 
        'Topic :: Multimedia :: Sound/Audio :: Conversion', 
        'Topic :: Multimedia :: Sound/Audio :: Speech', 
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
        ],
    author='Bloom Research',
    author_email='rosebloomresearch@gmail.com',
    packages=find_packages(),  
    package_data={'': ['rubberband_builds/*.dll']},
    install_requires=requirements,
    license='CC BY 4.0',
    long_description_content_type='text/markdown'
)

#!/usr/bin/env bash

while [ $# -gt 0 ]
do
    case "$1" in
        -v)  VERSION=$2;;
        --)	shift; break;;
        -*)
            echo >&2 \
            "usage: $0 [-v] [-f file] [file ...]"
            exit 1;;
        *)  break;;	# terminate while loop
    esac
    shift
done


# Navigate to SDA path
cd $HOME/Projects/SAMpyL

# Update versions on files
sed -i '' -E -- "s/__version__ = '.*'/__version__ = '$VERSION'/g" sampyl/__init__.py

# Add GitHub release tag
git add sampyl/__init__.py
git commit -m "PyPi release $VERSION"
git tag ${VERSION} -m "PyPi release $VERSION"
git push --tags origin master

python setup.py sdist bdist_wheel upload -r "https://pypi.python.org/pypi"

echo "${VERSION} released..."

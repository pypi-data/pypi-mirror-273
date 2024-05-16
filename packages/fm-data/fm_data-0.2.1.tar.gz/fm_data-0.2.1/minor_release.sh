#!/bin/bash

# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

# Guide to use this script:
# 1. version as a parameter. It should be new, i.e, different than the one in the init file.
#    This is automatically updated in the init file.
# 2. Update the change log with the contents of this version.
# 3. There should be no local changes. Either commit or stash them.

set -e

if [ -z "$1" ]; then
  echo "Please specify to-be-released version as parameter."
  exit 1
fi

OLD_VERSION="$(grep __version__ coveriteam/__init__.py | sed -e 's/^.*"\(.*\)".*$/\1/')"
VERSION="$1"
if [ $(expr match "$VERSION" ".*dev") -gt 0 ]; then
  echo "Cannot release development version."
  exit 1
fi
if [ "$VERSION" = "$OLD_VERSION" ]; then
  echo "Version already exists."
  exit 1
fi
if [ ! -z "$(git status -uno -s)" ]; then
  echo "Cannot release with local changes, please stash them."
  exit 1
fi

# Prepare files with new version number
hatch version "$VERSION"
git commit src/fm_tools/__init__.py -m "Release $VERSION"

git tag -s "$VERSION" -m "Release $VERSION"

git push --tags

read -p "Please enter next version number:  " -r
hatch version "$REPLY"
git commit src/fm_tools/__init__.py -m "Prepare version number for next development cycle."


echo

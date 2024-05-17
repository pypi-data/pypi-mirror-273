#!/usr/bin/env sh


export VERSION=0.0.11

export NAME=python-project-stub

DESCRIPTION='Stub files to use as the basis of a Python project that'
export DESCRIPTION="${DESCRIPTION} can be packaged and uploaded to PyPI"

export GITHUB_USER='striebel'

export AUTHOR='Jacob Striebel'
export AUTHOR_EMAIL='jacob.striebel@example.com'

export DATA_FILE_PATH_SUFFIXES='meta.sh:data/quote.txt' # When more needed, separate with colon (:)


# https://stackoverflow.com/a/1463370

printf 'global VERSION                ; VERSION                 = "'"${VERSION}"'"                \n'
printf 'global NAME                   ; NAME                    = "'"${NAME}"'"                   \n'
printf 'global DESCRIPTION            ; DESCRIPTION             = "'"${DESCRIPTION}"'"            \n'
printf 'global GITHUB_USER            ; GITHUB_USER             = "'"${GITHUB_USER}"'"            \n'
printf 'global AUTHOR                 ; AUTHOR                  = "'"${AUTHOR}"'"                 \n'
printf 'global AUTHOR_EMAIL           ; AUTHOR_EMAIL            = "'"${AUTHOR_EMAIL}"'"           \n'
printf 'global DATA_FILE_PATH_SUFFIXES; DATA_FILE_PATH_SUFFIXES = "'"${DATA_FILE_PATH_SUFFIXES}"'"\n'


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Diego Minguzzi 2025
#
import typing

#---------------------------------------------------------------------------------------------------
class Article:
    def __init__( self, title: str, text: str, references: typing.List[str]=[]):
        self._title = title
        self._text = text
        self._references = references

    @property
    def title( self): return self._title

    @property
    def text( self): return self._text

    @property
    def references( self): return self._references

    @property
    def referencesAsString( self, separator=', '): return separator.join(self._references)

    @property
    def numReferences( self) -> int:
        return len(self._references)

    def addReference( self, reference: str):
        if reference is None:
            raise ValueError('reference')
        self._references.append( reference.strip())

#---------------------------------------------------------------------------------------------------
def main():
    obj = Article( 'The Title', 'The text')
    obj.addReference('RefXYZ')
    obj.addReference('RefZZZ')
    print(f'Article:\n\t{obj.title}\n\t{obj.text}\n\tNum refrences:{len(obj.references)}\n\t{obj.references}')
    print(f'\t{obj.referencesAsString}')
    print(f'\t{obj.numReferences}')

#---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()


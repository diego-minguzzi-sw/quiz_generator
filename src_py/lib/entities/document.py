#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Diego Minguzzi 2025
#
class Document:
    def __init__( self):
        self._articles = []

    def addArticle( self, article):
        self._articles.append( article)

    @property
    def articles( self):
        return self._articles

    @property
    def numArticles( self) -> int:
        return len(self._articles)

#---------------------------------------------------------------------------------------------------
def main():
    obj = Document()

#---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()




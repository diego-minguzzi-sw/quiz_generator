#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Diego Minguzzi 2025
#
import logging as log
import random
import typing

class Question:
    def __init__( self,
                  question: str,
                  answers: typing.List[str],
                  explanation: str,
                  indexArticle: int=0):
        self._question= question
        self._answers= answers
        self._explanation= explanation
        self._indexCorrectAnswer= 0
        self._indexArticle= indexArticle

        if self.numAnswers <= 0:
            raise ValueError('No answer is provided.')

        numShuffles= random.randint(0, 10)
        for indx in range(0, numShuffles):
          self.shuffle()

    @property
    def question( self):
        return self._question

    @property
    def answers( self):
        return self._answers

    @property
    def numAnswers( self):
        return len(self._answers)

    @property
    def indexCorrectAnswer( self):
        return self._indexCorrectAnswer

    @property
    def correctAnswer( self):
        return self._answers[self._indexCorrectAnswer]

    def answer( self, indx: int):
        if (indx<0) or (indx>= len(self._answers)):
            raise ValueError(f'indx:{indx}')
        return self._answers[indx]

    @property
    def explanation( self):
        return self._explanation

    @property
    def indexArticle( self):
        return self._indexArticle

    def shuffle( self):
        newIndexCorrectAnswer= random.randint(0, len(self._answers)-1)

        tmp = self._answers[self._indexCorrectAnswer]
        self._answers[self._indexCorrectAnswer] = self._answers[newIndexCorrectAnswer]
        self._answers[newIndexCorrectAnswer] = tmp
        self._indexCorrectAnswer = newIndexCorrectAnswer
        log.debug(f'self._indexCorrectAnswer:{self._indexCorrectAnswer}')


#---------------------------------------------------------------------------------------------------
def main():
    obj = Question('Question',['A','B','C'],'Explanation')
    print(f'obj indexCorrectAnwser:{obj.indexCorrectAnswer}')
    print(f'obj Answers:{obj.answers}')
    print(f'obj Correct answer:{obj.correctAnswer}')

#---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    _FORMAT_STRING = "%(module)s.%(funcName)s():%(lineno)d %(asctime)s\n[%(levelname)-5s] %(message)s\n"
    log.basicConfig(level= log.DEBUG, format=_FORMAT_STRING)
    main()




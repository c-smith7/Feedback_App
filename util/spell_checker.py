import PyQt5
import enchant
from PyQt5 import QtCore
from enchant import tokenize
from enchant.errors import TokenizerNotFoundError
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import QPlainTextEdit


class SpellTextEdit(QPlainTextEdit):
    """QPlainTextEdit subclass which does spell-checking using PyEnchant"""
    def __init__(self, *args):
        QPlainTextEdit.__init__(self, *args)

        # Start with a default dictionary based on the current locale.
        self.highlighter = SpellChecker(self.document())
        self.highlighter.setDict(enchant.Dict())


class SpellChecker(QSyntaxHighlighter):
    """QSyntaxHighlighter subclass which consults a PyEnchant dictionary"""
    tokenizer = None
    token_filters = (tokenize.EmailFilter, tokenize.URLFilter)
    err_format = QTextCharFormat()
    err_format.setUnderlineColor(PyQt5.QtCore.Qt.red)
    err_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

    def __init__(self, *args):
        QSyntaxHighlighter.__init__(self, *args)

        # Initialize private members
        self._sp_dict = None
        self._chunkers = []

    def chunkers(self):
        """Gets the chunkers in use"""
        return self._chunkers

    def dict(self):
        """Gets the spelling dictionary in use"""
        return self._sp_dict

    def setChunkers(self, chunkers):
        """Sets the list of chunkers to be used"""
        self._chunkers = chunkers
        self.setDict(self.dict())

    def setDict(self, sp_dict):
        """Sets the spelling dictionary to be used"""
        try:
            self.tokenizer = tokenize.get_tokenizer(sp_dict.tag, chunkers=self._chunkers, filters=self.token_filters)
        except TokenizerNotFoundError:
            # Fall back to English tokenizer
            self.tokenizer = tokenize.get_tokenizer(chunkers=self._chunkers, filters=self.token_filters)
        self._sp_dict = sp_dict

        self.rehighlight()

    def highlightBlock(self, text):
        """Overridden QSyntaxHighlighter method to apply the highlight"""
        if not self._sp_dict:
            return

        # Build a list of all misspelled words and highlight them
        misspellings = []
        for (word, pos) in self.tokenizer(text):
            if not self._sp_dict.check(word):
                self.setFormat(pos, len(word), self.err_format)
                misspellings.append((pos, pos + len(word)))

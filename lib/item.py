"""
A representation of an item in DSpace.

An item has a collection of files (aka Bitstreams) and a number of metadata name value pairs. 
"""

import os
import re

class Item:
    delimiter = '||'

    def __init__(self, delimiter = '||'):
        self.delimiter = delimiter
        self._attributes = {}
        self.files = ""

    """
    Get a dict of all attributes.
    """
    def getAttributes(self):
        return self._attributes

    """
    Set an attribute value.
    """
    def setAttribute(self, attribute, value):
        if attribute == "files":
            self.files = value
        else:
            self._attributes[attribute] = value

    """
    Get an attribute value. 
    """
    def getAttribute(self, attribute):
        return self._attributes[attribute]

    """
    Convert the item to a string
    """
    def __str__(self):
        return str(self._attributes)

    """
    Get the files (bitstreams) associated with this item.
    This function just returns the file name, with no path.
    """
    def getFiles(self):
        values = []
        files = self.files.split(self.delimiter)
        for index, file_name in enumerate(files):
            file = os.path.basename(file_name).strip()
            values.append(file)
        return values

    """
    Get the files (bitstreams) associated with this item.
    This function returns the file with the full import path.
    """
    def getFilePaths(self):
        values = []
        files = self.files.split(self.delimiter)
        for index, file_name in enumerate(files):
            file = file_name.strip()
            values.append(file)
        return values

    """
    Returns an XML represenatation of the item.
    """
    def toXML(self):
        linesep = '\n'
        output = '<?xml version="1.0" encoding="utf-8" standalone="no"?>' + linesep
        output += '<dublin_core schema="dc">' + linesep
        for index, value in self.getAttributes().items():
            tag_open = self.getOpenAttributeTag(index)
            tag_close = "</dcvalue>" + linesep

            values = value.split(self.delimiter)

            for val in values:
                if not val:
                    continue

                output += '  '+tag_open
                output += self.escape(val.strip(), quote=True)
                output += tag_close
        output += "</dublin_core>" + linesep

        return output

    """
    Get the opening XML tag for a metadata attribute.
    """
    def getOpenAttributeTag(self, attribute):
        lang = self.getAttributeLangString(attribute)
        element = self.getAttributeElementString(attribute)
        qualifier = self.getAttributeQualifierString(attribute)

        tag_open = '<dcvalue%s%s%s>' % (element, qualifier, lang)

        return tag_open

    """
    Get a string the key value pair for the lang attribute.
    eg 'language="en"'
    """
    def getAttributeLangString(self, attribute):
        match = re.search('_(\w+)', attribute)

        if match != None:
            return 'language="' + self.escape(match.group(1), quote=True) + '"'
        else:
            return ''

    """
    Strip the language bit off of a metadata attribute.
    """
    def stripAttributeLang(self, attribute):
        attribs = attribute.split('_')
        return attribs[0]

    """
    Get a string of the key value pair for the element attribute.
    eg 'element="contributor"'
    """
    def getAttributeElementString(self, attribute):
        attribute = self.stripAttributeLang(attribute)
        attribs = attribute.split('.')

        if len(attribs) >= 2:
            return ' element="' + self.escape(attribs[1], quote=True) + '" '
        else:
            return ''

    """
    Get a string the key value pair for the qualifier attribute.
    eg 'qualifier="author"'
    """
    def getAttributeQualifierString(self, attribute):
        attribute = self.stripAttributeLang(attribute)
        attribs = attribute.split('.')

        if len(attribs) >= 3:
            return 'qualifier="' + self.escape(attribs[2], quote=True) + '"'
        else:
            return 'qualifier="none"'
    
    def escape(self, s, quote=True):
        """
        Replace special characters "&", "<" and ">" to HTML-safe sequences.
        If the optional flag quote is true (the default), the quotation mark
        characters, both double quote (") and single quote (') characters are also
        translated.
        """
        s = s.replace("&", "&amp;") # Must be done first!
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        s = s.replace(" ", "&#x20;")
        if quote:
            s = s.replace('"', "&quot;")
            s = s.replace('\'', "&#x27;")
        return s

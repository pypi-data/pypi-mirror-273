# This file is part of dsiUnits (https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB)]
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.

#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
import re
import warnings
import difflib
from typing import List
from copy import deepcopy
import math
from fractions import Fraction
from decimal import Decimal, InvalidOperation
import numbers

# config.py
class dsiConfigConfig:
    #Singelton Pattern this class can only have one instance all constructors will return this instance
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(dsiConfigConfig, cls).__new__(cls)
            # Initialize configuration options
            cls._instance.createPerByDivision = True
            cls._instance.maxDenominator = 10000
        return cls._instance


dsiConfigConfiginstance = dsiConfigConfig()

def _dsiStrFromNodes(nodeList):
    """Converts a list of nodes to a D-SI string."""
    dsiStr = ""
    for i, unitFraction in enumerate(nodeList):
        if i > 0:
            dsiStr += r"\per"
        for node in unitFraction:
            dsiStr += str(node)
    return dsiStr


class dsiParser:
    __dsiVersion = "2.2.0"
    __dsiSchemaUrl = "https://www.ptb.de/si/v2.2.0/SI_Format.xsd"
    __dsiRepositoryURL = "https://gitlab1.ptb.de/d-ptb/d-si/xsd-d-si"
    """Parser to parse D-SI unit string into a tree
    """

    def __init__(self, latexDefaultWrapper='$$', latexDefaultPrefix='', latexDefaultSuffix=''):
        """
        Args:
            latexDefaultWrapper (str, optional): String to be added both in the beginning and the end of the LaTeX string. Defaults to '$$'.
            latexDefaultPrefix (str, optional): String to be added in the beginning of the LaTeX string, after the wrapper. Defaults to ''.
            latexDefaultSuffix (str, optional): String to be added in the end of the LaTeX string, before the wrapper. Defaults to ''.
        """
        super()
        self.latexDefaultWrapper = latexDefaultWrapper
        self.latexDefaultPrefix = latexDefaultPrefix
        self.latexDefaultSuffix = latexDefaultSuffix

    def parse(self, dsiString: str):
        """parses a D-SI string into a tree structure


        Args:
            dsiString (str): D-SI unit raw string

        Raises:
            RuntimeWarning: double backslashes in D-SI string
            RuntimeWarning: empty D-SI string

        Returns:
            dsiTree: dsiTree object containing the D-SI unit
        """
        warningMessages = []
        # Catch any double (triple...) \ before they annoy us
        while r'\\' in dsiString:
            warningMessages.append(
                _warn(f"Double backslash found in string, treating as one backslash: «{dsiString}»", RuntimeWarning))
            dsiString = dsiString.replace(r'\\', '\\')

        if dsiString == "":
            warningMessages.append(_warn("Given D-SI string is empty!", RuntimeWarning))
            return dsiUnit('NULL', [], warningMessages, self.latexDefaultWrapper, self.latexDefaultPrefix,
                           self.latexDefaultSuffix)

        tree = []
        (tree, fractionWarnings) = self._parseDsiFraction(dsiString)
        warningMessages += fractionWarnings
        for i, node in enumerate(tree):
            (tree[i], fractionlessWarnings) = self._parseFractionlessDsi(node)
            warningMessages += fractionlessWarnings
        return dsiUnit(dsiString, tree, warningMessages, self.latexDefaultWrapper, self.latexDefaultPrefix,
                       self.latexDefaultSuffix)

    def _parseDsiFraction(self, dsiString: str):
        """parses D-SI fraction into list of fraction elements

        Args:
            dsiString (str): D-SI unit raw string

        Raises:
            RuntimeWarning: String must not contain more than one "per",
                            as defined in the D-SI specs

        Returns:
            list: strings separated by the "per"
            list: warning messages of problems encountered while parsing
        """
        tree = []
        warningMessages = []
        dsiStringWOperCent = dsiString.replace('percent',
                                               'prozent')  # rename percent to prozent to have it not split at per ....
        tree = dsiStringWOperCent.split(r"\per")
        for i, subtree in enumerate(tree):
            tree[i] = tree[i].replace('prozent', 'percent')
        for subtree in tree:
            if len(subtree) == 0:
                warningMessages.append(_warn(r"The dsi string contains a \per missing a numerator or denominator! " +
                                             f"Given string: {dsiString}",
                                             RuntimeWarning))
                tree.remove(subtree)
        if len(tree) > 2:
            warningMessages.append(_warn(r"The dsi string contains more than one \per, does not " +
                                         f"match specs! Given string: {dsiString}",
                                         RuntimeWarning))
        return (tree, warningMessages)

    def _parseFractionlessDsi(self, dsiString: str):
        """parses D-SI unit string without fractions

        Args:
            dsiString (str): D-SI unit raw string, not containing any fractions

        Raises:
            RuntimeWarning: if string does not meet the specs

        Returns:
            list: list of nodes
            list: warning messages of problems encountered while parsing
        """
        warningMessages = []
        items = dsiString.split("\\")
        if items[0] == '':  # first item of List should be empty, remove it
            items.pop(0)
        else:
            warningMessages.append(
                _warn(f"string should start with \\, string given was «{dsiString}»", RuntimeWarning))
        nodes = []

        (prefix, unit, exponent) = ('', '', '')
        valid=True
        item = items.pop(0)
        while True:
            if item in _dsiPrefixesLatex:
                prefix = item
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            if item in _dsiUnitsLatex:
                unit = item
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            if re.match(r'tothe\{[^{}]*\}', item): # used to be elif
                exponentStr = item.split('{')[1].split('}')[0]
                try:
                    exponent = Fraction(exponentStr).limit_denominator()
                except ValueError:
                    warningMessages.append(_warn(f"The exponent «{exponent}» is not a number!", RuntimeWarning))
                    valid=False
                    exponent = exponentStr
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            if (prefix, unit, exponent) == ('', '', ''):
                unit = item
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
                closestMatches = _getClosestStr(unit)
                if len(closestMatches) > 0:
                    closestMatchesStr = ', \\'.join(closestMatches)
                    closestMatchesStr = '\\' + closestMatchesStr
                    warningMessages.append(_warn(
                        fr"The identifier «{unit}» does not match any D-SI units! Did you mean one of these «{closestMatchesStr}» ?",
                        RuntimeWarning))
                    valid=False
                else:
                    warningMessages.append(
                        _warn(fr"The identifier «{unit}» does not match any D-SI units!", RuntimeWarning))
                    valid=False
            elif unit == '':
                itemStr = ""
                if prefix != "":
                    itemStr = itemStr + "\\" + prefix
                if exponent != "":
                    itemStr = itemStr + r"\tothe{" + str(exponent) + r"}"
                warningMessages.append(
                    _warn(f"This D-SI unit seems to be missing the base unit! «{itemStr}»", RuntimeWarning))
                valid=False
            nodes.append(_node(prefix, unit, exponent, valid=valid))
            if (len(items) == 0) and (item == ''): break
            (prefix, unit, exponent) = ('', '', '')
            valid=True
        return (nodes, warningMessages)

    def info(self):
        infoStr = "D-SI Parser Version: " + str(self) + "using D-SI Schema Version: " + str(
            self.__dsiVersion) + "from: " + str(self.__dsiRepositoryURL) + "using D-SI Schema: " + str(
            self.__dsiSchemaUrl)
        print(infoStr)
        return (infoStr, self.__dsiVersion, self.__dsiSchemaUrl, self.__dsiRepositoryURL)

dsiDefaultParser=dsiParser()

class dsiUnit:
    """D-SI representation in tree form, also includes validity check and warnings about D-SI string.
       Tree format: list of lists:
           List format:
           First layer: items of the unit fraction
           Second layer: nodes containing prefix, unit, power
    """

    def __init__(self, dsiString: str, dsiTree=[], warningMessages=[], latexDefaultWrapper='$$', latexDefaultPrefix='',
                 latexDefaultSuffix=''):
        """
        Args:
            dsiString (str): the D-SI unit string to be parsed
            optional dsiTree (list): List of lists of nodes as tuples containing (prefix: str,unit: str,exponent: Fraction=Fraction(1),scaleFactor: float = 1.0)
            like [('metre', 1.0, 1.0), ('second', -1.0, 1.0)] to generate ms^-1 when usign this construction method no str can be given
        """
        # we have got a tree so we dont need to parse the string
        if dsiString == "" and dsiTree != []:
            dsiString=_dsiStrFromNodes(dsiTree)
        if dsiString != "" and dsiTree == []:
            try:
                # TODO Why do we parse twice?
                dsiTree = dsiDefaultParser.parse(dsiString).tree
                warningMessages = dsiDefaultParser.parse(dsiString).warnings
            except Exception as e:
                warnings.warn(e)
        if dsiString == "" and dsiTree == []:
            warnings.warn("Given D-SI string is empty!")
            dsiTree = dsiDefaultParser.parse(dsiString).tree
            warningMessages = dsiDefaultParser.parse(dsiString).warnings
        self.dsiString = dsiString
        self.tree = dsiTree
        self.warnings = warningMessages
        self.valid = len(self.warnings) == 0
        self._latexDefaultWrapper = latexDefaultWrapper
        self._latexDefaultPrefix = latexDefaultPrefix
        self._latexDefaultSuffix = latexDefaultSuffix




    def toLatex(self, wrapper=None, prefix=None, suffix=None):
        """converts D-SI unit string to LaTeX

        Args:
            wrapper (str, optional): String to be added both in the beginning and the end of the LaTeX string. Defaults to the value set in the parser object.
            prefix (str, optional): String to be added in the beginning of the LaTeX string, after the wrapper. Defaults to the value set in the parser object.
            suffix (str, optional): String to be added in the end of the LaTeX string, before the wrapper. Defaults to the value set in the parser object.

        Returns:
            str: the corresponding LaTeX code
        """

        # If no wrapper/prefix/suffix was given, set to the parser's default
        wrapper = self._latexDefaultWrapper if wrapper == None else wrapper
        prefix = self._latexDefaultPrefix if prefix == None else prefix
        suffix = self._latexDefaultSuffix if suffix == None else suffix

        if self.tree == []:
            if len(prefix) + len(suffix) > 0:
                return wrapper + prefix + suffix + wrapper
            else:
                return ""
        latexArray = []
        if len(self.tree) == 1:  # no fractions
            for node in self.tree[0]:
                latexArray.append(node.toLatex())
            latexString = r'\,'.join(latexArray)
        elif len(self.tree) == 2:  # one fraction
            latexString = ""
            latexString += r'\frac'
            for frac in self.tree:
                latexString += r'{'
                nodeArray = []
                for node in frac:
                    nodeArray.append(node.toLatex())
                latexString += r'\,'.join(nodeArray)
                latexString += r'}'
        else:  # more than one fraction
            latexString = ""
            for i in range(len(self.tree)):
                nodeArray = []
                if i > 0:
                    latexString += r'{\color{red}/}'
                for node in self.tree[i]:
                    nodeArray.append(node.toLatex())
                latexString += r'\,'.join(nodeArray)
        return wrapper + prefix + latexString + suffix + wrapper

    def toUTF8(self):
        """Converts D-SI unit string to a compact UTF-8 format."""

        def exponent_to_utf8(exp):
            """Converts numerical exponents to UTF-8 subscript."""
            # Mapping for common exponents to UTF-8
            superscripts = {"1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵",
                            "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "0": "⁰",
                            "-": "⁻",".": "˙"}
            # Convert fractional exponents to a more readable format if needed
            return ''.join(superscripts.get(char, char) for char in str(exp))

        utf8Array = []
        for unitFraction in self.tree:
            fractionUtf8Array = []
            for node in unitFraction:
                # Fetch UTF-8 unit representation
                unitStr = _dsiUnitsUTF8.get(node.unit,'⚠'+node.unit+'⚠')#second arg is returend on itemError

                # Handle prefix (if any) and unit
                prefixStr = _dsiPrefixesUTF8.get(node.prefix, '⚠'+node.prefix+'⚠') if node.prefix else ""
                utf8Str = f"{prefixStr}{unitStr}"  # Direct concatenation for compactness

                # Handle exponent, converting to UTF-8 subscript, if not 1
                if node.exponent and node.exponent != 1:
                    utf8Str += exponent_to_utf8(node.exponent)

                fractionUtf8Array.append(utf8Str)

            # Join units within the same fraction with a dot for compactness
            utf8Array.append("".join(fractionUtf8Array))

        # Handle fractions, join numerator and denominator with a slash for division
        return " / ".join(utf8Array).replace(' ', '')



    def toBaseUnitTree(self,complete=False):
        """
        Converts the entire D-SI tree to its base unit representation.
        """
        baseUnitTree = []
        for unitFraction in self.tree:
            baseFraction = []
            for node in unitFraction:
                baseFraction.extend(node.toBaseUnits())
            baseUnitTree.append(baseFraction)
        unconsolidatedTree = dsiUnit(self.dsiString, baseUnitTree, self.warnings, self._latexDefaultWrapper, self._latexDefaultPrefix, self._latexDefaultSuffix)
        reduced=unconsolidatedTree.reduceFraction()
        # if kgms True we do a second round but resolve volt ampere mole this round
        if complete:
            baseUnitTree = []
            for unitFraction in self.tree:
                baseFraction = []
                for node in unitFraction:
                    baseFraction.extend(node.toBaseUnits(complete=complete))
                baseUnitTree.append(baseFraction)
            unconsolidatedTree = dsiUnit(self.dsiString, baseUnitTree, self.warnings, self._latexDefaultWrapper,
                                         self._latexDefaultPrefix, self._latexDefaultSuffix)
            reduced = unconsolidatedTree.reduceFraction()
        return reduced

    def reduceFraction(self):
        """
        Creates a new _dsiTree instance with reduced fractions.
        - Consolidates nodes with the same base unit by multiplying scales and summing exponents.
        - Sorts the nodes alphabetically by unit.
        - The first node carries the overall scale factor.
        """
        if len(self.tree) > 2:
            raise RuntimeError("D-SI tree with more than two fractions cannot be reduced.")

        consolidated_nodes = []

        # Handling single and two-node cases
        if len(self.tree) == 1:
            consolidated_nodes = self.tree[0]
        elif len(self.tree) == 2:
            # Copy nodes from the first fraction
            consolidated_nodes = [node for node in self.tree[0]]

            # Copy nodes from the second fraction, adjusting the exponents
            for node in self.tree[1]:
                # Inverting the exponent for nodes in the denominator
                invertedExponent = -1 * node.exponent
                fractionalScaleFactor = 1 / node.scaleFactor
                consolidated_nodes.append(_node(node.prefix, node.unit, invertedExponent,  scaleFactor=fractionalScaleFactor))

        # Consolidating nodes with the same unit
        i = 0
        while i < len(consolidated_nodes):
            j = i + 1
            while j < len(consolidated_nodes):
                if consolidated_nodes[i].unit == consolidated_nodes[j].unit:
                    # Consolidate nodes
                    scaleFactor = consolidated_nodes[i].scaleFactor*consolidated_nodes[j].scaleFactor
                    consolidated_nodes[i].scaleFactor = scaleFactor
                    exponent=consolidated_nodes[i].exponent + consolidated_nodes[j].exponent
                    consolidated_nodes[i].exponent = exponent
                    del consolidated_nodes[j]
                else:
                    j += 1
            i += 1

        # Calculate overall scale factor and apply it to the first node
        overall_scale_factor = 1.0
        for node in consolidated_nodes:
            overall_scale_factor *= node.scaleFactor
            node.scaleFactor = 1.0  # Reset scale factor for individual nodes
        # Sort nodes alphabetically by unit
        consolidated_nodes.sort(key=lambda x: x.unit)
        # Apply overall scale factor to the first node, if it exists
        if consolidated_nodes:
            consolidated_nodes[0].scaleFactor = overall_scale_factor
        nodesWOPowerZero=[]
        for node in consolidated_nodes:
            if node.exponent != 0:
                nodesWOPowerZero.append(node)
        if len(nodesWOPowerZero) == 0: # ok all nodes have ben power of zero so we deleted them so we end up with one as unit and 1.0 as exponent
            nodesWOPowerZero.append(_node("", "one", 1.0,scaleFactor=overall_scale_factor))
        consolidated_nodes=nodesWOPowerZero
        # Check for ones and delete them if they are not the only node ad set there exponent to 1.0 since 1^x = 1
        if len(consolidated_nodes) > 1:
            consolidated_nodes = [node for node in consolidated_nodes if node.unit != "one"]
        else:
            if consolidated_nodes[0].unit == "one":
                consolidated_nodes[0].exponent=1.0
        # Create and return a new instance of _dsiTree with consolidated nodes
        return dsiUnit(self.dsiString, [consolidated_nodes], self.warnings, self._latexDefaultWrapper,
                       self._latexDefaultPrefix, self._latexDefaultSuffix)

    def _removePer(self):
        if len(self.tree)==2:
            for i,node in enumerate(self.tree[1]):
                #invert exponent node.
                node.exponent=node.exponent*-1
                self.tree[0].append(node)
                self.tree[1].pop(i)
            self.tree.pop(1)

    def negExponentsToPer(self):
        """Converts negative exponents to the denominator of the fraction."""
        for node in self.tree[0]: # numerator
            if node.exponent < 0:
                node.exponent = -node.exponent
                try:
                    self.tree[1].append(_node("", node.unit, node.exponent))
                except IndexError:# if we have only the numerator list we need to add the denominator list
                    self.tree.append([_node("", node.unit, node.exponent)])
                self.tree[0].remove(node)
        if len(self.tree) ==2: # we have a numerator and a denominator so we must treat the denominator as well
            for node in self.tree[1]: # numerator
                if node.exponent < 0:
                    node.exponent = -node.exponent
                    self.tree[0].append(_node("", node.unit, node.exponent))
                    self.tree[1].remove(node)
        if len(self.tree[0]) == 0:
            self.tree[0].append(_node("", "one", 1.0))
        return self


    def sortTree(self):
        """Sorts each fraction's nodes alphabetically by their units."""
        for unitFraction in self.tree:
            unitFraction.sort(key=lambda node: node.unit)
    def __eq__(self, other):
        """Checks if two D-SI trees are identical after sorting their nodes alphabetically."""
        if not isinstance(other, dsiUnit):
            return False

        # Sort both trees before comparison
        selfCopy = deepcopy(self)
        otherCopy = deepcopy(other)
        selfCopy.sortTree()
        otherCopy.sortTree()
        if selfCopy.tree == otherCopy.tree:
            return True
        else:
            selfCopy._removePer()
            otherCopy._removePer()
            if selfCopy.tree==otherCopy.tree:
                return True
            else:
                return False

    def isScalablyEqualTo(self, other,complete=False):
        """Checks if two D-SI trees are scalably equal.

        Returns:
            (bool, float): Tuple of a boolean indicating if trees are scalably equal, and the scale factor.
        """
        if not isinstance(other, dsiUnit):
            return (math.nan, None)


        sortedSelf=deepcopy(self)
        sortedSelf.sortTree()
        sortedOther=deepcopy(other)
        sortedOther.sortTree()
        # okay now check if is identical
        if sortedSelf.tree == sortedOther.tree:
            return (1.0,self)
        scaleFactor=1
        for fracIdx,unitFraction in enumerate(sortedSelf.tree):
            try:
                if len(unitFraction) != len(sortedOther.tree[fracIdx]):
                    scaleFactor=math.nan
                    break
                for nodeIDX,node in enumerate(unitFraction):
                    scaleFactor *= node.isScaled(sortedOther.tree[fracIdx][nodeIDX])
            except IndexError:
                # if we get here we have a fraction in one tree that is not in the other in this case we resolve to base units and compare
                scaleFactor=math.nan
                break
        if not math.isnan(scaleFactor):
            return (scaleFactor,self)
        # Convert both trees to their base unit representations
        selfBaseUnitTree = self.toBaseUnitTree(complete=complete)
        otherBaseUnitTree = other.toBaseUnitTree(complete=complete)

        # Sort both trees
        selfBaseUnitTree.sortTree()
        otherBaseUnitTree.sortTree()
        # Check if units match
        if len(selfBaseUnitTree.tree) != len(otherBaseUnitTree.tree):
            return (math.nan, None)
        # Calculate scale factor
        scaleFactor = 1.0
        if len(selfBaseUnitTree.tree) != 1 or len(otherBaseUnitTree.tree) != 1:
            raise RuntimeError("D-SI tree with more than one fraction cannot be compared. And should not exist here since we consolidated earlier")
        for selfNode, otherNode in zip(selfBaseUnitTree.tree[0], otherBaseUnitTree.tree[0]):
            if selfNode.unit != otherNode.unit:
                return (math.nan, None)
            if selfNode.exponent != otherNode.exponent:
                return (math.nan, None)
            scaleFactor *= otherNode.scaleFactor / selfNode.scaleFactor
        # resetting scaleFactor to 1.0
        for unitFraction in selfBaseUnitTree.tree:
            for node in unitFraction:
                node.scaleFactor = 1.0
        return (scaleFactor,selfBaseUnitTree)

    def __str__(self):
        result = ""
        for node in self.tree[0]:
            result += str(node)
        if len(self.tree) == 2:
            result += r'\per'
            for node in self.tree[1]:
                result += str(node)
        return result

    def __repr__(self):
        contentStr=self.toUTF8()
        if not self.valid:
            contentStr+='INVALIDE'
        if self.warnings:
            contentStr+=f" {len(self.warnings)} WARNINGS"
        # Simple representation: class name and D-SI string
        return f"{contentStr}"


    def __pow__(self, other):
        if not isinstance(other, numbers.Real):
            raise TypeError("Exponent must be a real number")
        resultNodeLIst = deepcopy(self.tree)
        for unitFraction in resultNodeLIst:
            for node in unitFraction:
                node.exponent *= other
        resultTree =dsiUnit("", resultNodeLIst, self.warnings, self._latexDefaultWrapper, self._latexDefaultPrefix, self._latexDefaultSuffix)
        resultTree = resultTree.reduceFraction()
        if len(self.tree)==2: # check if we had a per representation
            resultTree.negExponentsToPer()
        return resultTree

    def __mul__(self, other):
        if len(self.tree) + len(other.tree) > 2:
            convertToPer=True
        else:
            convertToPer=False
        resultNodeLIst=deepcopy(self.tree)
        for i,unitFraction in enumerate(other.tree):
            if i>1:
                raise RuntimeError("D-SI tree with more than one fraction cannot be multiplied")
            try:
                resultNodeLIst[i].extend(deepcopy(unitFraction))
            except IndexError:
                resultNodeLIst.append(deepcopy(unitFraction))# there was no fraction so we add it

        resultTree =dsiUnit("", resultNodeLIst, self.warnings, self._latexDefaultWrapper, self._latexDefaultPrefix, self._latexDefaultSuffix)
        resultTree = resultTree.reduceFraction()
        if convertToPer:
            resultTree = resultTree.negExponentsToPer()
        return resultTree

    def __truediv__(self, other):
        if dsiConfigConfiginstance.createPerByDivision:
            return (self * (other**-1)).negExponentsToPer()
        else:
            return self * (other ** -1)


class _node:
    """one node of the D-SI tree, containing prefix, unit, power
    """
    def __init__(self, prefix: str,unit: str,exponent: Fraction=Fraction(1), valid:bool=True,scaleFactor: float = 1.0  ):# Adding scale factor with default value 1.0
        self.prefix=prefix
        self.unit=unit
        self.valid=valid
        if isinstance(exponent,Fraction) or isinstance(exponent,int):
            self.exponent=Fraction(exponent)
        if isinstance(exponent,str):
            if exponent== '':
                exponent= Fraction(1)
            else:
                try:
                    exponent = Fraction(exponent).limit_denominator(dsiConfigConfiginstance.maxDenominator)
                except ValueError:
                    exponent=exponent
                    warnings.warn(f"Exponent «{exponent}» is not a number!", RuntimeWarning)
        self.exponent=exponent
        self.scaleFactor=scaleFactor  # Adding scale factor with default value 1.0

    def toLatex(self):
        """generates a latex string from a node

        Returns:
            str: latex representation
        """
        latexString = ""
        if self.prefix:
            latexString += _dsiPrefixesLatex[self.prefix]
        try:
            latexString += _dsiUnitsLatex[self.unit]
        except KeyError:
            latexString += r'{\color{red}\mathrm{'+self.unit+r'}}'
            if self.valid==True:
                raise RuntimeError("Found invalid unit in valid node, this should not happen! Report this incident at: https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/issues/new")
        if isinstance(self.exponent,str):
            # exponent is str this shouldn't happen!
            latexString += r'^{{\color{red}\mathrm{'+self.exponent+r'}}}'
            if self.valid==True:
                raise RuntimeError("Found invalid unit in valid node, this should not happen! Report this incident at: https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/issues/new")
        elif self.exponent != 1:
            if not self.exponent.denominator == 1: # exponent is not an integer
                if self.exponent.denominator == 2: # square root
                    latexString = r'\sqrt{' + latexString 
                else: # higher roots need an extra argument
                    latexString = r'\sqrt[' + str(self.exponent.denominator) + ']{' + latexString
                    if self.exponent.numerator != 1: # keep anything in the numerator of the exponent in the exponent
                        latexString += '^{' + str(self.exponent.numerator) + '}'
                latexString += r'}'
                    
            else:
                latexString += r'^{' + str(self.exponent) + r'}'

        
        if self.unit == "":
            latexString = r'{\color{red}'+latexString+r'}'
            if self.valid==True:
                raise RuntimeError("Found invalid unit in valid node, this should not happen! Report this incident at: https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/issues/new")

        return latexString

    def toBaseUnits(self, complete=False) -> List['_node']:
        """
        Converts this node to its base unit representation.
        Adjusts the scale factor during the conversion. Optionally resolves to kg, s, and m units,
        including converting ampere, volt, and mole to their kg, s, and m equivalents when kgs is True.

        Args:
            kgs (bool): If true, also resolves volt to kg, s, and m units.

        Returns:
            List['_node']: List of nodes representing the base units or kg, s, m equivalents.
        """
        # Adjust the scale factor for the prefix
        prefixScale = _dsiPrefixesScales.get(self.prefix, 1)  # Default to 1 if no prefix
        adjustedScaleFactor = self.scaleFactor * prefixScale

        # Convert to base units if it's a derived unit
        if self.unit in _derivedToBaseUnits:
            baseUnitsInfo = _derivedToBaseUnits[self.unit]
            baseUnits = []
            for i, (baseUnit, exponent, scaleFactor) in enumerate(baseUnitsInfo):
                # Apply the adjusted scale factor only to the first base unit
                finalScaleFactor = math.pow(adjustedScaleFactor * scaleFactor, self.exponent) if i == 0 else 1.0
                baseUnits.append(_node('', baseUnit, exponent * self.exponent, scaleFactor=finalScaleFactor))
            return baseUnits
        elif complete:
            # Additional logic for converting ampere, volt, and mole to kg, s, and m equivalents
            if self.unit in _additionalConversions:
                kgsUnitsInfo = _additionalConversions[self.unit]
                kgsUnits = []
                for i, (kgsUnit, exponent, scaleFactor) in enumerate(kgsUnitsInfo):
                    finalScaleFactor = math.pow(adjustedScaleFactor * scaleFactor, self.exponent) if i == 0 else 1.0
                    kgsUnits.append(_node('', kgsUnit, exponent * self.exponent, scaleFactor=finalScaleFactor))
                return kgsUnits

        # Return the node as is if it's already a base unit, with adjusted scale factor
        return [_node('', self.unit, self.exponent,  scaleFactor=adjustedScaleFactor)]

    def __eq__(self, other):
        """Checks if two nodes are identical after sorting their nodes alphabetically."""
        return self.prefix == other.prefix and self.unit == other.unit and self.exponent == other.exponent and self.scaleFactor == other.scaleFactor

    def __str__(self):
        result=''

        if self.prefix !='':
            result+='\\'+self.prefix
        result = result + '\\' + self.unit
        if self.exponent != 1:
            result = result + r'\tothe{' + '{:g}'.format(float(self.exponent)) + '}'
        return result

    def isScaled(self,other):
        """Checks if two nodes are scaled equal."""
        if self.unit == other.unit and self.exponent == other.exponent:
            return _dsiPrefixesScales[other.prefix]/_dsiPrefixesScales[self.prefix]
        else:
            return math.nan

def _warn(message: str, warningClass):
    """Output warning on command line and return warning message

    Args:
        message (str): warning message
        warningClass: Warning type

    Returns:
        str: message
    """
    warnings.warn(message, warningClass)
    return message

def _getClosestStr(unknownStr):
    """returns the closest string and type of the given string

    Args:
        unknownStr (str): string to be compared

    Returns:
        str: closest string
        str: type of closest string
    """
    possibleDsiKeys = _dsiPrefixesLatex.keys() | _dsiUnitsLatex.keys() | _dsiKeyWords.keys()
    closestStr = difflib.get_close_matches(unknownStr, possibleDsiKeys, n=3,cutoff=0.66)
    return closestStr
# mapping D-SI prefixes to latex
_dsiPrefixesLatex = {
    'deca': r'\mathrm{da}',
    'hecto': r'\mathrm{h}',
    'kilo': r'\mathrm{k}',
    'mega': r'\mathrm{M}',
    'giga': r'\mathrm{G}',
    'tera': r'\mathrm{T}',
    'peta': r'\mathrm{P}',
    'exa': r'\mathrm{E}',
    'zetta': r'\mathrm{Z}',
    'yotta': r'\mathrm{Y}',
    'deci': r'\mathrm{d}',
    'centi': r'\mathrm{c}',
    'milli': r'\mathrm{m}',
    'micro': r'\micro', 
    'nano': r'\mathrm{n}',
    'pico': r'\mathrm{p}',
    'femto': r'\mathrm{f}',
    'atto': r'\mathrm{a}',
    'zepto': r'\mathrm{z}',
    'yocto': r'\mathrm{y}',
    'kibi': r'\mathrm{Ki}',
    'mebi': r'\mathrm{Mi}',
    'gibi': r'\mathrm{Gi}',
    'tebi': r'\mathrm{Ti}',
    'pebi': r'\mathrm{Pi}',
    'exbi': r'\mathrm{Ei}',
    'zebi': r'\mathrm{Zi}',
    'yobi': r'\mathrm{Yi}'
}
#TODO maybe directlusing the exponents is better
# mapping D-SI prefixes to scale factors
_dsiPrefixesScales = {
    'yotta': 1e24,
    'zetta': 1e21,
    'exa': 1e18,
    'peta': 1e15,
    'tera': 1e12,
    'giga': 1e9,
    'mega': 1e6,
    'kilo': 1e3,
    'hecto': 1e2,
    'deca': 1e1,
    '':1.0,
    'deci': 1e-1,
    'centi': 1e-2,
    'milli': 1e-3,
    'micro': 1e-6,
    'nano': 1e-9,
    'pico': 1e-12,
    'femto': 1e-15,
    'atto': 1e-18,
    'zepto': 1e-21,
    'yocto': 1e-24,
    'kibi': 1024,                       #2^10
    'mebi': 1048576,                    #2^20
    'gibi': 1073741824,                 #2^30
    'tebi': 1099511627776,              #2^40
    'pebi': 1125899906842624,           #2^50
    'exbi': 1152921504606846976,        #2^60 larger than 2^53 so quantization error is possible
    'zebi': 1180591620717411303424,     #2^70 larger than 2^53 so quantization error is possible
    'yobi': 1208925819614629174706176   #2^80 larger than 2^53 so quantization error is possible
}
# UTF-8 equivalents for SI prefixes
_dsiPrefixesUTF8 = {
    'deca': 'da',
    'hecto': 'h',
    'kilo': 'k',
    'mega': 'M',
    'giga': 'G',
    'tera': 'T',
    'peta': 'P',
    'exa': 'E',
    'zetta': 'Z',
    'yotta': 'Y',
    'deci': 'd',
    'centi': 'c',
    'milli': 'm',
    # Unicode character for micro: 'µ' (U+00B5)
    'micro': 'µ',
    'nano': 'n',
    'pico': 'p',
    'femto': 'f',
    'atto': 'a',
    'zepto': 'z',
    'yocto': 'y',
    'kibi': 'Ki',
    'mebi': 'Mi',
    'gibi': 'Gi',
    'tebi': 'Ti',
    'pebi': 'Pi',
    'exbi': 'Ei',
    'zebi': 'Zi',
    'yobi': 'Yi'
}
# mapping D-SI units to latex
_dsiUnitsLatex = {
    'metre': r'\mathrm{m}',
    'kilogram': r'\mathrm{kg}',
    'second': r'\mathrm{s}',
    'ampere': r'\mathrm{A}',
    'kelvin': r'\mathrm{K}',
    'mole': r'\mathrm{mol}',
    'candela': r'\mathrm{cd}',
    'one': r'1',
    'day': r'\mathrm{d}',
    'hour': r'\mathrm{h}',
    'minute': r'\mathrm{min}',
    'degree': r'^\circ',
    'arcminute': r"'",
    'arcsecond': r"''",
    'gram': r'\mathrm{g}',
    'radian': r'\mathrm{rad}',
    'steradian': r'\mathrm{sr}',
    'hertz': r'\mathrm{Hz}',
    'newton': r'\mathrm{N}',
    'pascal': r'\mathrm{Pa}',
    'joule': r'\mathrm{J}',
    'watt': r'\mathrm{W}',
    'coulomb': r'\mathrm{C}',
    'volt': r'\mathrm{V}',
    'farad': r'\mathrm{F}',
    'ohm': r'\Omega',
    'siemens': r'\mathrm{S}',
    'weber': r'\mathrm{Wb}',
    'tesla': r'\mathrm{T}',
    'henry': r'\mathrm{H}',
    'degreecelsius': r'^\circ\mathrm{C}',
    'lumen': r'\mathrm{lm}',
    'lux': r'\mathrm{lx}',
    'becquerel': r'\mathrm{Bq}',
    'sievert': r'\mathrm{Sv}',
    'gray': r'\mathrm{Gy}',
    'katal': r'\mathrm{kat}',
    'hectare': r'\mathrm{ha}',
    'litre': r'\mathrm{l}',
    'tonne': r'\mathrm{t}',
    'electronvolt': r'\mathrm{eV}',
    'dalton': r'\mathrm{Da}',
    'astronomicalunit': r'\mathrm{au}',
    'neper': r'\mathrm{Np}',
    'bel': r'\mathrm{B}',
    'decibel': r'\mathrm{dB}',
    'percent':r'\%',
    'byte': r'\byte',
    'bit': r'\bit',
}
# Comprehensive mapping from ASCII/UTF-8 representations to D-SI LaTeX strings
ascii_to_dsi_unit_map = {
    'kg': 'kilogram',
    'm': 'metre',
    's': 'second',
    'A': 'ampere',
    'K': 'kelvin',
    'mol': 'mole',
    'cd': 'candela',
    'g': 'gram',
    'rad': 'radian',
    'sr': 'steradian',
    'Hz': 'hertz',
    'N': 'newton',
    'Pa': 'pascal',
    'J': 'joule',
    'W': 'watt',
    'C': 'coulomb',
    'V': 'volt',
    'F': 'farad',
    'Ω': 'ohm',
    'S': 'siemens',
    'Wb': 'weber',
    'T': 'tesla',
    'H': 'henry',
    '°C': 'degreecelsius',
    'lm': 'lumen',
    'lx': 'lux',
    'Bq': 'becquerel',
    'Gy': 'gray',
    'Sv': 'sievert',
    'kat': 'katal',
    '%': 'percent',
    'ppm' : 'ppm',
    'B': 'byte',
    'bit': 'bit',
    # Add more units as needed
}

_dsiUnitsUTF8 = {
    'metre': 'm',
    'kilogram': 'kg',
    'second': 's',
    'ampere': 'A',
    'kelvin': 'K',
    'mole': 'mol',
    'candela': 'cd',
    'one': '1',
    'day': 'd',
    'hour': 'h',
    'minute': 'min',
    'degree': '°',
    'arcminute': '′',
    'arcsecond': '″',
    'gram': 'g',
    'radian': 'rad',
    'steradian': 'sr',
    'hertz': 'Hz',
    'newton': 'N',
    'pascal': 'Pa',
    'joule': 'J',
    'watt': 'W',
    'coulomb': 'C',
    'volt': 'V',
    'farad': 'F',
    'ohm': 'Ω',
    'siemens': 'S',
    'weber': 'Wb',
    'tesla': 'T',
    'henry': 'H',
    'degreecelsius': '°C',
    'lumen': 'lm',
    'lux': 'lx',
    'becquerel': 'Bq',
    'sievert': 'Sv',
    'gray': 'Gy',
    'katal': 'kat',
    'hectare': 'ha',
    'litre': 'l',
    'tonne': 't',
    'electronvolt': 'eV',
    'dalton': 'Da',
    'astronomicalunit': 'au',
    'neper': 'Np',
    'bel': 'B',
    'decibel': 'dB',
    'percent': '%',
    'ppm' : 'ppm',
    'byte': 'B',
    'bit': 'bit',
}

_derivedToBaseUnits = {
    # Time units
    'day': [('second', 1, 86400)],         # 1 day = 86400 seconds
    'hour': [('second', 1, 3600)],         # 1 hour = 3600 seconds
    'minute': [('second', 1, 60)],         # 1 minute = 60 seconds

    # Angle units
    'degree': [('radian', 1, math.pi/180)], # 1 degree = π/180 radians
    'arcminute': [('radian', 1, math.pi/10800)], # 1 arcminute = π/10800 radians
    'arcsecond': [('radian', 1, math.pi/648000)], # 1 arcsecond = π/648000 radians

    # Mass units
    'gram': [('kilogram', 1, 0.001)],  # 1 gram = 0.001 kilograms

    # Derived units
    'hertz': [('second', -1,1)],  # 1 Hz = 1/s
    'newton': [('kilogram', 1, 1), ('metre', 1, 1), ('second',-2, 1)],  # 1 N = 1 kg·m/s²
    'pascal': [('kilogram', 1, 1), ('metre',-1, 1), ('second',-2, 1)],  # 1 Pa = 1 kg/m·s²
    'joule': [('kilogram', 1, 1), ('metre',2, 1), ('second',-2, 1)],  # 1 J = 1 kg·m²/s²
    'watt': [('kilogram', 1, 1), ('metre',2, 1), ('second',-3, 1)],  # 1 W = 1 kg·m²/s³
    'coulomb': [('second', 1, 1), ('ampere', 1, 1)],  # 1 C = 1 s·A
    'volt': [('kilogram', 1, 1), ('metre',2, 1), ('second',-3, 1), ('ampere',-1, 1)],  # 1 V = 1 kg·m²/s³·A
    'farad': [('kilogram',-1, 1), ('metre',-2, 1), ('second', 4, 1), ('ampere',2, 1)],# 1 F = 1 kg⁻¹·m⁻²·s⁴·A²
    'ohm': [('kilogram', 1, 1), ('metre',2, 1), ('second',-3, 1), ('ampere',-2, 1)],  # 1 Ω = 1 kg·m²/s³·A⁻²
    'siemens': [('kilogram',-1, 1), ('metre',-2, 1), ('second',3, 1), ('ampere',2, 1)],# 1 S = 1 kg⁻¹·m⁻²·s³·A²
    'weber': [('kilogram', 1, 1), ('metre',2, 1), ('second',-2, 1), ('ampere',-1, 1)],  # 1 Wb = 1 kg·m²/s²·A
    'tesla': [('kilogram', 1, 1), ('second',-2, 1), ('ampere',-1, 1)],  # 1 T = 1 kg/s²·A
    'henry': [('kilogram', 1, 1), ('metre',2, 1), ('second',-2, 1), ('ampere',-2, 1)],  # 1 H = 1 kg·m²/s²·A²
    #'degreecelsius': [('kelvin', 1, 1)], # Degree Celsius is a scale, not a unit; the unit is Kelvin
    'lumen': [('candela', 1, 1), ('steradian', 1, 1)], # 1 lm = 1 cd·sr #TODO full conversion to base units
    'lux': [('candela', 1, 1), ('steradian', 1, 1), ('metre',-2, 1)], # 1 lx = 1 cd·sr/m² #TODO full conversion to base units
    'becquerel': [('second',-1, 1)], # 1 Bq = 1/s
    'sievert': [('metre',2, 1), ('second',-2, 1)], # 1 Sv = 1 m²/s²
    'gray': [('metre',2, 1), ('second',-2, 1)], # 1 Gy = 1 m²/s²
    'katal': [('mole', 1, 1), ('second',-1, 1)], # 1 kat = 1 mol/s
    # Other units
    'hectare': [('metre',2, 10000)],  # 1 ha = 10000 m²
    'litre': [('metre',3, 0.001)],  # 1 L = 0.001 m³
    'tonne': [('kilogram', 1, 1000)],  # 1 t = 1000 kg
    'electronvolt': [('joule', 1, 1.602176634e-19)],  # 1 eV = 1.602176634 × 10⁻¹⁹ J
    'dalton': [('kilogram', 1, 1.66053906660e-27)],  # 1 Da = 1.66053906660 × 10⁻²⁷ kg
    'astronomicalunit': [('metre', 1, 149597870700)],  # 1 AU = 149597870700 m
    'neper': [('one', 1,1)],  # Neper is a logarithmic unit for ratios of measurements, not directly convertible
    'bel': [('one', 1,1)],  # Bel is a logarithmic unit for ratios of power, not directly convertible
    'decibel': [('one', 1,1)],  # Decibel is a logarithmic unit for ratios of power, not directly convertible
    'byte':[('bit',1,8)], ## TODO overthink this
# Note: For logarithmic units like neper, bel, and decibel, conversion to base units is not straightforward due to their nature.
}
_additionalConversions = {
    # Conversions for ampere, volt, and mole into kg, s, m equivalents
    'volt': [('metre', 2, 1), ('kilogram', 1, 1), ('second', -3, 1), ('ampere', -1, 1)],  # V = kg·m²/s³·A⁻¹
    'percent':[('one',1,0.01)],
    'ppm':[('one',1,1e-6)],
    'byte':[('one',1,8)],
    'bit':[('one',1,1)],
    # Note: These are placeholders and need to be adjusted to reflect accurate conversions.
}
_dsiKeyWords = {
    'tothe': r'\tothe',
    'per': r'\per'}
# This file is part of dccQuantities (https://gitlab1.ptb.de/digitaldynamicmeasurement/dccQuantities)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB), Thomas Bruns(PTB)]
# (PTB) Physikalisch Technsiche Bundesanstalt, Bundesallee 100, 38116 Braunschweig, Germany
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import warnings
from functools import reduce
import operator
from typing import Union
import datetime
# for type annotations
import copy
import json
import numpy as np
# import scipy.interpolate
# for interpolation methods
import scipy as sp
from uncertainties import ufloat
from uncertainties import unumpy
import re
from requests import post
import pandas as pd
import io
import base64
import hashlib
from dccQuantitiesConfiguration import ToleranceSettings

from dccXMLJSONConv.dccConv import JSONToXML
from dccQuantitiesConfiguration import XMLConversionSettings
from dsiUnits import dsiUnit
from importlib.metadata import version
from packaging import version as versionParser
XMLConversionSettings.dccRestServer = None
timeout=0.5
def createXML(
    dccListDict,
    dccRestServer: str = XMLConversionSettings.dccRestServer,
    proxies: dict = XMLConversionSettings.proxies,
):
    js_dict = {"js": dccListDict}
    if dccRestServer is not None:
        try:
            response = post(dccRestServer + "json2dcc/", json=js_dict, proxies=proxies,timeout=(0.1, 5))
            if response.ok:
                # filter the requested dcc/xml from the full response-object
                xml_txt = response.text
                # print(xml_txt)
            else:
                # if it failed give some information, why
                print("invalid response: %s" % response.reason)
                print("invalid response: %s" % response.text)
                print(json.loads(response.text)["detail"])
        except:
            xml_txt = JSONToXML(dccListDict)
    else:
        xml_txt = JSONToXML(dccListDict)
    return xml_txt


def checkdccQuantitiesVersionCompatibility(versionToCheck: str):
    """Checks if given version number is compatible with current version of this software

    Args:
        versionToCheck (str): version of the loaded Data

    Raises:
        RuntimeWarning: Version mismatch

    Returns:
        bool: whether it works or not
    """
    ownVersion = versionParser.parse(version("dccQuantities"))
    otherVersion = versionParser.parse(versionToCheck)
    return (otherVersion.major == ownVersion.major and otherVersion.minor == ownVersion.minor)

def parseDCCContent(content):
    result={}
    try:
         content=content['dcc:content']
    except:
        pass
    if isinstance(content,list):
        for langlistEntry in content:
            result[langlistEntry['@lang']]=langlistEntry['#text']
    else:
        raise NotImplementedError()
        pass
    return result
class dsiJSONEncoder(json.JSONEncoder):
    """inherit form JSONEncoder, implements additional serializer"""

    def default(self, obj):
        """actual encoder

        Args:
            obj: object to encode

        Returns:
            str: serialized object
        """
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dccQuantityInterpolator):
            return obj.toDict()
        if isinstance(obj, dccQuantity):
            return obj.jsonDumps()
        if isinstance(obj, dccQuantityTable):
            return obj.jsonDumps()
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        #if isinstance(obj, dsiDCC):
        #    return obj.jsonDumps()
        if isinstance(obj, dsiUnit):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


# TODO implement actual software for this task
DsiASCIConversion = {
    "Hz": r"\hertz",
    "m/s^2": r"\metre\second\tothe{-2}",
    "mV/(m/s^2)": r"\milli\volt\metre\tothe{-2}\second\tothe{2}",
    "%": r"\percent",
    "degree": r"\degree",
    "pC/(m/s^2)": r"\pico\coulomb\metre\tothe{-1}\second\tothe{2}",
    "None": "",
}

revd = dict([reversed(i) for i in DsiASCIConversion.items()])
DsiASCIConversion.update(revd)
del revd

# conversion block ends here


def npArrayToXMLList(values, uncers=None):
    """turns a numpy array into one or two XML strings (space-separated)

    Args:
        values (np.array): values to be included in the xml str
        uncers (np.array, optional): absolute uncertainties, if given rounds the values correctly and returns a list of uncertainties as well. Defaults to None.

    Raises:
        RuntimeError: if arrays have the wrong dimension
        ValueError: if array lengths do not match

    Returns:
        str: one string if no uncers are given, two if uncers are given
    """
    if values.ndim != 1:
        raise RuntimeError(
            "conversion only supported for 1D Array but Array is "
            + str(values.ndim)
            + " dimensional"
        )
    if uncers is not None:
        originalUncerWasNone = False
        if len(uncers) != len(values):
            if uncers == "round":
                originalUncerWasNone = True
                uncers = np.floor(np.log10(values))
                uncers = np.power(10, uncers)
    else:
        originalUncerWasNone = True
    valuesSTR = ""
    uncersSTR = ""
    if uncers is None:
        uncers = np.zeros_like(values) * np.nan
    uarr = unumpy.uarray(values, std_devs=uncers)
    for i in range(len(values)):
        rawStr = "{:.2u}".format(uarr[i])
        if rawStr.startswith("("):  # okaaay we have an exponent
            number, exp = rawStr.split(")")
            number = number[1:]  # remove leading "C"
            vStr, uStr = number.split("+/-")
            vStr += exp
            uStr += exp
            valuesSTR += vStr + " "
            uncersSTR += uStr + " "
        else:
            vStr, uStr = "{:.2u}".format(uarr[i]).split("+/-")
            valuesSTR += vStr + " "
            uncersSTR += uStr + " "
    if originalUncerWasNone:
        return valuesSTR[:-1]  # remove last space
    else:
        return valuesSTR[:-1], uncersSTR[:-1]  # remove last space


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {}
    # TODO change to complete usage of u array an remove own comparison operation
    try:
        shared_keys.remove('uarray')
    except:
        pass
    for o in shared_keys:
        # Use numpy.isclose for comparison with tolerance for floating-point arithmetic
        if isinstance(d1[o], (float, np.ndarray)) and isinstance(d2[o], (float, np.ndarray)):
            if not np.isclose(d1[o], d2[o], atol=ToleranceSettings.atol, rtol=ToleranceSettings.rtol).all():  # You can adjust atol and rtol as needed
                modified[o] = (d1[o], d2[o])
        elif d1[o] != d2[o]:  # Fallback for non-floating-point types
            modified[o] = (d1[o], d2[o])
    same = set(o for o in shared_keys if o not in modified)
    return added, removed, modified, same

def hex_to_base64(hex_string):
    # Convert the hex string to bytes
    bytes_data = bytes.fromhex(hex_string)

    # Encode these bytes in base64
    base64_encoded = base64.b64encode(bytes_data)

    # Convert to string for readable output
    return base64_encoded.decode()

def md5_hash(input_string):
    # Create a new MD5 hash object
    hash_obj = hashlib.md5()

    # Update the hash object with the bytes of the input string
    hash_obj.update(input_string.encode('utf-8'))

    # Return the hexadecimal representation of the digest
    return hash_obj.hexdigest()

def find_overlapping_indices(arr1, arr2, tolerance=np.finfo(float).eps):
    # Create a matrix of differences
    diffs = np.abs(arr1[:, np.newaxis] - arr2)

    # Initialize lists to store indices
    indices_arr1 = []
    indices_arr2 = []

    for i in range(len(arr1)):
        # Find indices in arr2 where the difference is within the tolerance
        matching = np.where(diffs[i, :] <= tolerance)[0]

        # Check if there is exactly one matching element
        if len(matching) == 1:
            indices_arr1.append(i)
            indices_arr2.append(matching[0])
        elif len(matching) > 1:
            # Issue a warning if more than one match is found
            warnings.warn(f"Multiple matches found for arr1 index {i}; values ignored.")

    return np.array(indices_arr1), np.array(indices_arr2)

def combineMultiLangNameDicts(first,second,operator):
    resultDict={}
    languages = set(first.keys()) | set(second.keys())
    for lang in languages:
        try:
            resultDict[lang]=str(first[lang])+' '+str(operator)+' '+str(second[lang])
        except KeyError:
            warnings.warn("Key Error in Multilang name creation for language "+str(lang))
    return resultDict

class dccQuantity:
    """represents a value vector with uncer, can be serialized to both JSON and XML"""

    supportedUncerTypes = ["absolute", "rel", "relPercent", "relPPM"]

    def __init__(
        self,
        values: np.ndarray,
        uncer: Union[np.ndarray, None],
        ID: str,
        unit: str,
        uncerType: str = "absolute",
        refTypes: list = None,
        name: dict = {
            "EN": "Dummy",
            "DE": "Platzhalter",
        },  # TODO better default handling change to None...
        uncerParams: dict = {
            "coverageFactor": 2.0,
            "coverageProbability": 0.95,
            "distribution": "normal",
        },
    ) -> dccQuantity:
        """constructor

        Args:
            values (np.ndarray): values
            uncer (np.ndarray, optional): uncers
            ID (str): name of the quantity for internal use
            unit (str): D-SI Str of the unit
            uncerType (str, optional): type of the uncer, allowed are ['absolute','rel','relPercent','relPPM']. Defaults to "absolute".
            refTypes (list, optional): list of Str with the refTypes. Defaults to None.
            name (_type_, optional): dict with languages ["de","en","it"] as keys and the corresponding name as value. Defaults to {'EN':'Dummy','DE':'Platzhalter'}.

        Returns:
            dccQuantity: D-SI Vektor
        """

        self.dataType = self.__class__.__name__
        self.dccQuantitiesVersion = version("dccQuantities")
        self.quantity = str(ID)
        self.id=str(ID)
        if type(unit) == dsiUnit:
            self.unit = unit
        elif type(unit) == str:
            self.unit = dsiUnit(unit)
        else:
            self.unit = dsiUnit(str(unit))
        if refTypes is not None:
            try:
                self.refTypes = list(refTypes.split(" "))

            except:
                try:
                    self.refTypes = list(refTypes)
                except Exception as E:
                    warnings.warn(
                        "refTypes could not be converted to a list due to,"+str(E)+" using None"
                    )
                    self.refTypes=None
        else:
            self.refTypes = None
        self.multilangnames = name
        #TODO implement better handling for uncerParams
        if type(values) == int or type(values) == float:
            values = np.array([values])
        if type(uncer) == int or type(uncer) == float:
            uncer = np.array([uncer])
        if values.dtype == 'O':
            self.uarray = values
            try:
                self.values = unumpy.nominal_values(self.uarray)#TODO remove this variables and use only the uncerFlaot data
                self.uncer = unumpy.std_devs(self.uarray)#TODO remove this variables and use only the uncerFlaot data
                self.originalUncerType = "absolute" #uncertanies from uarray are always absolute
                self.uncerParams=uncerParams # set to default uncer params since we don't know beeter
            except Exception as e:
                new_message = f"An error occurred while extracting nominal values and uncertainties Mostlikly the valus havent been an ufloat/uarray : {str(e)}"
                raise type(e)(new_message) from e
        else:
            self.uncerParams = {}
            if uncerType is not None:
                self.uncerParams = uncerParams
            if type(values) == np.array:
                self.values = values
            else:
                self.values = np.array(values)
            if type(uncer) == type(None):
                self.originalUncerType = None
                self.uncer = (
                    np.zeros_like(values) * np.NaN
                )
            else:
                # TODO better uncer handling with function dict
                if (
                    type(uncer) != np.array
                ):  # if its not an array try to convert in np.ndarray
                    uncer = np.array(uncer)
                # __uncer__ handling
                self.originalUncerType = str(uncerType)
                if uncerType == "absolute":
                    self.uncer = abs(
                        uncer
                    )  # abs not needed here but better save than sorry
                elif uncerType == "rel":
                    self.uncer = abs(uncer * self.values)
                elif uncerType == "relPercent":
                    self.uncer = abs(uncer / 100 * self.values)
                elif uncerType == "relPPM":
                    self.uncer = abs(uncer / 1e6 * self.values)
                elif uncerType == None:
                    self.uncer = np.zeros_like(self.values)
                    RuntimeWarning(
                        "Uncer Values"
                        + str(uncer)
                        + " given but uncerType is None uncer not used!"
                    )
                else:
                    raise NotImplementedError(
                        "uncerType "
                        + str(uncerType)
                        + r" is not supported/implemented use ['absolute','rel','relPercent','relPPM']"
                    )
            self.uarray = unumpy.uarray(self.values, self.uncer)
        self.isInterPolatedData = False
        self.length = len(self.values)

    @classmethod
    def fromDict(cls, dict: dict) -> dccQuantity:
        """constructs dsiVector from dict"""
        if checkdccQuantitiesVersionCompatibility(dict["dccQuantitiesVersion"]) == False:
            raise ValueError(
                "Incompatible DSI Tools Versions JSONData/This Software"
                + str(dict["dccQuantitiesVersion"])
                + " / "
                + str(version("dccQuantities"))
            )
        # change constructor so that np.arrays are created
        if dict["uncer"] == None or dict["originalUncerType"] == None:
            instance = cls(
                np.array(dict["values"]),
                dict["uncer"],
                str(dict["quantity"]),
                str(dict["unit"]),
            )
        else:
            instance = cls(
                np.array(dict["values"]),
                np.array(dict["uncer"]),
                str(dict["quantity"]),
                str(dict["unit"]),
            )
        additionalkeys = dict.keys() - set(["values", "uncer", "unit", "quantity"])
        for key in additionalkeys:
            instance.__dict__[key] = dict[key]
        return instance

    @classmethod
    def fromJson(cls, jsonstr: str) -> dccQuantity:
        """constructs dsiVector from Json using a dict"""
        dict = json.loads(jsonstr)
        return cls.fromDict(dict)

    @classmethod
    def fromDCCXMLJSON(cls, jsonObj: str) -> dccQuantity:
        if type(jsonObj) == str:
            dataDict = json.loads(jsonObj)
        if type(jsonObj) == dict:
            dataDict = jsonObj
        try:
            dataDict = dataDict["dcc:quantity"]
        except KeyError:
            pass

        def parseDCCname(dccname: dict) -> dict:
            result = {}
            names = dccname["dcc:content"]
            for name in names:
                result[name["@lang"]] = name["#text"]
            return result

        def parseSIRealXMLList(siRealXMLList: dict) -> dict:
            result = {
                "values": np.fromstring(
                    siRealXMLList["si:valueXMLList"]["#text"], dtype=float, sep=" "
                ),
                "unit": siRealXMLList["si:unitXMLList"]["#text"],
            }
            try:
                result["uncer"] = np.fromstring(
                    siRealXMLList["si:expandedUncXMLList"]["si:uncertaintyXMLList"][
                        "#text"
                    ],
                    dtype=float,
                    sep=" ",
                )
                try:
                    result["uncer_params"] = {
                        "coverageFactor": siRealXMLList["si:expandedUncXMLList"][
                            "si:coverageFactorXMLList"
                        ]["#text"],
                        "coverageProbability": siRealXMLList["si:expandedUncXMLList"][
                            "si:coverageProbabilityXMLList"
                        ]["#text"],
                        "distribution": siRealXMLList["si:expandedUncXMLList"][
                            "si:distributionXMLList"
                        ]["#text"],
                    }
                except KeyError:
                    pass
            except KeyError:
                pass
            return result

        def praseRelativeUncertainty(relativeUncertainty: dict) -> dict:
            result = np.fromstring(
                relativeUncertainty["dcc:relativeUncertaintyXmlList"][
                    "si:valueXMLList"
                ][0]["#text"],
                dtype=float,
                sep=" ",
            )
            return result

        names = parseDCCname(dataDict["dcc:name"])
        data = parseSIRealXMLList(dataDict["si:realListXMLList"])
        try:
            relUncer = praseRelativeUncertainty(dataDict["dcc:relativeUncertainty"])
            hasRelUncer = True
        except KeyError:
            hasRelUncer = False
        if not "@refType" in dataDict:
            dataDict["@refType"] = None
        unitWOF__SLASHES = data["unit"].replace("\\\\", "\\")
        if "uncer" in data:
            if hasRelUncer:
                if "uncer_params" in data:
                    result = cls(
                        data["values"],
                        relUncer,
                        names[list(names.keys())[0]],
                        unitWOF__SLASHES,
                        uncerType="rel",
                        refTypes=dataDict["@refType"],
                        name=names,
                        uncerParams=data["uncer_params"],
                    )
                else:
                    result = cls(
                        data["values"],
                        relUncer,
                        names[list(names.keys())[0]],
                        unitWOF__SLASHES,
                        uncerType="rel",
                        refTypes=dataDict["@refType"],
                        name=names,
                    )
            else:
                if "uncer_params" in data:
                    result = cls(
                        data["values"],
                        data["uncer"],
                        names[list(names.keys())[0]],
                        unitWOF__SLASHES,
                        uncerType="absolute",
                        refTypes=dataDict["@refType"],
                        name=names,
                        uncerParams=data["uncer_params"],
                    )
                else:
                    result = cls(
                        data["values"],
                        data["uncer"],
                        names[list(names.keys())[0]],
                        unitWOF__SLASHES,
                        uncerType="absolute",
                        refTypes=dataDict["@refType"],
                        name=names,
                    )
        else:
            result = cls(
                data["values"],
                None,
                names[list(names.keys())[0]],
                unitWOF__SLASHES,
                refTypes=dataDict["@refType"],
                name=names,
            )
        return result

    def interpolatedValuesTodccQuantity(
        self, values: np.ndarray, uncer: np.ndarray
    ) -> dccQuantity:
        """generates an result dsiVector with same "parameters" from interpolated values. Is intended to be used from an dsiMultiVector since there the actual interpolation ist done.

        Args:
            values (np.ndarray): values
            uncer (np.ndarray): uncers

        Returns:
            dccQuantity: result dsiVector
        """
        # change constructor so that np.arrays are created
        if type(values) != np.ndarray:
            values = np.array(values)
        else:
            if values.ndim == 0:
                values = np.array(
                    [values]
                )  # we must create an 1D Array from the scalars to have consistent Matrixdimension for all use cases
        if type(uncer) != np.ndarray:
            uncer = np.array(uncer)
        else:
            if uncer.ndim == 0:
                uncer = np.array(
                    [uncer]
                )  # we must create an 1D Array from the scalars to have consistent Matrixdimension for all use cases
        resultDSiVector = dccQuantity(
            values,
            uncer,
            self["quantity"],
            self["unit"],
            refTypes=self.refTypes,
            name=self.multilangnames,
            uncerType=self["originalUncerType"],
            uncerParams=self.uncerParams,
        )
        # additionalKeys = self.__dict__.keys() - set(['values', 'uncer', 'unit', 'quantity', 'originalUncerType'])
        # for key in additionalKeys:
        #    resultDSiVector.__dict__[key] = dict[key]
        resultDSiVector.isInterPolatedData = True
        return resultDSiVector

    def jsonDumps(self) -> str:
        """dumps to JSON

        Returns:
            str: JSON Str
        """
        # Create a deep copy of the instance's dictionary to avoid mutating the original
        dictToDump = copy.deepcopy(self.__dict__)

        # Remove the 'uarray' key from the copied dictionary
        dictToDump.pop('uarray', None)  # Use pop to remove 'uarray'; does nothing if 'uarray' is not in the dictionary

        # Handle the special case for 'uncer' when originalUncerType is None
        if self.originalUncerType != None:
            return json.dumps(dictToDump, cls=dsiJSONEncoder, indent=4).replace(
                r"\\\\", r"\\"
            )
        else:
            dictToDump = self.__dict__
            dictToDump["uncer"] = None
            return json.dumps(dictToDump, cls=dsiJSONEncoder, indent=4).replace(
                r"\\\\", r"\\"
            )

    def toDCCrealListXMLList(self, uncer: bool = True):
        """generates complete DCC <si:realListXMLList> item with absolute uncer but no relative uncer.

        Args:
            uncer (bool, optional): Should the absolute uncer be added to the XML element. Defaults to True.

        Returns:
            str:  <si:realListXMLList>
        """
        if self.multilangnames == {"EN": "Dummy", "DE": "Platzhalter"}:
            raise RuntimeError(
                "Cont generate XML JSON without an multilanguage name " + str(self)
            )
        if not uncer:
            DCCrealListXMLList = {
                "si:valueXMLList": {"#text": npArrayToXMLList(self.values)},
                "si:unitXMLList": {"#text": str(self.unit)},
            }
        if uncer:
            if self.originalUncerType is not None:
                valuesXMLList, uncerXMLList = npArrayToXMLList(self.values, self.uncer)
                expandedUncerDictContent = {}
                expandedUncerDictContent["si:uncertaintyXMLList"] = {
                    "#text": uncerXMLList
                }
                for key in self.uncerParams.keys():
                    expandedUncerDictContent["si:" + str(key) + "XMLList"] = {
                        "#text": self.uncerParams[key]
                    }
                DCCrealListXMLList = {
                    "si:valueXMLList": {"#text": valuesXMLList},
                    "si:unitXMLList": {"#text": str(self.unit)},
                    "si:expandedUncXMLList": expandedUncerDictContent,
                }
            else:
                RuntimeWarning("No uncer in " + str(self) + " Ignoring uncer")
                DCCrealListXMLList = {
                    "si:valueXMLList": {"#text": npArrayToXMLList(self.values)},
                    "si:unitXMLList": {"#text": str(self.unit)},
                }
        return DCCrealListXMLList

    def toDCCXMLQuantityStr(self, uncer: bool = True):
        """generates complete <dcc:quantity> XML str for the DCC, similar to toDCCrealListXMLList() (but one level higher)

        Args:
            uncer (bool, optional): should uncer be added . Defaults to True.

        Returns:
            str: <dcc:quantity>
        """
        langList = []
        for lang in self.multilangnames:
            langList.append({"@lang": lang,
                             "#text": str(self.multilangnames[lang]),
                             })
        if self.refTypes:
            if len(self.refTypes) == 1:
                resultDict = {
                    "@refType": self.refTypes[0],
                    "dcc:name": {"dcc:content": langList},
                    "si:realListXMLList": self.toDCCrealListXMLList(bool(uncer)),
                }
            else:
                resultDict = {
                    "@refType": " ".join(self.refTypes),
                    "dcc:name": {"dcc:content": langList},
                    "si:realListXMLList": self.toDCCrealListXMLList(bool(uncer)),
                }
        else:
            resultDict = {
                "dcc:name": {"dcc:content": langList},
                "si:realListXMLList": self.toDCCrealListXMLList(bool(uncer)),
            }
        if self.originalUncerType not in [None, "absolute"]:
            resultDict["dcc:relativeUncertainty"] = {
                "dcc:relativeUncertaintyXmlList": {
                    "si:valueXMLList": {
                        "#text": npArrayToXMLList(
                            self.__getitem__("uncer_rel"), "round"
                        )
                    },
                    "si:unitXMLList": {"#text": r"\one"},
                }
            }
        return {"dcc:quantity": resultDict}

    def toXML(self):
        json = self.toDCCXMLQuantityStr()
        XML = createXML(json)
        return XML

    def addRefType(self, refType):
        """adds an refType

        Args:
            refType (str): refType to be added.
        """
        if self.refTypes is None:
            self.refTypes=[refType]
            return
        try:
            if not refType in self.refTypes:
                self.refTypes.append(refType)
        except AttributeError:
            self.refTypes = list(refType)

    def newQuantityFromIdx(self, idx):
        if isinstance(idx, (np.ndarray, list, slice)) and (
                isinstance(idx, np.ndarray) and idx.dtype == int or isinstance(idx, (list, slice))):
            # Get the copied data using the __getitem__ method
            copyedData = self[idx]

            # Determine the uncertainty based on the original uncertainty type
            uncer = copyedData[1] if self.originalUncerType is not None else None

            # Create a new dsiVector with the copied data and the same metadata
            #TODO use ufloat constuctor hear to track partial deviations
            new_vector = dccQuantity(
                values=copyedData[0],
                uncer=uncer,
                ID=self.quantity,
                unit=self.unit,
                uncerType=self.originalUncerType,
                refTypes=self.refTypes,
                name=self.multilangnames,
                uncerParams=self.uncerParams
            )
            return new_vector
        else:
            raise ValueError(
                "newVecFromIdx only possible with a slice, np.ndarray (dtype int), or list of ints, not with " + str(
                    type(idx)))

    def convertToUnit(self, newUnit: [str,dsiUnit]):
        """converts the values and uncer to a new unit
        Args:
            newUnit (str): new unit
        """
        if type(newUnit) == str:
            newUnit = dsiUnit(newUnit)
        if self.unit == newUnit:
            return
        scaleFactor,baseUnit = newUnit.isScalablyEqualTo(self.unit) # n*self.unit =1 other.unit
        if baseUnit is not None:
            self.uarray = self.uarray * scaleFactor
            self.values = unumpy.nominal_values(
                self.uarray)  # TODO remove this variables and use only the uncerFlaot data
            self.uncer = unumpy.std_devs(self.uarray)  # TODO remove this variables and use only the uncerFlaot data
            self.unit = newUnit
        else:
            raise ValueError("Actual unit "+str(self.unit.toUTF8())+" and new unit"+str(newUnit.toUTF8())+" are not scalably equal")

    def __getitem__(self, item):
        """See pyDCCToolsExamplesNoteBook.ipynb for detailed indexing Examples"""
        # print(key)
        if type(item) == int:
            if self.originalUncerType is not None:
                return (self.values[item], self.uncer[item])
            else:
                return (self.values[item], np.NaN)
        elif type(item) == slice:
            # TODO improve and check fancy slice indexing
            if self.originalUncerType is not None:
                return (self.values[item], self.uncer[item])
            else:
                return (self.values[item], self.values[item] * np.NaN)
        elif type(item) == str:
            if item != "uncer":
                try:
                    return self.__dict__[item]
                except KeyError:
                    if item == "uarray":
                        return self.uarray
                    elif item == "uncer_relPercent":
                        return abs(self.uncer / self.values * 100)
                    elif item == "uncer_relPPM":
                        return abs(self.uncer / self.values * 1e6)
                    elif item == "uncer_rel":
                        return abs(self.uncer / self.values)
                    else:
                        raise KeyError(
                            item
                            + " not supported try:"
                            + str(list(self.__dict__.keys()))
                            + r" or ['uncer_rel','uncer_relPercent','uncer_relPPM]"
                        )
            else:
                if self.originalUncerType != None:
                    return self.uncer
                else:
                    return np.zeros_like(self.values) * np.NaN

        elif type(item) == tuple:
            if type(item[0]) == str and type(item[1]) == int:
                if not item[0] == "uncer":
                    try:
                        return self.__dict__[item[0]][item[1]]
                    except KeyError:
                        if item[0] == "uncer_relPercent":
                            return abs(self.uncer[item[1]] / self.values[item[1]] * 100)
                        elif item[0] == "uncer_relPPM":
                            return abs(self.uncer[item[1]] / self.values[item[1]] * 1e6)
                        elif item[0] == "uncer_rel":
                            return abs(self.uncer[item[1]] / self.values[item[1]])
                        else:
                            raise KeyError(
                                item
                                + " not supported try:"
                                + str(list(self.__dict__.keys()))
                                + r" or ['uncer_relPercent','uncer_relPPM]"
                            )
                else:
                    if self.originalUncerType != None:
                        return self.uncer[item[1]]
                    else:
                        return np.NaN
            elif type(item[0]) == str and type(item[1]) == slice:
                if not item[0] == "uncer":
                    try:
                        return self.__dict__[item[0]][item[1]]
                    except KeyError:
                        if item[0] == "uncer_relPercent":
                            return abs(self.uncer[item[1]] / self.values[item[1]] * 100)
                        elif item[0] == "uncer_relPPM":
                            return abs(self.uncer[item[1]] / self.values[item[1]] * 1e6)
                        elif item[0] == "uncer_rel":
                            return abs(self.uncer[item[1]] / self.values[item[1]])
                        else:
                            raise KeyError(
                                item
                                + " not supported try:"
                                + str(list(self.__dict__.keys()))
                                + r" or ['uncer_relPercent','uncer_relPPM]"
                            )
                else:
                    if self.originalUncerType != None:
                        return self.uncer[item[1]]
                    else:
                        return np.zeros_like(self.values) * np.NaN[item[1]]

            else:
                raise KeyError("Second tuple element in neither int nor slice.")
        elif type(item) == list:
            return self.__getitem__(np.array(item))
        # Handling NumPy array indexing
        elif isinstance(item, np.ndarray) and item.dtype == int:
            if self.originalUncerType is not None:
                return (self.values[item], self.uncer[item])
            else:
                return (self.values[item], np.full(item.shape, np.NaN))
        else:
            raise KeyError(
                str(item)
                + "from type "
                + str(type(item))
                + " Not supported try dsiVector[int], dsiVector["
                + str(list(self.__dict__.keys()))
                + r" or 'uncer_relPercent','uncer_relPPM"
                + "dsiVector[values,int] or dsiVector['uncer',int]"
            )


    def __str__(self) -> str:
        length = self["values"].size
        interpolatedPrefix = ""
        if self.isInterPolatedData:
            interpolatedPrefix = "Interpolated "
        string = (
            interpolatedPrefix
            + str(self["quantity"])
            + " in "
            + dsiUnit(str(self["unit"])).toUTF8()# todo looks odd need to be checked
            + " len="
            + str(length)
            + " "
        )
        if self.originalUncerType != None:
            if length == 1:
                string = string + str(ufloat(self[0]).format("2u")) + " "
            elif length < 8:
                for i in range(length):
                    string = string + str(ufloat(self[i]).format("2u")) + " "
            else:
                firstBlock = ""
                secondBlock = ""
                for i in range(4):
                    firstBlock = firstBlock + "{:.2f}".format(ufloat(self[i])) + " "
                    secondBlock = (
                        secondBlock + "{:.2f}".format(ufloat(self[-(i + 1)])) + " "
                    )
                string = string + firstBlock + " ... " + secondBlock
            return string
        else:
            if length == 1:
                string = string + str(self[0][0]) + " "
            elif length < 8:
                for i in range(length):
                    string = string + str(self[i][0]) + " "
            else:
                firstBlock = ""
                secondBlock = ""
                for i in range(4):
                    firstBlock = firstBlock + str(self[i][0]) + " "
                    secondBlock = secondBlock + str(self[-(i + 1)][0]) + " "
                string = string + firstBlock + " ... " + secondBlock
            return string

    def __repr__(self) -> str:
        return str(self.dataType) + " @ " + hex(id(self)) + " " + self.__str__()

    def __len__(self):
        return self.length

    def __eq__(self, x):
        try:
            added, removed, modified, same = dict_compare(self.__dict__, x.__dict__)
        except:
            print("Debug ME")
        if added == set() and removed == set() and modified == {}:
            return True
        else:
            if (
                added == set()
                and removed == set()
                and list(modified.keys()) == ["uncer"]
            ):
                return (
                    np.isnan(self.uncer).all()
                    and np.isnan(x.uncer).all()
                    and len(self.uncer) == len(x.uncer)
                )
            elif (
                added == set()
                and removed == set()
                and set(list(modified.keys())).issubset(
                    set(["originalUncerType", "uncer", "values"])
                )
            ):
                uncerTypeIsOK = False
                valueMatch = False
                uncerMatch = False
                if "originalUncerType" in set(list(modified.keys())):
                    if not "absolute" in modified["originalUncerType"]:
                        uncerTypeIsOK = True  # TODO overthink this implementation
                else:
                    uncerTypeIsOK = True
                if "values" in set(list(modified.keys())):
                    valueMatch = np.allclose(
                        modified["values"][0], modified["values"][1],atol=ToleranceSettings.atol, rtol=ToleranceSettings.rtol
                    )
                else:
                    valueMatch = True
                if "uncer" in set(list(modified.keys())):
                    uncerMatch = np.allclose(modified["uncer"][0], modified["uncer"][1],atol=ToleranceSettings.atol, rtol=ToleranceSettings.rtol)
                else:
                    uncerMatch = True
                return np.all([uncerTypeIsOK, valueMatch, uncerMatch])
            return False

    def __checkMathCompatibility(self, other):
        if not isinstance(other, dccQuantity):
            raise ValueError("Only dsiVector can be added to dsiVector")
        if len(self) != len(other):
            if len(other)==1:
                saclfactor, baseunit = self.unit.isScalablyEqualTo(other.unit)
                if not saclfactor:
                    raise ValueError("Both vectors must have a convertible unit")
                return saclfactor, baseunit
            raise ValueError("Length of both vectors must be equal")
        if self.unit != other.unit:
            saclfactor, baseunit = self.unit.isScalablyEqualTo(other.unit)
            if not saclfactor:
                raise ValueError("Both vectors must have a convertible unit")
        else:
            saclfactor = 1
            baseunit=self.unit
        return saclfactor,baseunit
    def __add__(self, other):
        scalefactor,baseunit=self.__checkMathCompatibility(other)
        mathResult=self.uarray + scalefactor * other.uarray
        multiLangNames = combineMultiLangNameDicts(self.multilangnames,
                                                   other.multilangnames,
                                                   '+')
        return dccQuantity(mathResult,
                            None,
                            str(self.id) + '+' + str(other.id),
                            baseunit,
                            name=multiLangNames)

    def __sub__(self, other):
        scalefactor,baseunit=self.__checkMathCompatibility(other)
        mathResult=self.uarray-other.uarray*scalefactor
        multiLangNames=combineMultiLangNameDicts(self.multilangnames,other.multilangnames,'-')
        return dccQuantity(mathResult, None, str(self.quantity) + '-' + str(other.quantity), baseunit, name=multiLangNames)
    def __mul__(self, other):
        mathResult=self.uarray*other.uarray
        multiLangNames = combineMultiLangNameDicts(self.multilangnames, other.multilangnames, '*')
        return dccQuantity(mathResult, None, str(self.quantity) + '*' + str(other.quantity), self.unit * other.unit, name=multiLangNames)

    def __truediv__(self, other):
        mathResult=self.uarray/other.uarray
        multiLangNames = combineMultiLangNameDicts(self.multilangnames, other.multilangnames, '/')
        return dccQuantity(mathResult, None, str(self.quantity) + '/' + str(other.quantity), self.unit / other.unit, name=multiLangNames)

    def __hash__(self):
        return hash(self.jsonDumps())

    def getPDMetaData(self):
        if self.originalUncerType == None:
            # only one Col 
            df=pd.DataFrame.from_dict(
                {
                'quantity':self.quantity,
                'unit':str(self.unit),
                'refTypes':str(self.refTypes).lstrip('[').rstrip(']') if self.refTypes else '',
                'multiLangNames':str(self.multilangnames)
                }      
            ,orient='index')
        elif self.originalUncerType == 'absolute':
            # only two Col 
            df=pd.DataFrame.from_dict(
                {
                'quantity':[self.quantity, self.quantity+" Abs. Uncer."],
                'unit':[str(self.unit),str(self.unit)],
                'refTypes':[str(self.refTypes).lstrip('[').rstrip(']') if self.refTypes else '',''],
                'multiLangNames':[str(self.multilangnames),'']
                }      
            ,orient='index')
        else: # relative uncertainty
            # only two Col 
            """
            elif uncerType == "rel":
                self.uncer = abs(uncer * self.values)
            elif uncerType == "relPercent":
                self.uncer = abs(uncer / 100 * self.values)
            elif uncerType == "relPPM":
            """
            uncerUnits={'rel':r'\one','relPercent':r'\percent','relPPM':r'\one'}
            df=pd.DataFrame.from_dict(
                {
                'quantity':[self.quantity, self.quantity+' '+self.originalUncerType],
                'unit':[str(self.unit),uncerUnits[self.originalUncerType]],
                'refTypes':[str(self.refTypes).lstrip('[').rstrip(']') if self.refTypes else '',''],
                'multiLangNames':[str(self.multilangnames),'']
                }      
            ,orient='index')
        return df

    def getPDData(self):
        if self.originalUncerType == None:
        # only one Col 
            df=pd.DataFrame(data=[self['values']])#ggf. transpose
        elif self.originalUncerType == 'absolute':
        # only two Col 
            df=pd.DataFrame(data=[self['values'],self['uncer']])
        else: # relative uncertainty
            df=pd.DataFrame(data=[self['values'],self['uncer_'+self.originalUncerType]])
        return df

class dccQuantityTable:
    def __init__(
        self,
        indexQuants: [dccQuantity],
        valueQuants: [dccQuantity],
        interpolationTypes: dict = None,
        multiLangNames=None,
        multiLangDscp=None,
        refTypes=[]
    ) -> dccQuantityTable:  # TODO add interpolation args
        """Creates D-SI MultiVector

        Args:
            indexQuants (dsiVector]): index Vectors
            valueVectors (dsiVector]): data vectors
            interpolationTypes (dict, optional): supported are all methods from https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html#scipy.interpolate.interp1d. Defaults to None.

        Returns:
            dccQuantityTable: _description_
        """
        self.dataType = self.__class__.__name__
        self.dccQuantitiesVersion = version("dccQuantities")
        if not isinstance(indexQuants, list):
            self.index = [copy.copy(indexQuants)]
        else:
            self.index = copy.copy(indexQuants)
        self.indexDim = len(self.index)
        for i, index in enumerate(self.index):
            index.addRefType("basic_TableIndex" + str(i))
        self.tablerefType = "basic_" + str(self.indexDim) + "IndexTable"
        self.setRefTypes(refTypes)
        self.valueQuantites=[]
        self.valueQuantityNames = [] # will be filled later since we have to check if all quantities have the same length and care for interpolation
        self.indexQuantityNames = [index.quantity for index in self.index]
        self.interpolationTypes = interpolationTypes
        # check if all quantities have the same length
        vectorLens = []
        for vec in self.index + valueQuants:
            vectorLens.append(len(vec))
        vectorLens = np.array(vectorLens)
        if not np.all(vectorLens == vectorLens[0]):
            raise ValueError(
                "All vectors must have the same length"
            )  # TODO add detailed error which vectors do not match
        if interpolationTypes != None:
            if len(self.index) > 1:
                interpolationTypes = None
                raise RuntimeWarning(
                    "interpolation with multi indexing is not supported at the moment"
                )
            else:
                self.interpolators = {}
        for valueQuant in valueQuants:
            self.valueQuantityNames.append(valueQuant["quantity"])
            if interpolationTypes != None:
                try:
                    interPolatorTypeToUse = interpolationTypes[valueQuant["quantity"]]
                except KeyError:
                    try:
                        interPolatorTypeToUse = interpolationTypes["default"]
                    except KeyError:
                        raise KeyError(
                            "Neither specific interpolator Type for quantity "
                            + str(valueQuant["quantity"])
                            + " nor default interpolator typ was given.\n Use an dict with interpolator types like {'quantity1':'linear','default':'nearest'}"
                        )
                if len(self.index[0]) == len(valueQuant):
                    self.interpolators[valueQuant["quantity"]] = dccQuantityInterpolator(
                        self.index[0], valueQuant, interPolatorTypeToUse
                    )
                else:
                    raise ValueError(
                        "X>"
                        + str(len(self.index[0]))
                        + " and Y>"
                        + str(len(valueQuant))
                        + " vector length for interpolator do not match, no interpolator created"
                    )
            #self.__dict__[valueQuant["quantity"]] = valueQuant # TODO remove this overengeenered solution and use self.valueQuantites
            self.valueQuantites.append(valueQuant)
        self.language = []
        for quant in self.index + self.valueQuantites:
            self.language.append(list(quant.multilangnames.keys()))
        languagesMatch = True
        # instead of setting self.language to None after mismatch we need to return the matching keys even if not all dsiVectors contain all multiLanguage keys
        for langKey in self.language:
            if sorted(self.language[0]) != sorted(langKey):
                languagesMatch = False
        if languagesMatch:
            self.language = sorted(self.language[0])
        else:
            raise RuntimeWarning("Multilanguage keys do not match!")
            self.language = None
        self.name = ""
        if multiLangNames==None:
            for index in self.index:
                self.name += str(index.quantity)[:8]
            for valueQuant in valueQuants:
                self.name += "_" + str(valueQuant.quantity)[:8]
        else:
            try:
                self.name=multiLangNames['en']
            except KeyError:
                self.name=multiLangNames[list(multiLangNames.keys())[0]]
        self.name=hex_to_base64(md5_hash(self.dump_csv()))[:4]+'_'+self.name[:50]
        self.multiLangNames=multiLangNames
        self.multiLangDscp=multiLangDscp

    def setRefTypes(self,refTypes):
        self.refTypes = [s for s in refTypes if not re.match(r"basic_\dIndexTable", s)]

    @classmethod
    def fromDict(cls, dict: dict) -> dccQuantityTable:
        """constructs dsiMultiVector from dict"""
        if checkdccQuantitiesVersionCompatibility(dict["dccQuantitiesVersion"]) == False:
            raise ValueError(
                "Incompatible DSI Tools Versions JSONData/This Software"
                + str(dict["dccQuantitiesVersion"])
                + " / "
                + str(version("dccQuantities"))
            )
        indexDSIVectors = []
        for indexVectorSTR in dict["index"]:
            indexDSIVectors.append(dccQuantity.fromJson(indexVectorSTR))
        valueVectorQuantities = dict["valueQuantites"]
        valueVectors = []
        for valueVectorQuantity in valueVectorQuantities:
            valueVectors.append(dccQuantity.fromJson(valueVectorQuantity))
        instance = dccQuantityTable(
            indexDSIVectors, valueVectors, interpolationTypes=dict["interpolationTypes"]
        )
        # TODO change interpolator handling
        additionalKeys = dict.keys() - set(
            ["index", "valueQuantites","interpolators"]
        )
        for key in additionalKeys:
            instance.__dict__[key] = dict[key]
        return instance

    @classmethod
    def fromJson(cls, jsonStr: str) -> dccQuantityTable:
        """constructs dsiMultiVector from JSON using a dict"""
        if isinstance(jsonStr, str):
            dic = json.loads(jsonStr)
        elif isinstance(jsonStr, dict):
            dic = jsonStr
        else:
            raise TypeError(f"jsonStr is {type(jsonStr)}, expected str or dict")
        return cls.fromDict(dic)

    @classmethod
    def fromDCCXMLJSON(cls, jsonData: str) -> dccQuantity:
        if isinstance(jsonData, str):
            mvDict = json.loads(jsonData)
        if isinstance(jsonData, dict):
            mvDict = jsonData
        try:
            listContent = mvDict["dcc:list"]
        except KeyError:
            listContent=mvDict

        def getIDXnumFromTableRefType(input_string):
            match = re.search(r"basic_(\d+)IndexTable", input_string)
            if match:
                return int(match.group(1))
            else:
                raise ValueError(
                    input_string + " is not an correct basic_NIndexTable refType"
                )

        numIDX = False
        refTypes=listContent["@refType"].split(" ")
        for refType in refTypes:
            try:
                numIDX = getIDXnumFromTableRefType(refType)
            except ValueError:
                pass
        if numIDX == False:
            raise ValueError("basic_NIndexTable refType Missing")
        dsiVectors = []
        for dsiVecDict in listContent["dcc:quantity"]:
            dsiVectors.append(dccQuantity.fromDCCXMLJSON(dsiVecDict))
        # find the index vectors
        IDXVectors = []
        for i in range(numIDX):
            tableIDXRefType = "basic_TableIndex" + str(i)
            vecFound = False
            for idx, vec in enumerate(dsiVectors):
                if not vec.refTypes is None:
                    if not vecFound:
                        if tableIDXRefType in vec.refTypes:
                            IDXVectors.append(dsiVectors.pop(idx))
                            vecFound = True
                    else:
                        if tableIDXRefType in vec.refTypes:
                            raise RuntimeError(
                                "More than one Quantity hast refType "
                                + str(tableIDXRefType)
                                + " this is ambiguous! Stopped parsing"
                            )
            if not vecFound:
                raise RuntimeError(
                    "No Quantity with refType "
                    + str(tableIDXRefType)
                    + " found! Stopped parsing"
                )
        try:
            rawNames=listContent['dcc:name']['dcc:content']
            tabMultiLangNames=parseDCCContent(rawNames)
        except KeyError:
            tabMultiLangNames=None
        try:
            rawDscp=listContent['dcc:description']['dcc:content']
            tabMultiLangDscp=parseDCCContent(rawDscp)
        except KeyError:  
            tabMultiLangDscp=None
        multiVec = dccQuantityTable(IDXVectors, dsiVectors, multiLangNames=tabMultiLangNames, multiLangDscp=tabMultiLangDscp, refTypes=refTypes)
        return multiVec

    def toDCCquantityList(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        resultList = []
        for index in self.index:
            resultList.append(index.toDCCXMLQuantityStr()["dcc:quantity"])
        for valueQuant in self.valueQuantites:
            resultList.append(valueQuant.toDCCXMLQuantityStr()["dcc:quantity"])
        return {
            "dcc:list": {
                "dcc:quantity": resultList,
                "@refType": ' '.join(list(self.refTypes)+[self.tablerefType]),
                #"@_Comment": "",
            }
        }

    def toXML(self):
        json = self.toDCCquantityList()
        XML = createXML(json)
        return XML

    def jsonDumps(self) -> str:
        """dumps to JSON

        Returns:
            str: JSON Str
        """
        return json.dumps(self.__dict__, cls=dsiJSONEncoder)

    def toDict(self) -> dict:
        return self.__dict__

    def dump_xlsx(self,fileName=None,sheetName='Sheet1'):
        if fileName==None:
            fileName = io.BytesIO()
        metaDF,dataDF=self.dump_pdDataFrames()
        combinedDF=pd.concat([metaDF,dataDF])
        if isinstance(fileName, io.BytesIO):
            if fileName.getbuffer().nbytes <128:
                with pd.ExcelWriter(fileName) as excel_writer:
                    combinedDF.to_excel(excel_writer, sheet_name=sheetName, header=False)
            else:
                with pd.ExcelWriter(fileName,mode='r+') as excel_writer:
                    combinedDF.to_excel(excel_writer, sheet_name=sheetName, header=False)
        else:
            try:
                with pd.ExcelWriter(fileName,mode='r+') as excel_writer:
                    combinedDF.to_excel(excel_writer, sheet_name=sheetName, header=False)
            except FileNotFoundError:
                with pd.ExcelWriter(fileName) as excel_writer:
                    combinedDF.to_excel(excel_writer, sheet_name=sheetName, header=False)
        return fileName

    def dump_ods(self,fileName=None,sheetName='Sheet1'):
        if fileName==None:
            fileName = io.BytesIO()
        metaDF,dataDF=self.dump_pdDataFrames()
        combinedDF=pd.concat([metaDF,dataDF])
        if isinstance(fileName, io.BytesIO):
            if fileName.getbuffer().nbytes <128:
                with pd.ExcelWriter(fileName, engine='odf') as excel_writer:
                    combinedDF.to_excel(excel_writer, sheet_name=sheetName, header=False)
            else:
                with pd.ExcelWriter(fileName, engine='odf',mode='r+') as excel_writer:
                    combinedDF.to_excel(excel_writer, sheet_name=sheetName, header=False)
        else:
            try:
                with pd.ExcelWriter(fileName, engine='odf',mode='r+') as excel_writer:
                    combinedDF.to_excel(excel_writer, sheet_name=sheetName, header=False)
            except FileNotFoundError:
                with pd.ExcelWriter(fileName, engine='odf') as excel_writer:
                    combinedDF.to_excel(excel_writer, sheet_name=sheetName, header=False)
        return fileName

    def dump_csv(self):
        metaDF,dataDF=self.dump_pdDataFrames()
        header=metaDF.to_csv(decimal='.',sep=';', index=True, header = False)
        data=dataDF.to_csv(decimal='.',sep=';', index=True, header = False)
        return header+data

    def dump_pdDataFrames(self):
        metaData = []
        data = []
        for index in self.index:
            metaData.append(index.getPDMetaData())
            data.append(index.getPDData())
        for valueVectorQuant in self.valueQuantityNames:
            metaData.append(self[valueVectorQuant].getPDMetaData())
            data.append(self[valueVectorQuant].getPDData())
        return pd.concat(metaData, axis=1, ignore_index=True),pd.concat(data, axis=0, ignore_index=True).transpose()

    def getAllUnits(self):
        allunits=[]
        for idxQuant in self.index:
            unitStr=idxQuant['unit']
            allunits.append(unitStr)
        for valueQuant in self.valueQuantites:
            unitStr = valueQuant['unit']
            allunits.append(unitStr)
        return list(set(allunits))

    def doesContainColWithUnit(self,unit):
        allUnits=self.getAllUnits()
        #TODO change to D-SI comarsion of scaled EQ units
        if unit in allUnits:
            return True
        else:
            return False

    def getColsWithUnit(self,unit):
        colNames = {}
        colNames['index'] = []
        colNames['valueVectors'] = []
        if unit is not '':
            if self.doesContainColWithUnit(unit):
                for dsiVec in self.index:

                    unitStr=dsiVec['unit']
                    if unitStr==unit:
                        colNames['index'].append(dsiVec['quantity'])
                for valueQuant in self.valueQuantityNames:
                    unitStr = self[valueQuant]['unit']
                    if unitStr==unit:
                        colNames['valueVectors'].append(valueQuant)
        else:
            colNames['index'] = self.indexQuantityNames
            colNames['valueVectors'] = self.valueQuantityNames
        return colNames

    def getColsWithRefType(self,refType):
        colNames = {}
        colNames['index'] = []
        colNames['valueVectors'] = []
        if refType is not '':
            if self.doesContainColWithrefType(refType):
                for dsiVec in self.index:
                    refTypes=dsiVec.refTypes
                    if refType in refTypes:
                        colNames['index'].append(dsiVec['quantity'])
                for valueQuant in self.valueQuantityNames:
                    refTypes = self[valueQuant].refTypes
                    if refType in refTypes:
                        colNames['valueVectors'].append(valueQuant)
        else:
            colNames['index'] = self.indexQuantityNames
            colNames['valueVectors'] = self.valueQuantityNames
        return colNames

    def getMatchingColumns(self,unit=None,refType=None,logic='AND'):
        unitCols=self.getColsWithUnit(unit)
        rfTypeCols=self.getColsWithRefType(refType)
        matchingTableNames={}
        if logic=='AND':
            matchingTableNames['index']=list(set(unitCols['index']).intersection(rfTypeCols['index']))
            matchingTableNames['valueVectors']=list(set(unitCols['valueVectors']).intersection(rfTypeCols['valueVectors']))
        elif logic=='OR':
            matchingTableNames['index']=list(set(unitCols['index']).union(rfTypeCols['index']))
            matchingTableNames['valueVectors']=list(set(unitCols['valueVectors']).union(rfTypeCols['valueVectors']))
        return matchingTableNames

    def getAllrefTypes(self):
        allrefTypes=[]
        for dsiVec in self.index:
            refTypes=dsiVec.refTypes
            if refTypes is not None:
                allrefTypes=allrefTypes+refTypes
        for valueQuant in self.valueQuantityNames:
            refTypes = self[valueQuant].refTypes
            if refTypes is not None:
                allrefTypes=allrefTypes+refTypes
        allrefTypes=allrefTypes+self.refTypes
        return list(set(allrefTypes))
    
    def doesContainColWithrefType(self,refType):
        allrefTypes=self.getAllrefTypes()
        if refType in allrefTypes:
            return True
        else:
            return False
    
    def getOverlappingIDXKeys(self,extIdxVec,indexName=None,tolerance=np.finfo(float).eps):
        ownIDX=0
        if indexName is not None:
            ownIDX=self.indexQuantityNames.index(indexName)
        return find_overlapping_indices(self.index[ownIDX]['values'],extIdxVec['values'],tolerance)
    
    def __getitem__(self, item):
        """See pyDCCToolsExamplesNoteBook.ipynb for detailed indexing Examples"""
        if type(item) == str:
            if item != "index":
                try:
                    return self.valueQuantites[self.valueQuantityNames.index(item)]
                except ValueError as ve:
                    # TODO fix this for multi indexing
                    if item in self.indexQuantityNames:
                        return self.index[self.indexQuantityNames.index(item)]
                    else:
                        raise ve
            else:
                return self.index

        elif type(item) == tuple:
            if type(item[0]) == str:
                try:
                    return self.interpolators[item[0]](item[1])
                except KeyError as ke:
                    raise ke
        elif type(item) == np.ndarray:
            interpolIndexVec = self.index[0].interpolatedValuesTodccQuantity(
                item, np.zeros_like(item)
            )
            dsiValueList = []
            for valueVectorQuant in self.valueQuantityNames:
                dsiValueList.append(self.interpolators[valueVectorQuant](item))
            return dccQuantityTable(interpolIndexVec, dsiValueList)
        else:
            raise KeyError()

    def __repr__(self):
        rptStr = str(self.dataType) + " @ " + hex(id(self)) + " Index >"
        for i, index in enumerate(self.index):
            rptStr += str(i) + " " + str(index["quantity"])
        rptStr += (
            " Quantities>"
            + str(self.valueQuantityNames)
            + " Interpolation Typ>"
            + str(self.interpolationTypes)
        )
        return rptStr

    def __eq__(self, x):
        added, removed, modified, same = dict_compare(self.__dict__, x.__dict__)
        if added == set() and removed == set() and modified == {}:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.dump_csv())


class dccQuantityInterpolator:
    supportedInterpolators = {
        "scipy": [
            "linear",
            "nearest",
            "nearest-up",
            "zero",
            "slinear",
            "quadratic",
            "cubic",
            "previous",
            "next",
        ]
    }

    @staticmethod
    def generateSupportedInterpolatorsMessage() -> str:
        """generates Error Message for non implemented interpolator"""
        printableMsg = "Supported interpolator sources and Algorithms are:\n"
        for algoKey in dccQuantityInterpolator.supportedInterpolators.keys():
            printableMsg += (
                str(algoKey)
                + " -->"
                + str(dccQuantityInterpolator.supportedInterpolators[algoKey])
                + "\n"
            )
        return printableMsg

    def __init__(
        self, indexVector: dccQuantity, dataVector: dccQuantity, type: (str, str)
    ) -> dccQuantityInterpolator:
        """D-SI Vector interpolator

        Args:
            indexVector (dccQuantity): index Vector ("X")
            dataVector (dccQuantity): dataVector ("Y")
            type (str,str): interpolation source and type e.g. ("scipy","linear")
        Returns:
            dccQuantityInterpolator: _description_
        """
        self.dataType = self.__class__.__name__
        self.dccQunatitiesVersion = version("dccQuantities")
        self.indexQuantity = indexVector["quantity"]
        self.dataQuantity = dataVector["quantity"]
        self.indexVector = indexVector
        self.dataVector = dataVector
        if type[0] == "scipy":
            if type[1] in dccQuantityInterpolator.supportedInterpolators["scipy"]:
                self.interpolators = {
                    "values": sp.interpolate.interp1d(
                        indexVector["values"],
                        dataVector["values"],
                        kind=type[1],
                        copy="False",
                        bounds_error=True,
                    ),
                    "uncer": sp.interpolate.interp1d(
                        indexVector["values"],
                        dataVector["uncer"],
                        kind=type[1],
                        copy="False",
                        bounds_error=True,
                    ),
                }
                self.type = type
                self.interpolatorSoftware = "scipy"
                self.interPolatorSoftwareVersion = sp.__version__

            else:
                raise KeyError(
                    "Interpolator Kind >"
                    + str(type[1])
                    + " not supported by scipy, no interpolator created. Use one of "
                    + str(dccQuantityInterpolator.supportedInterpolators["scipy"])
                )
        else:
            raise KeyError(
                "Interpolator source "
                + str(type[0])
                + " not supported. Use one of the supported ones\n "
                + dccQuantityInterpolator.generateSupportedInterpolatorsMessage()
            )

    def toDict(self) -> dict:
        exclude_keys = ["interpolators", "dataVector", "indexVector"]
        return {
            k: self.__dict__[k]
            for k in set(list(self.__dict__.keys())) - set(exclude_keys)
        }
        

    def __repr__(self) -> str:
        return (
            str(self.dataType)
            + " @ "
            + hex(id(self))
            + " "
            + str(self.type)
            + " "
            + str(self.interpolatorSoftware)
            + " "
            + str(self.interPolatorSoftwareVersion)
            + " X> "
            + str(self.indexQuantity)
            + " Y>"
            + str(self.dataQuantity)
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self, args: np.array) -> dccQuantity:
        return self.dataVector.interpolatedValuesTodccQuantity(
            self.interpolators["values"](args), self.interpolators["uncer"](args)
        )

def getNDTablesFromDCC(dccDict):
    lists = find_paths_with_key(dccDict, "dcc:list")
    tables = []
    for path in lists:
        dccLists = getFromDict(dccDict, path)
        if not isinstance(dccLists, dict):
            for idx, dccList in enumerate(dccLists):
                if "@refType" in dccList.keys():
                    if isinstance(dccList["@refType"], str):
                        refTypeList = list(
                            dccList["@refType"].split(" ")
                        )  # is should be already splitted but who knows
                    else:
                        refTypeList = dccList["@refType"]
                    for refType in refTypeList:
                        match = re.search(r"basic_(\d+)IndexTable", refType)
                        if match:
                            appendedPath=path+[idx]
                            tables.append((appendedPath, int(match.group(1))))
        else:
            dccList = dccLists
            if "@refType" in dccList.keys():
                if isinstance(dccList["@refType"], str):
                    refTypeList = list(
                        dccList["@refType"].split(" ")
                    )  # is should be already splitted but who knows
                else:
                    refTypeList = dccList["@refType"]
                for refType in refTypeList:
                    match = re.search(r"basic_(\d+)IndexTable", refType)
                    if match:
                        tables.append((path, int(match.group(1))))
    return tables


def find_paths_with_key(data, search_key, current_path=None):
    if current_path is None:
        current_path = []

    paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            current_path.append(key)
    
            if key == search_key:
                paths.append(list(current_path))
    
            if isinstance(value, dict):
                paths.extend(find_paths_with_key(value, search_key, current_path))
                
            if isinstance(value, list):
                paths.extend(find_paths_with_key(value, search_key, current_path))
            current_path.pop()
    if isinstance(data, list):
        for key, value in enumerate(data):
            current_path.append(key)
    
            if key == search_key:
                paths.append(list(current_path))
    
            if isinstance(value, dict):
                paths.extend(find_paths_with_key(value, search_key, current_path))
    
            if isinstance(value, list):
                paths.extend(find_paths_with_key(value, search_key, current_path))
            current_path.pop()

    return paths


def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value

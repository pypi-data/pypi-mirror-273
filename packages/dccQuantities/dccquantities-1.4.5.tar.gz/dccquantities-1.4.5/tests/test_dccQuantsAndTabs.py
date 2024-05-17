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
import json
import os
import re
import pytest
import numpy as np
from dccQuantities import dccQuantity,dccQuantityTable,dsiJSONEncoder
from dsiUnits import dsiUnit
def remove_whitespacesFromXML(s):
    # Replace all whitespace chars except newline
    s = re.sub(r'[\t\r\f\v]+', '', s)
    # Remove all spaces around newlines
    s = re.sub(r' *\n *', '\n', s)
    # Remove empty lines
    s = re.sub(r'\n\n', '\n', s)
    # Remove all whitespaces and linebreaks at beginning and end of str
    s = s.strip()
    s = s.strip(r'\n')
    return s

def test_whitespaceRemoval():
    # Strings will be trimmed, but whitespaces in the middle of the string remain intact
    assert remove_whitespacesFromXML("   <test>   ") == "<test>"
    assert remove_whitespacesFromXML("<test>  <test>") == "<test>  <test>"

    # Strings around newlines will be trimmed
    assert remove_whitespacesFromXML("<test>  \n  <test>") == "<test>\n<test>"
    assert remove_whitespacesFromXML("<test>  \r\n  <test>") == "<test>\n<test>"

    # Double newlines and leading/trailing newlines will be removed
    assert remove_whitespacesFromXML("\n <test>\n\n<test>\n") == "<test>\n<test>"


def test_singelVector():
    testVector=dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent",
                           refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    assert testVector.length == 20
    assert len(testVector) == 20
    assert str(testVector['unit']) == r'\hertz'
    assert testVector[9] == (5 , 0.005)
    assert testVector[4] == (2.5, 0.0025)
    np.testing.assert_allclose(testVector['values'], (np.arange(20) + 1) * 0.5)
    assert testVector['quantity'] == 'Frequency'
    assert testVector['uncer_relPercent',5] == 0.1
    assert testVector['uncer_relPercent'][5] == 0.1
    assert testVector['uncer_rel',5] == 0.1/100
    assert testVector['uncer_rel'][5] == 0.1/100
    assert testVector['uncer'][5] == 0.1 / 100*testVector['values'][5]
    assert np.all(testVector['uncer'][5:10] == 0.1 / 100*testVector['values'][5:10])
    assert np.all(testVector['uncer',5:10] == 0.1 / 100 * testVector['values',5:10])
    np.testing.assert_allclose(testVector['values',10:12], np.array([5.5,6.0]))
    with pytest.raises(IndexError) as idxError:
        testVector['uncer_relPercent', 1000]
    assert str(idxError.value) == "index 1000 is out of bounds for axis 0 with size 20"
    assert testVector['refTypes'] == ["vib_Test"]

def test_singelVectorWithNanRefTypes():
    testVector=dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent",
                           refTypes=np.NAN, name={'EN': 'Frequency', 'DE': 'Frequenz'})
    assert testVector.length == 20
    assert len(testVector) == 20
    assert str(testVector['unit']) == r'\hertz'
    assert testVector[9] == (5 , 0.005)
    assert testVector[4] == (2.5, 0.0025)
    np.testing.assert_allclose(testVector['values'], (np.arange(20) + 1) * 0.5)
    assert testVector['quantity'] == 'Frequency'
    assert testVector['uncer_relPercent',5] == 0.1
    assert testVector['uncer_relPercent'][5] == 0.1
    assert testVector['uncer_rel',5] == 0.1/100
    assert testVector['uncer_rel'][5] == 0.1/100
    assert testVector['uncer'][5] == 0.1 / 100*testVector['values'][5]
    assert np.all(testVector['uncer'][5:10] == 0.1 / 100*testVector['values'][5:10])
    assert np.all(testVector['uncer',5:10] == 0.1 / 100 * testVector['values',5:10])
    np.testing.assert_allclose(testVector['values',10:12], np.array([5.5,6.0]))
    with pytest.raises(IndexError) as idxError:
        testVector['uncer_relPercent', 1000]
    assert str(idxError.value) == "index 1000 is out of bounds for axis 0 with size 20"
    assert testVector['refTypes'] == None

def test_multiVector():
    testDSiVectorFreq = dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent", refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    testDsiVectorMag = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    testDsiVectorPhase = dccQuantity((np.arange(20) + 1) * 0.1 * np.pi, np.ones(20) * 0.1, 'Phase', r'\radian', uncerType="relPercent")
    testMultVectorMultiIndex = dccQuantityTable([testDSiVectorFreq], [testDsiVectorMag, testDsiVectorPhase])
    assert testMultVectorMultiIndex['index'][0]['quantity'] == 'Frequency'
    assert testMultVectorMultiIndex['index'][0] == testDSiVectorFreq
    assert testMultVectorMultiIndex['index'][0][9] == (5 , 0.005)
    assert testMultVectorMultiIndex.indexQuantityNames == ['Frequency']
    assert testMultVectorMultiIndex.valueQuantityNames == ['Magnitude', 'Phase']
    assert testMultVectorMultiIndex['Magnitude'][15] == (80, 0.08)

def test_multiVectorinterpolation():
    testDSiVectorFreq = dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent", refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    testDsiVectorMag = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    testDsiVectorPhase = dccQuantity((np.arange(20) + 1) * 0.1 * np.pi, np.ones(20) * 0.1, 'Phase', r'\radian', uncerType="relPercent")
    testMultVector = dccQuantityTable([testDSiVectorFreq], [testDsiVectorMag, testDsiVectorPhase], interpolationTypes={'Magnitude':('scipy', 'linear'), 'Phase':('scipy', 'linear'), 'default':('scipy', 'linear')})
    with pytest.raises(ValueError) as vError:
        testMultVector['Magnitude',15.5]
    assert str(vError.value) == "A value (15.5) in x_new is above the interpolation range's maximum value (10.0)."
    interPolated = testMultVector['Magnitude', [7.5,6.66789, 8.5]]
    assert interPolated.isInterPolatedData
    np.testing.assert_allclose(interPolated['values'],np.array([75.0, 66.6789, 85.0]))
    np.testing.assert_allclose(interPolated['uncer'],np.array([0.05625, 0.04446076, 0.07225]))

def test_jsonDumpingSingleVector():
    testVector=dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent",
                           refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    jsonstr=testVector.jsonDumps()
    testVecotr2=dccQuantity.fromJson(jsonstr)
    isEqual =( testVector == testVecotr2)
    assert isEqual == True

def test_xmlDumpingSingleVectorRelPercent():
    testVector=dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent",
                           refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    xmlAsJSON=testVector.toDCCXMLQuantityStr()
    jsonSTR=json.dumps(xmlAsJSON, cls=dsiJSONEncoder)
    loadedVec=dccQuantity.fromDCCXMLJSON(jsonSTR)
    loadedVec.originalUncerType="relPercent"
    isEqual =(loadedVec == testVector)
    assert isEqual == True

def test_xmlDumpingSingleVectorAbs():
    testVector=dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="absolute",
                           refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    xmlAsJSON=testVector.toDCCXMLQuantityStr()
    jsonSTR=json.dumps(xmlAsJSON, cls=dsiJSONEncoder)
    loadedVec=dccQuantity.fromDCCXMLJSON(jsonSTR)
    assert loadedVec == testVector
    
def test_xmlDumpingSingleVectorNoUncer():
    testVector = dccQuantity((np.arange(20) + 1) * 0.5, None, 'Frequency', r'\hertz', name={'EN': 'Frequency', 'DE': 'Frequenz'})
    xmlAsJSON = testVector.toDCCXMLQuantityStr()
    jsonSTR = json.dumps(xmlAsJSON,cls=dsiJSONEncoder)
    loadedVec = dccQuantity.fromDCCXMLJSON(jsonSTR)
    assert loadedVec == testVector
    XML=loadedVec.toXML()
    with open("tests/test_xmlDumpingSingleQuantNoUncer.xml") as XMlFile:
        assert remove_whitespacesFromXML(XMlFile.read()) == remove_whitespacesFromXML(XML)

def test_multiVector_jsonDumping():
    testDSiVectorFreq = dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent", refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    testDsiVectorMag = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    testDsiVectorPhase = dccQuantity((np.arange(20) + 1) * 0.1 * np.pi, np.ones(20) * 0.1, 'Phase', r'\radian', uncerType="relPercent")
    testMultVector = dccQuantityTable([testDSiVectorFreq], [testDsiVectorMag, testDsiVectorPhase])
    json=testMultVector.jsonDumps()
    loadedMultiVector=dccQuantityTable.fromJson(json)
    assert testMultVector == loadedMultiVector

def test_multiVectorMultiIndex_jsonDumping():
    testDSiVectorFreq = dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent", refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    testDsiVectorMag = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    testDsiVectorPhase = dccQuantity((np.arange(20) + 1) * 0.1 * np.pi, np.ones(20) * 0.1, 'Phase', r'\radian', uncerType="relPercent")
    testDSiVectorEXAmp = dccQuantity((np.arange(20) + 1) * 20, np.ones(20) * 0.1, 'Frequency', r'\volt',
                                     uncerType="relPercent", refTypes=["vib_Test"],
                                     name={'EN': 'Anregungs Amplitude', 'DE': 'Excitation Amplitude'})
    testMultVector = dccQuantityTable([testDSiVectorFreq, testDSiVectorEXAmp], [testDsiVectorMag, testDsiVectorPhase])
    json=testMultVector.jsonDumps()
    loadedMultiVector=dccQuantityTable.fromJson(json)
    assert testMultVector == loadedMultiVector

def test_multiVectorJSONDumpingAndLoading():
    testDSiVectorFreq = dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent", refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    testDsiVectorMag = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    testDsiVectorPhase = dccQuantity((np.arange(20) + 1) * 0.1 * 3, np.ones(20) * 0.1, 'Phase', r'\radian', uncerType="relPercent", name={'EN': 'Phase', 'DE': 'Phase'})
    testMultVector = dccQuantityTable([testDSiVectorFreq], [testDsiVectorMag, testDsiVectorPhase])
    jsonSTR=testMultVector.jsonDumps()
    loadedMultiVec=dccQuantityTable.fromJson(jsonSTR)
    assert loadedMultiVec==testMultVector

def test_multiVectorJSONDumpingAndLoadingFromFile():
    testDSiVectorFreq = dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent", refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    testDsiVectorMag = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    testDsiVectorPhase = dccQuantity((np.arange(20) + 1) * 0.1 * 3, np.ones(20) * 0.1, 'Phase', r'\radian', uncerType="relPercent", name={'EN': 'Phase', 'DE': 'Phase'})
    testMultVector = dccQuantityTable([testDSiVectorFreq], [testDsiVectorMag, testDsiVectorPhase])
    jsonDict=testMultVector.toDCCquantityList()
    with open("tests/test_dccQuantTabJSONDumpingAndLoadingFromFile.json",encoding='utf-8') as JSONFile:
        fileContent=JSONFile.read()
        #print(fileContent)
        loadedMultiVec=dccQuantityTable.fromJson(fileContent)
    isEqual = (loadedMultiVec == testMultVector)
    assert isEqual==True

def test_multiVectorToXML():
    testDSiVectorFreq = dccQuantity((np.arange(20) + 1) * 0.5, np.ones(20) * 0.1, 'Frequency', r'\hertz', uncerType="relPercent", refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    testDsiVectorMag = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    testDsiVectorPhase = dccQuantity((np.arange(20) + 1) * 0.1 * 3, np.ones(20) * 0.1, 'Phase', r'\radian', uncerType="relPercent", name={'EN': 'Phase', 'DE': 'Phase'})
    testMultVector = dccQuantityTable([testDSiVectorFreq], [testDsiVectorMag, testDsiVectorPhase])
    createdXML = testMultVector.toXML()
    with open("tests/test_dccQuantTabXMLDumping.xml") as XMlFile:
        assert remove_whitespacesFromXML(XMlFile.read()) == remove_whitespacesFromXML(createdXML)

def test_tableDumping():
    testDSiVectorFreq = dccQuantity((np.arange(20) + 1) * 0.5, None, 'Frequency', r'\hertz', refTypes=["vib_Test"], name={'EN': 'Frequency', 'DE': 'Frequenz'})
    testDsiVectorMag = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    testDsiVectorPhase = dccQuantity((np.arange(20) + 1) * 0.1 * 3, np.ones(20) * 0.1, 'Phase', r'\radian', uncerType="relPercent", name={'EN': 'Phase', 'DE': 'Phase'})
    testMultVector = dccQuantityTable([testDSiVectorFreq], [testDsiVectorMag, testDsiVectorPhase])
    csvStr=testMultVector.dump_csv()
    with open("tests/test_tableDumping.csv",'r',encoding='utf-8') as csvFile:
        assert csvStr == csvFile.read()
    try:
        os.remove("output.xlsx")
        os.remove("output.ods")
    except:
        pass
    testMultVector.dump_xlsx("output.xlsx")
    testMultVector.dump_xlsx("output.xlsx",sheetName="Test")
    xlsxFileObj = testMultVector.dump_xlsx()
    testMultVector.dump_ods("output.ods")
    testMultVector.dump_ods(fileName="output.ods",sheetName="Test")
    odsFileObj = testMultVector.dump_ods()
    odsFileObj = testMultVector.dump_ods(fileName=odsFileObj,sheetName="Test")
    try:
        os.remove("output.xlsx")
        os.remove("output.ods")
    except:
        pass
    print("DONE")

#################################
#### Tesing Math operations #####

def test_addition():
    testDsiVectorMag1 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    testDsiVectorMag2 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt',
                                    uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    additionResult=testDsiVectorMag1+testDsiVectorMag2
    assert additionResult['values'][5] == 60

def test_substraction():
    testDsiVectorMag1 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    testDsiVectorMag2 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt',
                                    uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    additionResult=testDsiVectorMag1-testDsiVectorMag2
    assert additionResult['values'][5] == 0

def test_substractionWScalar():
    testDsiVectorMag1 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    testDsiScalar = dccQuantity(np.array([5]), np.array(0.1), 'Magnitude', r'\volt',
                                uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    additionResult=testDsiVectorMag1-testDsiScalar
    assert additionResult['values'][5] == 25


def test_division():
    testDsiVectorDistance = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Distance', r'\metre', uncerType="relPercent", name={'EN': 'Distance', 'DE': 'Entfernung'})
    testDsiVectorTime = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.001, 'Time', r'\second',
                                    uncerType="relPercent", name={'EN': 'Time', 'DE': 'Zeit'})
    additionResult=testDsiVectorDistance/testDsiVectorTime
    assert additionResult['values'][5] == 1.0

def test_multiplication():
    testDsiVectorDistance = dccQuantity((np.arange(20) + 1) * 5,
                                        np.ones(20) * 0.1,
                                      'Distance',
                                      r'\metre',
                                        uncerType="relPercent",
                                        name={'EN':'Distance','DE':'Entfernung'})

    testDsiVectorTime = dccQuantity((np.arange(20) + 1) * 5,
                                    np.ones(20) * 0.001,
                                  'Time',
                                  r'\second',
                                    uncerType="relPercent",
                                    name={'EN': 'Time', 'DE': 'Zeit'})

    additionResult=testDsiVectorDistance*testDsiVectorTime
    assert additionResult['values'][5] == 900.0

def test_multiplicationWScalar():
    testDsiVectorDistance = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Distance', r'\metre',
                                        uncerType="relPercent", name={'EN': 'Distance', 'DE': 'Entfernung'})
    testDsiVectorTime = dccQuantity(5.0, 0.001, 'Time', r'\second',
                                    uncerType="relPercent", name={'EN': 'Time', 'DE': 'Zeit'})
    additionResult = testDsiVectorDistance * testDsiVectorTime
    assert additionResult['values'][5] == 150.0

def test_additionWithSiPrfix():
    testDsiVectorMag1 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    testDsiVectorMag2 = dccQuantity(1.0, 0.1, 'Magnitude Offset', r'\milli\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    additionResult=testDsiVectorMag1+testDsiVectorMag2
    assert additionResult['values'][5] == 30.001

def test_additionWithSiPrfix2():
    testDsiVectorMag1 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    testDsiVectorMag2 = dccQuantity(1.0, 0.1, 'Magnitude Offset', r'\kilo\volt',
                                    uncerType="relPercent", name={'EN': 'Magnitude', 'DE': 'Magnitude'})
    additionResult=testDsiVectorMag1+testDsiVectorMag2
    assert additionResult['values'][5] == 1030.0

def test_toUnitConversion():
    testCountsPerSecond = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Counts per Second', r'\second\tothe{-1}', uncerType="relPercent", name={'EN': 'Counts per Second', 'DE': 'Zählungen pro Sekunde'})
    testCountsPerSecond.convertToUnit(r'\hertz')
    assert testCountsPerSecond['unit'] == dsiUnit(r'\hertz')
    assert testCountsPerSecond['values'][3] == 20
    assert testCountsPerSecond['uncer'][3] == 0.02
    testCountsPerSecond.convertToUnit(r'\kilo\hertz')
    assert testCountsPerSecond['unit'] == dsiUnit(r'\kilo\hertz')
    assert testCountsPerSecond['values'][3] == 20/1000
    assert testCountsPerSecond['uncer'][3] == 0.02/1000
    testCountsPerSecond.convertToUnit(r'\becquerel')
    assert testCountsPerSecond['unit'] == dsiUnit(r'\becquerel')
    assert testCountsPerSecond['values'][3] == 20
    assert testCountsPerSecond['uncer'][3] == 0.02
    testCountsPerSecond.convertToUnit(r'\kilo\becquerel')
    assert testCountsPerSecond['unit'] == dsiUnit(r'\kilo\becquerel')
    assert testCountsPerSecond['values'][3] == 0.020
    assert testCountsPerSecond['uncer'][3] == 0.00002
'''
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.1
    @description: Used to append content from a feature service
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014
'''
import gc
import os
import sys
import arcpy

from arcpyhelper import ArcRestHelper
from arcpyhelper import Common

def outputPrinter(message,typeOfMessage='message'):
    if typeOfMessage == "error":
        arcpy.AddError(message=message)
    elif typeOfMessage == "warning":
        arcpy.AddWarning(message=message)
    else:
        arcpy.AddMessage(message=message)

    print(message)
def main(*argv):
    userName = None
    password = None
    org_url = None
    fsId = None
    layerName = None
    dataToAppend = None
    arh = None
    fs = None
    results = None
    fl = None
    existingDef= None
    try:

##        userName = argv[0]
##        password = argv[1]
##        org_url = argv[2]
##        fsId = argv[3]
##        layerName = argv[4]
##        dataToAppend = argv[5]
##        toggleEditCapabilities = argv[6]

        userName = "MikeSolutions"
        password = 'double1pa'
        org_url = 'www.arcgis.com'
        fsId = 'db2decf77abd4386976e33a8e5b5279a'
        layerName ='Logger Area'
        dataToAppend = r'C:\temp\test.shp'
        toggleEditCapabilities = 'False'

        if arcpy.Exists(dataset=dataToAppend) == False:
            outputPrinter(message="Data layer not found: %" % dataToAppend)
        else:
            arh = ArcRestHelper.featureservicetools(username = userName, password=password,org_url=org_url,
                                                       token_url=None,
                                                       proxy_url=None,
                                                       proxy_port=None)
            if not arh is None:
                outputPrinter(message="Security handler created")

                fs = arh.GetFeatureService(itemId=fsId,returnURLOnly=False)

                if arh.valid:
                    outputPrinter("Logged in successful")
                    if not fs is None:
                        if toggleEditCapabilities == 'True':
                            existingDef = arh.EnableEditingOnService(url=fs.url)
                        fl = arh.GetLayerFromFeatureService(fs=fs,layerName=layerName,returnURLOnly=False)
                        if not fl is None:
                            results = fl.addFeatures(fc=dataToAppend)

                            if 'error' in results:
                                outputPrinter(message="Error in response from server: " % results['error'],typeOfMessage='error')
                                arcpy.SetParameterAsText(6, "false")

                            else:
                                outputPrinter (message="%s features added" % len(results['addResults']) )
                                if toggleEditCapabilities == 'True':
                                    existingDef = arh.EnableEditingOnService(url=fs.url,definition = existingDef)
                                arcpy.SetParameterAsText(6, "true")

                        else:
                            outputPrinter(message="Layer %s was not found, please check your credentials and layer name" % layerName,typeOfMessage='error')
                            arcpy.SetParameterAsText(6, "false")
                    else:
                        outputPrinter(message="Feature Service with id %s was not found" % fsId,typeOfMessage='error')
                        arcpy.SetParameterAsText(6, "false")
                else:
                    outputPrinter(arh.message,typeOfMessage='error')
                    arcpy.SetParameterAsText(6, "false")


            else:
                outputPrinter(message="Security handler not created, exiting")
                arcpy.SetParameterAsText(6, "false")


    except arcpy.ExecuteError:
        line, filename, synerror = Common.trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        outputPrinter(message="ArcPy Error Message: %s" % arcpy.GetMessages(2),typeOfMessage='error')
        arcpy.SetParameterAsText(6, "false")
    except (Common.CommonError,ArcRestHelper.ArcRestHelperError),e:
        outputPrinter(message=e,typeOfMessage='error')
        arcpy.SetParameterAsText(6, "false")
    except:
        line, filename, synerror = Common.trace()
        outputPrinter(message="error on line: %s" % line,typeOfMessage='error')
        outputPrinter(message="error in file name: %s" % filename,typeOfMessage='error')
        outputPrinter(message="with error message: %s" % synerror,typeOfMessage='error')
        arcpy.SetParameterAsText(6, "false")
    finally:
        existingDef = None
        userName = None
        password = None
        org_url = None
        fsId = None
        layerName = None
        dataToAppend = None
        arh = None
        fs = None
        results = None
        fl = None

        del existingDef
        del userName
        del password
        del org_url
        del fsId
        del layerName
        del dataToAppend
        del arh
        del fs
        del results
        del fl

        gc.collect()
if __name__ == "__main__":
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in xrange(arcpy.GetArgumentCount()))
    main(*argv)




























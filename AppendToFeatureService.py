"""
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.0.0
    @description: Used to stage the app in your organization.
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014
"""

import sys, os, datetime
from arcpy import env
from arcpyhelper import ArcRestHelper
from arcpyhelper import Common

log_file='./logs/AppendToFeatureService.log'
dateTimeFormat = '%Y-%m-%d %H:%M'
globalLoginInfo = 'C:/Work/ArcGIS for Utilities/_Water/Staging/A4W-SubDMAProcessor-v1/Application/configs/GlobalLoginInfo.json'

if __name__ == "__main__":
    env.overwriteOutput = True

    log = Common.init_log(log_file=log_file)

    try:

        if log is None:
            print "Log file could not be created"

        print "********************Script Started********************"
        print datetime.datetime.now().strftime(dateTimeFormat)
        cred_info = None
        if os.path.isfile(globalLoginInfo):
            loginInfo = Common.init_config_json(config_file=globalLoginInfo)
            if 'Credentials' in loginInfo:
                cred_info = loginInfo['Credentials']
        print "    Logging in"
        
        arh = ArcRestHelper.featureservicetools(username = cred_info['Username'], password=cred_info['Password'],org_url=cred_info['Orgurl'],
                                           token_url=None, 
                                           proxy_url=None, 
                                           proxy_port=None)
        
        if arh is None:
            print "    Log in not successful"
            
        print "    Logged in successfully"
        
        fs = arh.GetFeatureService(itemId='c9342bc237a54a3db0fc21aa089c4fb5',returnURLOnly=False)
        if not fs is None:                
            fl = arh.GetLayerFromFeatureService(fs=fs,layerName='DMA Sensors',returnURLOnly=False)
            if not fl is None:
                results = fl.addFeatures(fc=r'C:\Work\ArcGIS for Utilities\_Water\Staging\A4W-SubDMAProcessor-v1\Maps and GDBs\DMA.gdb\DMASensors')        
                print results
        
        
    except(TypeError,ValueError,AttributeError),e:
        print e
              
    finally:
        print datetime.datetime.now().strftime(dateTimeFormat)
        print "###############Script Completed#################"
        print ""
        if log is not None:
            log.close()
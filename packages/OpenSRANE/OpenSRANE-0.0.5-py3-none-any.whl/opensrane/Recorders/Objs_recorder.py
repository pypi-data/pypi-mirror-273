# /* ****************************************************************** **
# **   OpenSRANE - Open Software for Risk Assessment of Natech Events   **
# **                                                                    **
# **                                                                    **
# **                                                                    **
# ** (C) Copyright 2023, Mentioned Regents in 'COPYRIGHT' file.         **
# **                                                                    **
# ** All Rights Reserved.                                               **
# **                                                                    **
# ** Commercial use of this program without express permission of the   **
# ** owner (The Regents), is                                            **
# ** strictly prohibited.  See file 'COPYRIGHT'  in main directory      **
# ** for information on usage and redistribution,  and for a            **
# ** DISCLAIMER OF ALL WARRANTIES.                                      **
# **                                                                    **
# ** Developed by:                                                      **
# **   Bijan SayyafZadeh (OpenSRANE@Gmail.com)                          **
# **   MehDi Sharifi                                                    **
# **   Abdolreza S. Moghadam                                            **
# **   Eslam Kashi                                                      **
# **                                                                    **
# ** ****************************************************************** */

'''
 Written: Bijan Sayyafzadeh
 Created: 2022
 
 Revision: -
 By & Date: -
'''


from opensrane.Misc._NewClass import _NewClass
from .ObjManager import *
import opensrane as _opr
import os as _os
import datetime as _dt
import _pickle as _pickle
from copy import deepcopy as _deepcopy
import gc as _gc


class Objs_recorder(_NewClass):
    '''
    
    This Object id for recording all of the objects in each scenario analysis
    tag= tag of the recorder
    filename: name of the file that data will be record in it
    SaveStep: It was the Number of the steps of analysis that after that, data will be record on a file but it removed from objects and it is sent to analyze part. It is set to None because for preventing any error of using old created models.
    fileAppend: Does data append to a existing file or it reset existing data in the file name
    RecodingSubpackages: List of subpackages that Users wanna to be record by recorders. The default value is ['PlantUnits','Hazard', 'DateAndTime', 'WindData'] but others also can be added by user except 'Recorders'. The Other subpackages will be record once at the first savefile. 
    MergeSavedFiles: If set this option into True, When analysis finished all files will be merge into one file and for huge files it take so much memory and time!
    
    '''
    
    def __init__(self,tag,filename='',fileAppend=True, RecodingSubpackages=['PlantUnits', 'Hazard', 'DateAndTime', 'WindData', 'NodesGroups'], MergeSavedFiles=False, SaveStep=None):
         
        #---- Fix Part for each class __init__ ----
        ObjManager.Add(tag,self)
        _NewClass.__init__(self,tag)
        #------------------------------------------
        
        self.filename=filename
        self.fileAppend=fileAppend
        
        if fileAppend==False:
            self._ResetRecorder()
        
        self.RecordedList=[] #List that store all recorded objects inside in each happend scenario as a dictionary and send it to pickle to save in file
        
        self.RecordCounter=0
        
        #Set does the code merge all created files together or not
        self.MergeSavedFiles=MergeSavedFiles
        
        #If file append be True then code should find the number of maximum existing saved file and create new files with number greater than the founded number
        self.MaxExistSavedfileIndex=0
        if fileAppend==True:
            
            for file in _os.listdir():
                if file[-3:]=='OPR' and file[:len(filename)]==filename and len(file)>=len(filename+'.OPR'):
                    num=file[len(filename):-4]
                    if num!='' and num.isnumeric()==True:
                        if int(num)>self.MaxExistSavedfileIndex: self.MaxExistSavedfileIndex=int(num)



        #List of Subpacakges that shouldn't be saved or saving them doesn't have any meaning. These subpackages have no object to be defined and saved and are just some commands
        self.SubsNotNeededToSave=['Recorders','All','Misc','Plot','PostProcess','_New_module']
        
        #List of SubPackages that should be save
        RecodingSubpackages=[ i for i in RecodingSubpackages if i not in self.SubsNotNeededToSave] #Remove subpackages that there is no need to save them if user defined them in RecodingSubpackages
        self.RecodingSubpackages=RecodingSubpackages 
        
        
    def Record(self):
        '''
        This function records all the objects and save them all in the entered filename
        '''

        self.RecordCounter +=1

        #If there is any damage then the data will be recorded
        if _opr.Analyze.ScenarioAnalyze.anydamage==True:
            

            CurrentScenarioDict={}
            #Get SubPackage all Objects
            CurrentScenarioDict={SubPackname:SubPackobj.ObjManager.Objlst for SubPackname,SubPackobj in _opr.Misc.GetModules() if SubPackname in self.RecodingSubpackages}
                        
            #Add all current object to Objects that are in memory
            self.RecordedList.append(_deepcopy(CurrentScenarioDict))

           
        return 0

    def SaveToFile(self,fileindex):
        
        #fileindex are from 0 to number of files. If user wanna to append the existing files then the maximum index number of existing files should be added to input fileindex
        fileindex=fileindex+self.MaxExistSavedfileIndex

        
        #Create log file to record number of the analysis
        with open(self.filename+str(fileindex)+'.Log', "w") as f:
            f.write(f'Number of Analysis: {self.RecordCounter}\nNumber of Scenarios in this log: {len(self.RecordedList)}')
        
        #Set the file name
        filename=self.filename+str(fileindex)+'.OPR'
        
        # Write data to the file    
        with open(filename, 'wb') as fileObj:
            _pickle.dump(self.RecordedList,fileObj,protocol=-1)
        
        
        #Clear memory
        self.RecordedList=[]
        #Set RecordCounter to zero
        self.RecordCounter=0

        
    def OtherSaveOnce(self):

        '''
        Method for saving subpackages that are not defined by user for saving in each analysis or simulation and using this method are saved just once
        '''
        SavedandNotSavedSUBS= self.RecodingSubpackages + self.SubsNotNeededToSave
        
        OtherSubPackagesDict={SubPackname:SubPackobj.ObjManager.Objlst for SubPackname,SubPackobj in _opr.Misc.GetModules() if SubPackname not in SavedandNotSavedSUBS}
        
        #Create log file to record number of the analysis
        with open(self.filename+'.Log', "w") as f:
            f.write(f'Number of Analysis: {0}\nNumber of Scenarios in this log: {0}')
        
        #Set the file name
        filename=self.filename+'.OPR'
        
        # Write data to the file    
        with open(filename, 'wb') as fileObj:
            _pickle.dump(OtherSubPackagesDict,fileObj,protocol=-1)
                

    def _MergeAndClear(self):
        
        #At the end of analysis _MergeAndClear method for any object will be called and for each object 
        if self.MergeSavedFiles==True:
        
            filename=self.filename
            
            #Set files equal the files that their name is similar with
            files=_os.listdir()            
            Recfiles=[file for file in files if (file.startswith(filename) and file.endswith('OPR') and len(file)>len(filename+'.OPR'))]
            
            #Merge OPR Files------------------------------------------------------------------------------------
            AllScenarioList=[]
            
            for file in Recfiles:
                    
                # Read file
                with open(file, 'rb') as fileObj:
                    loaddict=_pickle.load(fileObj)
                    AllScenarioList =AllScenarioList +  loaddict if type(loaddict)==list else AllScenarioList
                #Remove file
                _os.remove(file)

            #Main file
            file=filename+'M.OPR' #M suffix stands for showing this is the merged files
            
            #Write to file
            with open(file, 'wb') as fileObj:
                _pickle.dump(AllScenarioList,fileObj,protocol=-1)

            
            #Merge Log files-------------------------------------------------------------------------------------
            AnalyzeNumber=0
            ScenarioNumber=0
            
            Recfiles=[file for file in files if (file.startswith(filename) and file.endswith('Log') and len(file)>len(filename+'.Log'))]
            for file in Recfiles:
                    
                # Read file
                with open(file, 'r') as fileObj:
                    number=fileObj.read()
                    number=number.split()[3],number.split()[-1]
                    AnalyzeNumber, ScenarioNumber =AnalyzeNumber +  int(number[0]), ScenarioNumber +  int(number[1])
                #Remove file
                _os.remove(file)        

            #Main file
            file=filename+'M.Log' #M suffix stands for showing this is the merged files
                    
            #Write to file
            with open(file, 'w') as fileObj:
                fileObj.write(f'Number of Analysis: {AnalyzeNumber}\nNumber of Scenarios in this log: {ScenarioNumber}')


    def _ResetRecorder(self):
        '''
        This function clear the created filename that records the objects
        '''
        #Remove all OPR files
        for file in _os.listdir():
            if file[-3:]=='OPR' and file[:len(self.filename)]==self.filename:
                _os.remove(file)

        #Remove all log files
        for file in _os.listdir():
            if file[-3:]=='Log' and file[:len(self.filename)]==self.filename:
                _os.remove(file)        
            

class Objs_recorder_loader():
    
    
    _ScenarioBank={}
    _ScenarioFile={}
    _LoadedFile=None
    
    @staticmethod
    def ReturnFileIndexScenariosDict(filename):
        '''
        This Function returns a dictionary with following structure
        {filename:{'Analysis Number Range':The range of the analysis number that has been done in this file, 
                   'Scenario Number Range':The range of recorded scenarios that exist in this file}}
        
        So, in this file we will see the Analysis that has been done for the file and also the recorded scenario range for each file.
        
        Scenarios are numbering here according to the name of their recorded or saved file and the order of them is not important and order of the files are determined by _os.listdir() command
        '''
        Results={}     

        
        AnalyzeNumber=0
        ScenarioNumber=0
        for file in _os.listdir():
            if file[-3:]=='Log' and file[:len(filename)]==filename and len(file)>len(filename+'.Log'):
            
                #Read logo file and update it
                with open(file, "r") as fileObj:

                    #Read file and export data
                    number=fileObj.read()
                
                number=number.split()[3],number.split()[-1]
                Results=Results | {file[:-4]:{'Analysis Number Range':(AnalyzeNumber+1  , AnalyzeNumber  +  int(number[0])), 
                                         'Scenario Number Range':(ScenarioNumber+1 , ScenarioNumber +  int(number[1]))}}
                               
                AnalyzeNumber, ScenarioNumber = AnalyzeNumber +  int(number[0]), ScenarioNumber +  int(number[1])
        
        
        if Results=={}:
            print(f'{filename} not found!')
            return -1  
            
        return Results


    @staticmethod
    def TotalNumberOfScenarios(filename):
        '''
        This static method or function returns the maximum number of recorded or created scenarios number (Total number of scenarios)
        '''
        #get dictionary of the files and the number od analysis and scenarios boundary for each file
        FilesAnaScenNumbers=Objs_recorder_loader.ReturnFileIndexScenariosDict(filename)
        
        return max([max(file['Scenario Number Range']) for file in FilesAnaScenNumbers.values()])

    @staticmethod
    def TotalNumberOfAnalysis(filename):
        '''
        This static method or function returns the maximum number of Analysis or simulations (Total number of Analysis)
        '''
        #get dictionary of the files and the number od analysis and scenarios boundary for each file
        FilesAnaScenNumbers=Objs_recorder_loader.ReturnFileIndexScenariosDict(filename)
        
        return max([max(file['Analysis Number Range']) for file in FilesAnaScenNumbers.values()])

    @staticmethod
    def load1RecordedScenario(ScenarioNumber, filename):
        '''
        This function returns all recorded objects of Scenario with number of ScenarioNumber to the memory
        if no recorded data will be available in the current recording object or in the filename, 
        it retunes empty
        
        This function is proper for just one call and not proper for multiple calls
        
        '''
        #Check if the ScenarioNumber was less than 1 then comment
        if ScenarioNumber<1:
            print('Scenarios number start from 1!')
            return -1
        
        #Before any load all objects should be delete
        _opr.wipe()
        
        #get dictionary of the files and the number od analysis and scenarios boundary for each file
        FilesAnaScenNumbers=Objs_recorder_loader.ReturnFileIndexScenariosDict(filename)
        
        #Check if file exist
        if FilesAnaScenNumbers==-1:
            return -1
            
        #Get the maximum created scenario number
        MaxCreatedScenNum=Objs_recorder_loader.TotalNumberOfScenarios(filename)
            
        scenarioDict={}
        
        
        #check if ScenarioNumber is not greater than the recorded scenarios
        if MaxCreatedScenNum<ScenarioNumber:
            print(f"Entered Scenario Tag ({ScenarioNumber}) is greater than maximum recorded scenario so so nothing loaded")
            return -1
            
        
        for filename,fileresult in FilesAnaScenNumbers.items():
            
            if ScenarioNumber>fileresult['Scenario Number Range'][1]:continue
            
            FileScenarioRange=FilesAnaScenNumbers[filename]['Scenario Number Range']
            ScenarioNumber=ScenarioNumber-FileScenarioRange[0]
            
            # Read file and load scenario
            with open(filename+".OPR", 'rb') as fileObj:

                loadlist=_pickle.load(fileObj)

                if type(loadlist)==list:
                    scenarioDict= loadlist[ScenarioNumber]
            break
        

        if scenarioDict=={}:
            print(f'No Scenario was recorded in {filename} file')
            return -1
        
        #feed the loaded scenario to subpackages
        for SubPackname,SubPackobj in _opr.Misc.GetModules():
            
            if SubPackname!='Recorders' and SubPackname in scenarioDict.keys():
                #replace each subpackage Objlst, Taglst, TagObjDict with what are available in the recorded scenario
                SubPackobj.ObjManager.Objlst=scenarioDict[SubPackname] if scenarioDict!={} else []
                SubPackobj.ObjManager.Taglst=[obj.tag for obj in SubPackobj.ObjManager.Objlst]
                SubPackobj.ObjManager.TagObjDict={obj.tag:obj for obj in SubPackobj.ObjManager.Objlst}
        
        #Finally the OtherSubpackagesSavedOnce should be loaded
        # Read file and load scenario
        with open(filename+".OPR", 'rb') as fileObj:

            loadlist=_pickle.load(fileObj)

            if type(loadlist)==list:
                scenarioDict= loadlist[ScenarioNumber]
                
        #feed the loaded scenario to subpackages
        for SubPackname,SubPackobj in _opr.Misc.GetModules():
            
            if SubPackname!='Recorders' and SubPackname in scenarioDict.keys():
                #replace each subpackage Objlst, Taglst, TagObjDict with what are available in the recorded scenario
                SubPackobj.ObjManager.Objlst=scenarioDict[SubPackname] if scenarioDict!={} else []
                SubPackobj.ObjManager.Taglst=[obj.tag for obj in SubPackobj.ObjManager.Objlst]
                SubPackobj.ObjManager.TagObjDict={obj.tag:obj for obj in SubPackobj.ObjManager.Objlst}
        
        
        return 0    


    @staticmethod
    def load1ScenarioItt(ScenarioNumber, filename):
        '''
        This function returns all recorded objects of Scenario with number ScenarioNumber to the memory
        if no recorded data will be available in the current recording object or in the filename, 
        it retunes empty
        
        This function is proper for itterations and not proper for just one call
        
        '''
        
        #Check if the ScenarioNumber was less than 1 then comment
        if ScenarioNumber<1:
            print('Scenarios number start from 1!')
            return -1
            
        #Before any load all objects should be delete
        # _opr.wipe() #But it Decrease Speed Widely
        
        global _ScenarioFile    #it saves all scenarios of File with index _LoadedFile
        global _LoadedFile      #index of the loaded file
        if '_LoadedFile' not in globals(): _LoadedFile=None
        
        #get dictionary of the files and the number od analysis and scenarios boundary for each file
        FilesAnaScenNumbers=Objs_recorder_loader.ReturnFileIndexScenariosDict(filename)
        
        #Check if file exist
        if FilesAnaScenNumbers==-1:
            return -1
            
        #Get the maximum created scenario number
        MaxCreatedScenNum=Objs_recorder_loader.TotalNumberOfScenarios(filename)
            
        scenarioDict={}
        

        #check if ScenarioNumber is not greater than the recorded scenarios
        if MaxCreatedScenNum<ScenarioNumber:
            print(f"Entered Scenario Tag ({ScenarioNumber}) is greater than maximum recorded scenario so nothing loaded")
            return -1
            
        
        for filename,fileresult in FilesAnaScenNumbers.items():
            
            if ScenarioNumber>fileresult['Scenario Number Range'][1]:continue #Means that Targer scenario is not in the file

            FileScenarioRange=FilesAnaScenNumbers[filename]['Scenario Number Range']
            ScenarioNumber=ScenarioNumber-FileScenarioRange[0]
            
            if filename!=_LoadedFile: #Means that the proper file (File that the scenario is located in) is not loaded in the memory
                _LoadedFile=filename
                print('File',_LoadedFile, end=' ')
                
                # Read file and load scenario
                with open(filename+".OPR", 'rb') as fileObj:
                    _ScenarioFile=_pickle.load(fileObj)
                    print('loaded.',end=' ')
            
            if type(_ScenarioFile)==list:
                scenarioDict= _ScenarioFile[ScenarioNumber]
                
            break
        

        if scenarioDict=={}: 
            return -1
        
        #feed the loaded scenario to subpackages
        for SubPackname,SubPackobj in _opr.Misc.GetModules():
            
            if SubPackname!='Recorders' and SubPackname in scenarioDict.keys():
                #replace each subpackage Objlst, Taglst, TagObjDict with what are available in the recorded scenario
                SubPackobj.ObjManager.Objlst=scenarioDict[SubPackname] if scenarioDict!={} else []
                SubPackobj.ObjManager.Taglst=[obj.tag for obj in SubPackobj.ObjManager.Objlst]
                SubPackobj.ObjManager.TagObjDict={obj.tag:obj for obj in SubPackobj.ObjManager.Objlst}
        
        
        return 0    


    @staticmethod
    def LoadOtherSubPackages(filename):
        '''
        This function is for loading other subpackages that are saved just once and we should use it when we need them
        '''
        #Check if file exist
        if filename+'.Log' not in  _os.listdir() or filename+'.OPR' not in  _os.listdir():
            print(f'File {filename} does not exist and it OtherSubPackages are not loaded')
            return -1
    
        #Finally the OtherSubpackagesSavedOnce should be loaded
        # Read file and load scenario
        with open(filename+".OPR", 'rb') as fileObj:

            loadDict=_pickle.load(fileObj)

            if type(loadDict)==dict:
                scenarioDict= loadDict
                
        #feed the loaded scenario to subpackages
        for SubPackname,SubPackobj in _opr.Misc.GetModules():
            
            if SubPackname!='Recorders' and SubPackname in scenarioDict.keys():
                #replace each subpackage Objlst, Taglst, TagObjDict with what are available in the recorded scenario
                SubPackobj.ObjManager.Objlst=scenarioDict[SubPackname] if scenarioDict!={} else []
                SubPackobj.ObjManager.Taglst=[obj.tag for obj in SubPackobj.ObjManager.Objlst]
                SubPackobj.ObjManager.TagObjDict={obj.tag:obj for obj in SubPackobj.ObjManager.Objlst}
        
        return 0


#Bank Part ---------------------------------------------------------------------------------------------------------------


    @staticmethod
    def loadScenarioBank(filename):
        
        '''
        This function Loads all recorded Scenarios into the memory
        Then you can Call each scenario using load1ScenarioOfBank method
        
        '''

        global _ScenarioBank
        
        _ScenarioBank=[]
        
        for file in _os.listdir():
            if file[-3:]=='OPR' and file[:len(filename)]==filename:
            
                # Read file
                with open(file, 'rb') as fileObj:
                    loaddict=_pickle.load(fileObj)
                    if type(loaddict)==list: _ScenarioBank =  _ScenarioBank + loaddict 
                    
        if _ScenarioBank==[]:
            print(f'{file} not found!')
            return -1
            
        return len(_ScenarioBank)
      
      
    @staticmethod
    def load1ScenarioOfBank(ScenarioNumber):
        
        '''
        This function Loads one scenario from loaded bank
        
        '''
        
        if '_ScenarioBank' not in globals(): 
            print('No Scenario bank has been loaded in the memory')
            return -1
    
        global _ScenarioBank

        #Check if the ScenarioNumber was less than 1 then comment
        if ScenarioNumber<1:
            print('Scenarios number start from 1!')
            return -1
            
        #If entered tag be greater than what is recorded
        if ScenarioNumber>len(_ScenarioBank) : 
            print(f'Entered scenario tag ({ScenarioNumber}) is greater than the maximum recorded tag ({len(_ScenarioBank)}) so nothing loaded')
            return -1
        
        scenarioDict= _ScenarioBank[ScenarioNumber-1]
        
        #feed the subpackages
        for SubPackname,SubPackobj in _opr.Misc.GetModules():
            
            if SubPackname!='Recorders' and SubPackname in scenarioDict.keys():
                #replace each subpackage Objlst, Taglst, TagObjDict with what are available in the recorded scenario
                SubPackobj.ObjManager.Objlst=scenarioDict[SubPackname] if scenarioDict!={} else []
                SubPackobj.ObjManager.Taglst=[obj.tag for obj in SubPackobj.ObjManager.Objlst]
                SubPackobj.ObjManager.TagObjDict={obj.tag:obj for obj in SubPackobj.ObjManager.Objlst}
        
        scenarioDict={}
        
        return 0


    @staticmethod
    def ClearScenarioBank():
        '''
        this funtion clear loaded scenario bank from the memory
        '''
        global _ScenarioBank
        
        # if '_ScenarioBank' in globals(): del _ScenarioBank
        _ScenarioBank={}
        _gc.collect()        
        

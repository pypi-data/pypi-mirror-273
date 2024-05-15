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
import json as _json
import os as _os

class recorder(_NewClass):
    '''
    Developer Attention: To add any new recorder :
                                                    1st- Add target data to the "Record" method
                                                    2nd- Remember to add two header row to the 
    
    This Object Specify a recorder object that records type of data to a variable or a file
    filename: name of the file that user wants to store data in
    fileAppend: specify that does the recorder add data to the current data in name or not
    recordfield: Specifies the field of data that want to record. The selections are as the following
        'DamageLevel' : record the damage level of each plant unit ( the level that the plant unit got damage)
        'NodesGroupIsDamaged' : record the nodesgroup with tag equal NodesGroupTag is damaged or not (0 for not damaged and 1 for damaged or failed or dead)
        'FragilityTag' : record the Happened Fragility tag of each plant unit
        'LOC' : record the maximum released liquid (LOC : Loss of containment) of each plant unit
        'HazardMag' : Record the sampled hazard magnitude
        'NodesRadiationOverPressure' : Record NodesGroup Radiation,OverPressure 
        'NodesRadiationProbit' :
        'NodesOverPressureProbit' : 

        
        

    NodesGroupTag : Specify the tag of interested nodesgroup to be recorded for 'NodesGroupIsDamaged'
        
    recorded results is a list that in each line first it gives the scenario number and in the following it gives requested data
    
    '''
    
    def __init__(self,tag,filename='Recorder',fileAppend=True, recordfield='DamageLevel', NodesGroupTag=1, MergeSavedFiles=False):
         
        #---- Fix Part for each class __init__ ----
        ObjManager.Add(tag,self)
        _NewClass.__init__(self,tag)
        #------------------------------------------
        
        self.filename=filename
        self.fileAppend=fileAppend
        self.recordfield=recordfield
        self.NodesGroupTag=NodesGroupTag
        
        self.results=""        #String Variable that the results are stored in
        self.AnalyzeCounter=0  #Integer that counts the number of calling record method that shows the number of the analysis

        #Set does the code merge all created files together or not
        self.MergeSavedFiles=MergeSavedFiles
        
        #Remember for parallel analysis it cause multiple remove and in parallel do not set fileAppend==False
        if fileAppend==False:
            self._Deletefile()

        #If file append be True then code should find the number of maximum existing saved file and create new files with number greater than the founded number
        self.MaxExistSavedfileIndex=0
        if fileAppend==True:
            
            for file in _os.listdir():
                if file[-6:]=='OPRrec' and file[:len(filename)]==filename and len(file)>=len(filename+'.OPRrec'):
                    num=file[len(filename):-7]
                    if num!='' and num.isnumeric()==True:
                        if int(num)>self.MaxExistSavedfileIndex: self.MaxExistSavedfileIndex=int(num)            
        
    def Record(self):

        #By each time calling the Record command, 1 should be added to analyze counter 
        self.AnalyzeCounter +=1

        #If there is any damage then the data will be recorded
        if _opr.Analyze.ScenarioAnalyze.anydamage==False: return

        #-----------Case recordfield be 'DamageLevel'
        if self.recordfield=='DamageLevel':
            
          
            #Record data
            record=""   #Dictionary that records the current scenario data
            for tag,obj in _opr.PlantUnits.ObjManager.TagObjDict.items():
                
                #record damage level of the each plant unit
                record=record+str(obj.DamageLevel)+' '                     
        
        #-----------Case recordfield be 'NodesGroupIsDamaged'
        if self.recordfield=='NodesGroupIsDamaged':
            
               
            #Record data
            record=''   #Dictionary that records the current scenario data
            if _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].isDamagedList==[]: #Means not analyzed because no damage
                record='0 '*len(_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].xGlobalList)
            else:            

                #record damage level of the each plant unit
                record=record.join([("0 " if i==False else "1 ") for i in _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].isDamagedList])      

        #-----------Case recordfield be 'FragilityTag'
        if self.recordfield=='FragilityTag':
            
          
            #Record data
            record=""   #Dictionary that records the current scenario data
            for tag,obj in _opr.PlantUnits.ObjManager.TagObjDict.items():
                
                #record damage level of the each plant unit
                record=record+str(obj.DamageFragilityTag)+' '          

        #-----------Case recordfield be 'LOC'
        if self.recordfield=='LOC':
            
          
            #Record data
            record=""   #Dictionary that records the current scenario data
            for tag,obj in _opr.PlantUnits.ObjManager.TagObjDict.items():
                
                #record damage level of the each plant unit
                record=record+str(max(obj.OutFlowModelObject.TotalMassLiquid_Release) if obj.OutFlowModelObject!=None else 0)+' '         
                
        #-----------Case recordfield be 'HazardMag'
        if self.recordfield=='HazardMag':
            
          
            #Record data
            record=""   #Dictionary that records the current scenario data
            for tag,obj in _opr.Hazard.ObjManager.TagObjDict.items():
                
                #record damage level of the each plant unit
                record=record+str(obj.SampledMagnitude) +' '         

        #-----------Case recordfield be 'NodesRadiationOverPressure'
        if self.recordfield=='NodesRadiationOverPressure':
            
               
            #Record data
            record=''   #Dictionary that records the current scenario data
            if _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].isDamagedList==[]: #Means not analyzed because no damage
                record='0,0 '*len(_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].xGlobalList)
            else:            

                #record RadiationOverPressure for each node
                record=record.join([f"{round(Radiation,4)},{round(OVPressure,4)} " for Radiation,OVPressure in zip(_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].Radiation_Intensity,
                                                                                                                   _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].OverPressure_Intensity)])      

        #-----------Case recordfield be 'NodesToxic'
        if self.recordfield=='NodesToxic':
            
               
            #Record data
            record=''   #Dictionary that records the current scenario data
            if _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].isDamagedList==[]: #Means not analyzed because no damage
                record='None '*len(_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].xGlobalList)
            else:            

                #record damage level of the each plant unit
                record=record.join([",".join([f"{mattag}:{dose}" for mattag,dose in recDict.items()])+" " for recDict in _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].Toxic_Intensity])      

        #-----------Case recordfield be 'NodesRadiationProbit'
        if self.recordfield=='NodesRadiationProbit':
            
               
            #Record data
            record=''   #Dictionary that records the current scenario data
            if _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].isDamagedList==[]: #Means not analyzed because no damage
                record='0 '*len(_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].xGlobalList)
            else:            

                #record RadiationOverPressure for each node
                record=record.join([f"{RadiationProbit} " for RadiationProbit in _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].Radiation_Probit])      

        #-----------Case recordfield be 'NodesOverPressureProbit'
        if self.recordfield=='NodesOverPressureProbit':
            
               
            #Record data
            record=''   #Dictionary that records the current scenario data
            if _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].isDamagedList==[]: #Means not analyzed because no damage
                record='0 '*len(_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].xGlobalList)
            else:            

                #record RadiationOverPressure for each node
                record=record.join([f"{OverPressureProbit} " for OverPressureProbit in _opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].OverPressure_Probit])      

        #----- Final Part -----   (((Add recorded data to the results)))
        self.results=f'{self.results}\n{record}'            #Format of entering scenario tag and other
        
        
        
    def SaveToFile(self,fileindex):

        #fileindex: is an integer that will be add to the end of the filename to save in seperate file
        #fileindex are from 0 to number of files. If user wanna to append the existing files then the maximum index number of existing files should be added to input fileindex
        cnt=fileindex+self.MaxExistSavedfileIndex


        #--------------- First part: Define Header lines (Two First Rows) ---------------------------------------------------------------------
        
        #Fill two first header line
        #-----------Case recordfield be 'DamageLevel'
        if self.recordfield=='DamageLevel':

            header="%"+str(self.AnalyzeCounter) + '-'+"recordfield='DamageLevel'" #First line specify Number of analysis and the recordfield name
            header=f'{header}\n%PlantUnits tags = {[tag for tag in _opr.PlantUnits.ObjManager.TagObjDict.keys()]}' #Secondline specifiy the tags of the plant units

        #-----------Case recordfield be 'NodesGroupIsDamaged'
        if self.recordfield=='NodesGroupIsDamaged':

            header="%"+str(self.AnalyzeCounter) + '-'+"recordfield='NodesGroupIsDamaged'" #First line specify Number of analysis and the recordfield name
            header=f'{header}\n%NodesGroup with tags {self.NodesGroupTag} and with type={_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].Type}' #Secondline shows the tags and type of the nodesgroup

        #-----------Case recordfield be 'FragilityTag'
        if self.recordfield=='FragilityTag':

            header="%"+str(self.AnalyzeCounter) + '-'+"recordfield='FragilityTag'" #First line specify Number of analysis and the recordfield name
            header=f'{header}\n%PlantUnits tags = {[tag for tag in _opr.PlantUnits.ObjManager.TagObjDict.keys()]}' #Secondline specifiy the tags of the plant units

        #-----------Case recordfield be 'LOC'
        if self.recordfield=='LOC':

            header="%"+str(self.AnalyzeCounter) + '-'+"recordfield='LOC'" #First line specify Number of analysis and the recordfield name
            header=f'{header}\n%PlantUnits tags = {[tag for tag in _opr.PlantUnits.ObjManager.TagObjDict.keys()]}' #Secondline specifiy the tags of the plant units

        #-----------Case recordfield be 'HazardMag'
        if self.recordfield=='HazardMag':

            header="%"+str(self.AnalyzeCounter) + '-'+"recordfield='HazardMag'" #First line specify Number of analysis and the recordfield name
            header=f'{header}\n%Defined Hazards tags = {[tag for tag in _opr.Hazard.ObjManager.TagObjDict.keys()]}' #Secondline specifiy the tags of the plant units

        #-----------Case recordfield be 'NodesRadiationOverPressure'
        if self.recordfield=='NodesRadiationOverPressure':

            header="%"+str(self.AnalyzeCounter) + '-'+"recordfield='NodesRadiationOverPressure'" #First line specify Number of analysis and the recordfield name
            header=f'{header}\n%(Radiation,OverPressure) for NodesGroup with tags {self.NodesGroupTag} and with type={_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].Type}' #Secondline shows the tags and type of the nodesgroup

        #-----------Case recordfield be 'NodesToxic'
        if self.recordfield=='NodesToxic':

            header="%"+str(self.AnalyzeCounter) + '-'+"recordfield='NodesToxic'" #First line specify Number of analysis and the recordfield name
            header=f'{header}\n%(ProbitTag:Dose,...) [(0:0) for not for No toxic tag] NodesGroup with tags {self.NodesGroupTag} and with type={_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].Type}' #Secondline shows the tags and type of the nodesgroup

        #-----------Case recordfield be 'NodesRadiationProbit'
        if self.recordfield=='NodesRadiationProbit':

            header="%"+str(self.AnalyzeCounter) + '-'+"recordfield='NodesRadiationProbit'" #First line specify Number of analysis and the recordfield name
            header=f'{header}\n%NodesGroup with tags {self.NodesGroupTag} and with type={_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].Type}' #Secondline shows the tags and type of the nodesgroup

        #-----------Case recordfield be 'NodesOverPressureProbit'
        if self.recordfield=='NodesOverPressureProbit':

            header="%"+str(self.AnalyzeCounter) + '-'+"recordfield='NodesOverPressureProbit'" #First line specify Number of analysis and the recordfield name
            header=f'{header}\n%NodesGroup with tags {self.NodesGroupTag} and with type={_opr.NodesGroups.ObjManager.TagObjDict[self.NodesGroupTag].Type}' #Secondline shows the tags and type of the nodesgroup


        #----- Final Part ----- Write to file/s 
        #Add results to header
        self.results=str(header)+str(self.results)

        #(((Save recorded data to the file or files (Create new file and write to it))))
        with open(self.filename+str(cnt)+'.OPRrec', 'w' ) as file:
                file.write(str(self.results))        
                self.results=""                 #Clear results after writing them in file

        #Set the Recorder Counter to zero
        self.AnalyzeCounter=0
    
    def OtherSaveOnce(self):
        #Just because such method exist for objs_recorder, so here also should exist to avoid error when calling all objects (For recorder it doesn't do anything
        pass
    
    
    def _Deletefile(self):
        
            
        #Remove all OPR files
        for file in _os.listdir():
            if file[-6:]=='OPRrec' and file[:len(self.filename)]==self.filename:
                _os.remove(file)

    def _MergeAndClear(self):
        '''
        Merge multiple files to gether and clear the created files

        '''
        
        #At the end of analysis _MergeAndClear method for any object will be called and for each object 
        if self.MergeSavedFiles==True:
        
            AllData=''
            AllAnalysisNumber=0
            files=_os.listdir()

            #Set files equal the files that their name is similar with 
            Recfiles=[file for file in files if (file.startswith(self.filename) and file.endswith('OPRrec') and len(file)>len(self.filename+'.OPRrec'))]

            #Get all files content

            for file in Recfiles:
                
                #read file data
                with open(file,'r') as f:
                
                    #Get and store the number of analysis
                    data=f.readlines()
                    FirstLine=data[0]  #Save firstline 
                    Secondline=data[1] #Save second line data
                    Number_of_analysis=data[0].split('-')[0][1:]
                    AllAnalysisNumber=AllAnalysisNumber+int(Number_of_analysis)
                    data=''.join(data[2:])  
                    AllData=AllData +"\n"+data if data!='' else AllData
                
                #Remove file
                _os.remove(file)

                
            #Create first two lines
            header="%"+str(AllAnalysisNumber)+'-'+FirstLine.split('-')[1][:-1]+'\n'+Secondline[:-1]

            #add allData to the main file data
            AllData=header+AllData

            with open(self.filename+'M.OPRrec', 'w' ) as file:
                    file.write(AllData)  



    def LoadRecorderfile(self,filename=''):
        '''
        This function return results of as a dictionary with keys equal to scenario tag and values equal to entered value
        '''
        if filename=='': filename=self.filename+'.OPRrec'
        
        with open(filename, "r") as file:
            data = file.readlines()
            
        result={}   #Dictionary of the results
        scenario=0
        for dat in data[2:]:                        #data[2:] beccause two first lines are headers
            scenario +=1         #First value that separated with : is the tag value    
            rslt=[]
            [rslt.extend([float(val) if val!='None' else None]) for val in dat.split()]
            result[scenario]=rslt
            
        return result
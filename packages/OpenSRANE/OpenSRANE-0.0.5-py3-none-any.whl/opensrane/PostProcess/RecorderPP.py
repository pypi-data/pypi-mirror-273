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


import opensrane as _opr
import random as _rnd
from tqdm import tqdm as _tqdm
import multiprocessing as _mp
import numpy as _np
import os as _os
import plotly.express as _px
import plotly.graph_objects as _go
import math as _math
from plotly.offline import iplot as _iplot
from plotly.offline import plot as _plot

class RecorderPP():
    
    Results=None
    
    def __init__(self,Recorder_FilenamesList=[],Number_Of_LOC_Histogram_Bins=100):
        
        self.Number_Of_LOC_Histogram_Bins=Number_Of_LOC_Histogram_Bins
        
        self.Recorder_FilenamesList=[] #list of the Recorder filename that defined by user
        self.Recorder_files=[]         #List of the existing files
        
        #Check files content one by one and if exist then will be append to Recorder_FilenamesList
        files=_os.listdir()
                
        for filename in Recorder_FilenamesList:
            for file in files:
                #Check if file exist
                if file.startswith(filename):
                    self.Recorder_FilenamesList.append(filename)
                    self.Recorder_files.append(file)
                    
        for filename in Recorder_FilenamesList:
            if filename not in self.Recorder_FilenamesList:
                print(f'file {filename} does not exist in the current directory files')
                
                
        #Get Total Number of Analysis
        self.TotalScenario=self.Total_Num_of_Analyze()

    def DamagedLevelList(self):
    
        DamagedLevelListVar=[] #list of the plant units Damage level list, each value is a Dictionary of Damage level of the plant units for each scenario

        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need
            if self.File_RecordField(filedata)=='DamageLevel':
                
                #Export PlantUnits objects tag
                Objstag=filedata[1].split('=')[1].split('[')[1].split(']')[0].split(',')
                Objstag=[int(i) for i in Objstag]


                # Export DamagedLevelList data
                for linedata in filedata[2:]:   #data[2:] beccause two first lines are headers
                    
                    DamagedLevelListVar.append({tag:(int(dmlvl) if dmlvl!='None' else None)  for tag,dmlvl in zip(Objstag,linedata.split())})
        
        return DamagedLevelListVar
            
    
    def FragilityTagList(self):
    
        FragilityTagListVar=[]             #List of the plant units happend fragility tag Dictionaries, 
        
        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need     
            if self.File_RecordField(filedata)=='FragilityTag':

                #Export PlantUnits objects tag
                Objstag=filedata[1].split('=')[1].split('[')[1].split(']')[0].split(',')
                Objstag=[int(i) for i in Objstag]

                # Export Fragility/Probit recorded data
                for linedata in filedata[2:]:    #data[2:] beccause two first lines are headers
                    
                    FragilityTagListVar.append({tag:(int(Fragtag) if Fragtag!='None' else None)  for tag,Fragtag in zip(Objstag,linedata.split())})   

        
        return FragilityTagListVar
        
    def LOCList(self):
    
        LOCListVar=[]                      #List of the PlantUnits tag and max Loss of Containment value Dictionary
        
        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata)=='LOC':

                #Export PlantUnits objects tag
                Objstag=filedata[1].split('=')[1].split('[')[1].split(']')[0].split(',')
                Objstag=[int(i) for i in Objstag]

                # Export LOC recorded data
                for linedata in filedata[2:]:    #data[2:] beccause two first lines are headers
                    
                    LOCListVar.append({tag:float(Loci) for tag,Loci in zip(Objstag,linedata.split())})       
        
        return LOCListVar
        
    def NodesGroupDamageList(self):
    
        NodesGroupDamageListVar=[]         #List of NodesGroup isDamaged list, each Dictionary is NodesGroupTag and corresponding Damagelist
        
        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata)=='NodesGroupIsDamaged':    

                #Export NodesGroup Tag and type
                NodesGroupTag=int(filedata[1].split()[3])
                NodesGroupType=filedata[1].split('=')[-1]
                
                #Export Data
                for linedata in filedata[2:]:    #data[2:] beccause two first lines are headers
                    NodesGroupDamageListVar.append({NodesGroupTag:[int(isDam) for isDam in linedata.split()]}) 
                    
        return NodesGroupDamageListVar
        
    def NodesGroupTypeDict(self):

        NodesGroupTypeDictVar={}           #Dictionray of each NodesGroup object that keys are tag of nodes group and values are the type of the nodes group
        
        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata) in ['NodesGroupIsDamaged', 'NodesRadiationOverPressure','NodesRadiationProbit','NodesOverPressureProbit']: 

                #Export NodesGroup Tag and type
                NodesGroupTag=int(filedata[1].split()[3]) if self.File_RecordField(filedata) != 'NodesRadiationOverPressure' else int(filedata[1].split()[5])
                NodesGroupType=filedata[1].split('=')[-1][:-1]
                
                #NodesGroupTypeDict
                NodesGroupTypeDictVar[NodesGroupTag]=NodesGroupType


        return NodesGroupTypeDictVar
        
        
    def NodesGroupDamageProbability(self):
        NodesGroupDamProb={}            #Dictionray of each NodesGroup object that keys are tag of nodes group and values are the probability of their damage
    
        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata)=='NodesGroupIsDamaged':    

                #Export NodesGroup Tag and type
                NodesGroupTag=int(filedata[1].split()[3])
                
                #----Probability of NodesGroup Damage
                NGtag=NodesGroupTag
                
                if NGtag not in NodesGroupDamProb.keys():
                    NodesGroupDamProb[NGtag]=[0 for i in filedata[2].split()]

                for linedata in filedata[2:]:

                    NodesGroupDamProb[NGtag]=[i+int(j) for i,j in zip(NodesGroupDamProb[NGtag],linedata.split())]

        #convert to expected Value
        NodesGroupDamProb[NGtag]=[i/self.TotalScenario for i in NodesGroupDamProb[NGtag]]
                
        return NodesGroupDamProb
        
        
        
        
    def TotalLOCList(self):
        
        ListOfLoc=[sum(list(LOCDIC.values())) for LOCDIC in self.LOCList()]
    
        return ListOfLoc
        
        
    def LOC_bins_hist_probloc(self):
    
        [bins,hist,probloc]=[[],[],[]]  #statistics parameters of LOC in scenarios (bins of LOC, histogram values, probability values)
        
        ListOfLoc=self.TotalLOCList()
        
        minLoc=min([i for i in ListOfLoc if i!=0])
        maxLoc=max([i for i in ListOfLoc if i!=0])
        nbins=self.Number_Of_LOC_Histogram_Bins
        hist, bins=_np.histogram(ListOfLoc,bins=[minLoc+(maxLoc-minLoc)/nbins*i for i in range(nbins+1)]) #length of the bins always should be one more than length of the hist    
        probloc=[i/self.TotalScenario for i in hist] 
    
        return [bins,hist,probloc]
        
    def Damagelevel_eLOC(self):
    
        DmglvlLOC={}

    
        #----Damagelevel and corresponding expected loss of containment
        for dam,loc in zip(self.DamagedLevelList(),self.LOCList()):
            for tag,dmlvl in dam.items():
                if (dmlvl not in list(DmglvlLOC.keys()) and dmlvl!=None):
                    DmglvlLOC[dmlvl]=0
                if (loc[tag]!=None and dmlvl!=None):
                    DmglvlLOC[dmlvl]=DmglvlLOC[dmlvl]+loc[tag]
            
        #convert to expected Value
        for dmlvl,loc in DmglvlLOC.items():
            DmglvlLOC[dmlvl]=loc/self.TotalScenario    
    
    
        return DmglvlLOC
        
    def Total_Number_Of_Scenarios(self):
        
        return self.TotalScenario
        
    def UnitsZeroDamageProb(self):
    
        UnitsZeroDamageProbVar={}          #Probability of each PlantUnit zero level damage


        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata)=='DamageLevel':    
                
                #Export PlantUnits objects tag
                Objstag=filedata[1].split('=')[1].split('[')[1].split(']')[0].split(',')
                Objstag=[int(i) for i in Objstag]
                
                #------ Probability of Units Zero Level Damage
                UnitsZeroDamageProbVar={tag:0 for tag in Objstag}
                for DamLevelDict in self.DamagedLevelList():
                    for tag,DamLev in DamLevelDict.items() :
                        if DamLev==0: UnitsZeroDamageProbVar[tag]=UnitsZeroDamageProbVar[tag]+1

        #convert to probability
        UnitsZeroDamageProbVar={tag:DamLev/self.TotalScenario for tag,DamLev in UnitsZeroDamageProbVar.items()}
        
        
    
        return UnitsZeroDamageProbVar
        
    def ProbOfFragilities(self):

        ProbOfFragilitiesVar=[]            #Probablility of happening each fragility 

        #find Fragilities tag (Fragtags)
        Fragtags=[]
        [Fragtags.extend([fragtag for fragtag in fragdict.values() if fragtag!=None]) for fragdict in self.FragilityTagList()]
        Fragtags=list(set(Fragtags))

        ProbOfFragilitiesVar={tag:0 for tag in Fragtags}
        for FragDict in self.FragilityTagList():
            for Fragtag in FragDict.values() :
                if Fragtag!=None: ProbOfFragilitiesVar[Fragtag]=ProbOfFragilitiesVar[Fragtag]+1

        #convert to probability
        ProbOfFragilitiesVar={tag:Num/self.TotalScenario for tag,Num in ProbOfFragilitiesVar.items()}

        return ProbOfFragilitiesVar
        
    def ScenariosAnalyzeNumbers(self):
    
        ScenariosAnalyzeNumbersVar={} #Store scenario(key)  and number of analyzed scenarios list (Value)
        for ScenarioNum,damagelistrow in enumerate(self.DamagedLevelList()):
            LevelList=RecorderPP._LevelList(damagelistrow)
            LevelList=['-'.join(LevelList[:i])  for i in range(1,len(LevelList)+1)]
            
            #Fill Results for ScenariosProbability
            if LevelList!=[]: 
                i=LevelList[-1]
                if i not in ScenariosAnalyzeNumbersVar.keys():
                    ScenariosAnalyzeNumbersVar[i]=[ScenarioNum]
                else:
                    ScenariosAnalyzeNumbersVar[i].append(ScenarioNum)      
                            
        return ScenariosAnalyzeNumbersVar
        
    def ScenariosProbability(self):

        Results={} #Store scenario and number of happening (ScenariosProbability)
        
        for ScenarioNum,damagelistrow in enumerate(self.DamagedLevelList()):
            LevelList=RecorderPP._LevelList(damagelistrow)
            LevelList=['-'.join(LevelList[:i])  for i in range(1,len(LevelList)+1)]
            
            #Fill Results for ScenariosProbability
            if LevelList!=[]: 
                
                for i in  LevelList:
                    if i not in Results.keys():
                        Results[i]=1
                    else:
                        Results[i]=Results[i]+1

        #Convert Results number to probability(value) (Scenario(key)) 
        ScenariosProbabilityVar={tag:val/self.TotalScenario for tag,val in Results.items()}
        
        return ScenariosProbabilityVar
        
    def ScanariosSubScenario(self):

        Results={}          #Store scenario and number of happening (ScenariosProbability)
        DamlvlScenDict=self.Damagelevel_Scenario_Dict()   #Dictionary of damage level (key) and corresponding Scenarios set (Value)
        
        for ScenarioNum,damagelistrow in enumerate(self.DamagedLevelList()):
            LevelList=RecorderPP._LevelList(damagelistrow)
            LevelList=['-'.join(LevelList[:i])  for i in range(1,len(LevelList)+1)]     
                    
            #Fill Results for ScenariosProbability
            if LevelList!=[]: 
                
                for i in  LevelList:
                    if i not in Results.keys():
                        Results[i]=1
                    else:
                        Results[i]=Results[i]+1
                    
        #Scenarios(key) and its SubScenariosList(Value) Dictionary
        dmlvl=lambda scenario: [key for key,val in DamlvlScenDict.items() if scenario in val][0] #Find scenario damage level
        ScanariosSubScenarioVar={Scenario:[] for Scenario in Results.keys()}
        for Scenario in ScanariosSubScenarioVar.keys():
            ScanariosSubScenarioVar[Scenario]=[SubScen for SubScen in Results.keys() if (dmlvl(SubScen)==dmlvl(Scenario)+1 and Scenario in SubScen)]
    
        return ScanariosSubScenarioVar
  
        
    def Damagelevel_Scenario_Dict(self):
    
        DamlvlScenDict={}   #Dictionary of damage level (key) and corresponding Scenarios set (Value)
        
        for ScenarioNum,damagelistrow in enumerate(self.DamagedLevelList()):
            LevelList=RecorderPP._LevelList(damagelistrow)
            LevelList=['-'.join(LevelList[:i])  for i in range(1,len(LevelList)+1)]
            
            #fill DamlvlScenDict
            for lvl,name in enumerate(LevelList):
                if lvl not in DamlvlScenDict.keys():
                    DamlvlScenDict[lvl]=set([name])
                else:
                    DamlvlScenDict[lvl].update([name])
    
        return DamlvlScenDict
        
    def HazardMagnitude(self):
        
        HazardMagnitudeVar=[]              #List of the hazard tags and magnitudes (tag as key and magnitude as value)

        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata)=='HazardMag': 
                
                #Export Hazard objects tag
                Objstag=filedata[1].split('=')[1].split('[')[1].split(']')[0].split(',')
                Objstag=[int(i) for i in Objstag]


                # Export Hazard data
                for linedata in filedata[2:]:   #data[2:] beccause two first lines are headers
                    
                    HazardMagnitudeVar.append({tag:(float(mag))  for tag,mag in zip(Objstag,linedata.split())})
        
        return HazardMagnitudeVar
        
        
    def ScenarioName_DamageLevel_Dict(self):

        ScenNameDamLvlDict={}            #Dictionary that its key is Scenario name and the value is its corresponding Damage level Dictionary

        #Create Damage Level and Corresponding Name Dictionary
        for dmlvl in self.DamagedLevelList():
            ScenNameDamLvlDict["-".join(RecorderPP._LevelList(dmlvl))]=dmlvl  

        return ScenNameDamLvlDict
        
    def NodesGroupRadiationDict(self): 
    
        NodesGroupRadiationAveDict={}  #Dictionary of NodesGroup Radiation Data, and keys is Nodes Group tag and value is the list of Radiation values Average 
        NodesGroupTypeDict={}           #Dictionray of each NodesGroup object that keys are tag of nodes group and values are the type of the nodes group

        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata)=='NodesRadiationOverPressure':
                
                #import NodesGroup Tag and type
                NodesGroupTag=int(filedata[1].split()[5])
                NodesGroupType=filedata[1].split('=')[-1]

                #NodesGroupTypeDict
                NodesGroupTypeDict[NodesGroupTag]=NodesGroupType

                # import NodesRadiationOverPressure data
                for linedata in filedata[2:]:   #data[2:] beccause two first lines are headers

                    if NodesGroupTag not in NodesGroupRadiationAveDict.keys():
                        NodesGroupRadiationAveDict[NodesGroupTag]=[0 for i in [float(data.split(',')[0])  for data in linedata.split()]]
                    
                    NodesGroupRadiationAveDict[NodesGroupTag]=[i+j for i,j in zip(NodesGroupRadiationAveDict[NodesGroupTag],[float(data.split(',')[0])  for data in linedata.split()])]

        #Convert to average
        NodesGroupRadiationAveDict[NodesGroupTag]=[i/self.TotalScenario for i in NodesGroupRadiationAveDict[NodesGroupTag]]
    
        return NodesGroupRadiationAveDict
        
        
    def NodesGroupOverPressureDict(self):
    
        NodesGroupOverPressureAveDict={}  #Dictionary of NodesGroup OverPressure Data, and keys is Nodes Group tag and value is the list of OverPressure values Average
        NodesGroupTypeDict={}           #Dictionray of each NodesGroup object that keys are tag of nodes group and values are the type of the nodes group

        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata)=='NodesRadiationOverPressure':
                
                #import NodesGroup Tag and type
                NodesGroupTag=int(filedata[1].split()[5])
                NodesGroupType=filedata[1].split('=')[-1]

                #NodesGroupTypeDict
                NodesGroupTypeDict[NodesGroupTag]=NodesGroupType

                # import NodesRadiationOverPressure data
                for linedata in filedata[2:]:   #data[2:] beccause two first lines are headers

                    if NodesGroupTag not in NodesGroupOverPressureAveDict.keys():
                        NodesGroupOverPressureAveDict[NodesGroupTag]=[0 for i in [float(data.split(',')[0])  for data in linedata.split()]]
                    
                    NodesGroupOverPressureAveDict[NodesGroupTag]=[i+j for i,j in zip(NodesGroupOverPressureAveDict[NodesGroupTag],[float(data.split(',')[1])  for data in linedata.split()])]

        #Convert to average
        NodesGroupOverPressureAveDict[NodesGroupTag]=[i/self.TotalScenario for i in NodesGroupOverPressureAveDict[NodesGroupTag]]
    
        return NodesGroupOverPressureAveDict
        
        
        
    def NodesGroup_OVP_Probit_Dict(self):
    
        NodesGroupOVPProbAveDict={}     #Dictionary of NodesGroup OverPressure corresponding Probit Data, and keys is Nodes Group tag and value is the list of Probit(OverPressure) values Average 
        NodesGroupTypeDict={}           #Dictionray of each NodesGroup object that keys are tag of nodes group and values are the type of the nodes group
        
        
        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata)=='NodesOverPressureProbit':
                
                #import NodesGroup Tag and type
                NodesGroupTag=int(filedata[1].split()[3])
                NodesGroupType=filedata[1].split('=')[-1]

                #NodesGroupTypeDict
                NodesGroupTypeDict[NodesGroupTag]=NodesGroupType


                # import NodesOverPressureProbit data
                for linedata in filedata[2:]:   #data[2:] beccause two first lines are headers

                    if NodesGroupTag not in NodesGroupOVPProbAveDict.keys():
                        NodesGroupOVPProbAveDict[NodesGroupTag]=[0 for i in [float(data)  for data in linedata.split()]]

                    NodesGroupOVPProbAveDict[NodesGroupTag]=[i+j for i,j in zip(NodesGroupOVPProbAveDict[NodesGroupTag],[float(data)  for data in linedata.split()])]

        #Convert to average
        NodesGroupOVPProbAveDict[NodesGroupTag]=[i/self.TotalScenario for i in NodesGroupOVPProbAveDict[NodesGroupTag]]
        
        return NodesGroupOVPProbAveDict
        
        
        
    def NodesGroup_Rad_Probit_Dict(self):   
        
        NodesGroupRadProbAveDict={}     #Dictionary of NodesGroup Radiation Probit Data, and keys is Nodes Group tag and value is the list of Probit(Radiation) values Average
        NodesGroupTypeDict={}           #Dictionray of each NodesGroup object that keys are tag of nodes group and values are the type of the nodes group
        
        
        #Check all files
        for file in self.Recorder_files:
            
            with open(file, "r") as file:
                filedata = file.readlines()
            
            #Check if Recordfiled of loaded file is compatible with what we need        
            if self.File_RecordField(filedata)=='NodesRadiationProbit':
                
                #import NodesGroup Tag and type
                NodesGroupTag=int(filedata[1].split()[3])
                NodesGroupType=filedata[1].split('=')[-1]

                #NodesGroupTypeDict
                NodesGroupTypeDict[NodesGroupTag]=NodesGroupType


                # import NodesRadiationProbit data
                for linedata in filedata[2:]:   #data[2:] beccause two first lines are headers

                    if NodesGroupTag not in NodesGroupRadProbAveDict.keys():
                        NodesGroupRadProbAveDict[NodesGroupTag]=[0 for i in [float(data)  for data in linedata.split()]]

                    NodesGroupRadProbAveDict[NodesGroupTag]=[i+j for i,j in zip(NodesGroupRadProbAveDict[NodesGroupTag],[float(data)  for data in linedata.split()])]


        #Convert to average
        NodesGroupRadProbAveDict[NodesGroupTag]=[i/self.TotalScenario for i in NodesGroupRadProbAveDict[NodesGroupTag]]
        
        return NodesGroupRadProbAveDict
        
        
#--------------------------- Some required internal methods --------------------------------------------

    def _LevelList(damagelistrow):
        #This function returns damage levels and corresponding tags
        #Format= (Damage Level):[tag of damaged units]

        #if no damage happened return []
        if 0 not in damagelistrow.values(): return []

        #Export data
        rslt={}
        for tag,dmlvl in damagelistrow.items():
            if dmlvl not in list(rslt.keys()) and dmlvl!=None:
                rslt[dmlvl]=str(tag)
            elif dmlvl!=None:
                rslt[dmlvl]=rslt[dmlvl]+','+str(tag)
        

        #Arrange data from 0 to ... 
        finalrslt=[]
        for dmlvl in range(max(rslt.keys())+1):
            text=f'({dmlvl}):[{rslt[dmlvl]}]'   #Convert to text format
            finalrslt.append(text)

        return finalrslt
        
        
        
    def File_Num_of_Analyze(self,filedata):
        #This function gets the read file data and returns the num of analysis and RecordField
        return filedata[0].split('-')[0][1:]
        
        
    def File_RecordField(self,filedata):
        #This method returns the Record field name of file 
        return filedata[0].split('-')[1].split('=')[1][1:-2]
        
    def Total_Num_of_Analyze(self):
    
        filename=self.Recorder_FilenamesList[0] #Get the name of first recorder file
        files=[file for file in self.Recorder_files if file.startswith(filename)]
        
        Total=0
        for file in files:
            with open(file, "r") as file:
                filedata = file.readlines()
                
            Total+=int(self.File_Num_of_Analyze(filedata))
            
        return Total
        
    def NumberOfScenarios(self):
    
        filename=self.Recorder_FilenamesList[0] #Get the name of first recorder file
        files=[file for file in self.Recorder_files if file.startswith(filename)]
        
        Total=0
        for file in files:
            with open(file, "r") as file:
                filedata = file.readlines()
            
            Total+=len(filedata[2:])
            
        return Total
        
        
        
        
    #------------------------------------------- Plotting Part ---------------------------------------------
    
    def plot_DamageLevel_ExpectedLoss(self, yaxistype='log',PlotMode=1,height=None,width=None,):
        
        '''
        This function plots the expected loss of containment in each damage level
        
        yaxistype is the type of the yaxis ['linear', 'log', 'date', 'category','multicategory']

        '''
        dmloc=self.Damagelevel_eLOC()

        fig = _px.bar(x=list(dmloc.keys()), y=list(dmloc.values()), labels={'x':'Damage level', 'y':'Expected liquid loss of Containment (kg)'},  opacity=0.75)

        #set range for lof type
        yaxisrange=None
        if yaxistype=='log':
            miny=min(list(dmloc.values()))
            #To prevent sending zero for log function
            if miny==0:
                sortlis=list(dmloc.values())
                sortlis=list(set(sortlis))
                sortlis.sort()
                miny=sortlis[1]

            miny=int(_math.log10(miny))-1

            maxy=max(list(dmloc.values()))
            maxy=int(_math.log10(maxy))+1

            yaxisrange=[miny,maxy]              #in log type plotly consider the entered values as power of ten

        fig.update_layout(
            title_text='Expected loss of containment in each damage level', # title of plot
            bargap=0.01, # gap between bars of adjacent location coordinates
            plot_bgcolor='white', 
            yaxis=dict(type=yaxistype,range=yaxisrange, showline=True, linecolor='black',linewidth=2),
            xaxis=dict(type='linear',showline=True, linecolor='black',linewidth=2)
        )
        
        if height!=None:
            fig.update_layout(height=height)
        if width!=None:
            fig.update_layout(width=width)        

        if PlotMode==3:
        
            return _iplot(fig)
            
        elif PlotMode==2:
            
            image_filename='DamageLevel_ExpectedLoss.html'
            _plot(fig,filename=image_filename)
            
        else:
            fig.show()
            
    def plot_Unit_ZeroLevel_DamageProb(self, yaxistype='log',PlotMode=1,height=None,width=None,):
        
        '''
        This function plots each plant unit damage probability in zero level

        yaxistype is the type of the yaxis ['linear', 'log', 'date', 'category','multicategory']
        
        '''
        zerdamp=self.UnitsZeroDamageProb()

        fig = _px.bar(x=list(zerdamp.keys()), y=list(zerdamp.values()), labels={'x':'Unit tag', 'y':'probability of damage in zero level'},  opacity=0.75)

        #set range for lof type
        yaxisrange=None
        if yaxistype=='log':
            miny=min(list(zerdamp.values()))
            #To prevent sending zero for log function
            if miny==0:
                sortlis=list(zerdamp.values())
                sortlis=list(set(sortlis))
                sortlis.sort()
                miny=sortlis[1]

            miny=int(_math.log10(miny))-1

            yaxisrange=[miny,0]              #in log type plotly consider the entered values as power of ten


        fig.update_layout(
            title_text='Expected unit zero level damage', # title of plot
            bargap=0.01, # gap between bars of adjacent location coordinates
            plot_bgcolor='white',
            yaxis=dict(type=yaxistype,showline=True, linecolor='black',linewidth=2,range=yaxisrange),
            xaxis=dict(type='linear',showline=True, linecolor='black',linewidth=2), 
        )

        if height!=None:
            fig.update_layout(height=height)
        if width!=None:
            fig.update_layout(width=width)        

        if PlotMode==3:
        
            return _iplot(fig)
            
        elif PlotMode==2:
            
            image_filename='Unit_ZeroLevel_DamageProb.html'
            _plot(fig,filename=image_filename)
            
        else:
            fig.show()
            

    def plot_Fragilities_Probits_Probability(self, yaxistype='log',PlotMode=1,height=None,width=None,):
        
        '''
        This function plots each fragility and probit happening probability

        yaxistype is the type of the yaxis ['linear', 'log', 'date', 'category','multicategory']
        
        '''
        FragProbHapp=self.ProbOfFragilities()

        fig = _px.bar(x=list(FragProbHapp.keys()), y=list(FragProbHapp.values()), labels={'x':'Fragility tag', 'y':'probability of Fragility Happening'},  opacity=0.75)

        #set range for lof type
        yaxisrange=None
        if yaxistype=='log':
            miny=min(list(FragProbHapp.values()))
            #To prevent sending zero for log function
            if miny==0:
                sortlis=list(FragProbHapp.values())
                sortlis=list(set(sortlis))
                sortlis.sort()
                miny=sortlis[1]

            miny=int(_math.log10(miny))-1

            yaxisrange=[miny,0]              #in log type plotly consider the entered values as power of ten

        fig.update_layout(
            title_text='Expected Fragility/Probit happening', # title of plot
            bargap=0.01, # gap between bars of adjacent location coordinates
            plot_bgcolor='white',
            yaxis=dict(type=yaxistype,showline=True, linecolor='black',linewidth=2,range=yaxisrange),
            xaxis=dict(type='linear',showline=True, linecolor='black',linewidth=2) 
        )

        if height!=None:
            fig.update_layout(height=height)
        if width!=None:
            fig.update_layout(width=width)        

        if PlotMode==3:
        
            return _iplot(fig)
            
        elif PlotMode==2:
            
            image_filename='Fragilities_Probits_Probability.html'
            _plot(fig,filename=image_filename)
            
        else:
            fig.show()


    def plot_Expected_Total_LOC(self, yaxistype='log',PlotMode=1,height=None,width=None,):
        
        '''
        This function plots expected total loss of containment

        yaxistype is the type of the yaxis ['linear', 'log', 'date', 'category','multicategory']
        
        '''

        bins,hist,probloc=self.LOC_bins_hist_probloc()
        TotalLOCList=self.TotalLOCList()

        bins=[(i+j)/2 for i,j in zip(bins[:-1],bins[1:])] #to get the average of the data (length of the bins is always one value greater than hist and probloc)


        fig = _px.histogram(x=TotalLOCList, nbins=400,log_y=True,log_x=False,width=700,height=600,histnorm='probability',
                            labels={'x':'Totla Loss (kg)', 'y':'Probability'},opacity=0.75)

         #set range for lof type
        yaxisrange=None
        if yaxistype=='log':
            probloc=list(set(probloc))
            probloc.sort()
            if probloc[0]==0:probloc.pop(0)
            miny=min(probloc)
            miny=int(_math.log10(miny))-1
            yaxisrange=[miny,0]              #in log type plotly consider the entered values as power of ten


        fig.update_layout(bargap=0.2,
                          plot_bgcolor='white', 
                          yaxis=dict(type=yaxistype,showline=True, linecolor='black',linewidth=2,range=yaxisrange),
                          xaxis=dict(type='linear',showline=True, linecolor='black',linewidth=2))
        if height!=None:
            fig.update_layout(height=height)
        if width!=None:
            fig.update_layout(width=width)        

        if PlotMode==3:
        
            return _iplot(fig)
            
        elif PlotMode==2:
            
            image_filename='Expected_Total_LOC.html'
            _plot(fig,filename=image_filename)
            
        else:
            fig.show()

        # fig = px.bar(x=bins, y=hist, labels={'x':'Totla Loss', 'y':'count'},  opacity=0.75)
        # fig.update_layout(
        #     title_text='Sampled Results', # title of plot
        #     bargap=0.01, # gap between bars of adjacent location coordinates
        # )
        # fig.show()
        # fig = px.bar(x=bins, y=probloc, labels={'x':'Totla Loss', 'y':'Probability'},  opacity=0.75)
        # fig.update_layout(
        #     title_text='Sampled Results', # title of plot
        #     bargap=0.01, # gap between bars of adjacent location coordinates
        # )
        # fig.show()

    def plot_ScenarioProbability(self, yaxistype='log',DamageLevel=[],ScenarioList=[],PlotMode=1,height=None,width=None,):

        '''
        This function plots Scenarios versus their probability value in all damage levels
        
        DamageLevel = List of damage level that user want to watch the results

        ScenarioList=List of scenarios that want to be shown in graph. (for Empty it means that plot all scenarios)

        yaxistype is the type of the yaxis ['linear', 'log', 'date', 'category','multicategory']

        '''

        ScenProb=self.ScenariosProbability()
        DamLvlScenDict=self.Damagelevel_Scenario_Dict()

        if DamageLevel!=[]:
            ScenLevel=[]
            [ScenLevel.extend(scenlist) for dmlvl,scenlist in DamLvlScenDict.items() if dmlvl in DamageLevel]
            ScenProb={scen:prob for scen,prob in ScenProb.items() if scen in ScenLevel}
        
        if ScenarioList!=[]:
            ScenProb={scen:prob for scen,prob in ScenProb.items() if scen in ScenarioList}

        fig=_go.Figure()
        fig.add_scatter(y=list(ScenProb.values()),mode='lines',marker=dict(color='red'),line=dict(color='blue'),
                        hoverinfo='text',
                        hovertext=[f'Scenario Name = {key}<br>Probability = {val}' for key,val in ScenProb.items()],
                        hoverlabel=dict(bgcolor='gray',font=dict(size=14,color='yellow')))

         #set range for lof type
        yaxisrange=None
        if yaxistype=='log':
            miny=min(list(ScenProb.values()))
            miny=int(_math.log10(miny))-1
            yaxisrange=[miny,0]              #in log type plotly consider the entered values as power of ten

        fig.update_layout(yaxis=dict(type=yaxistype,showline=True, linecolor='black',linewidth=2,title='Probability',titlefont=dict(family='Balto', size=16, color='black'),range=yaxisrange),#type['-', 'linear', 'log', 'date', 'category','multicategory']
                        xaxis=dict(type='linear',showline=True, linecolor='black',linewidth=2,title='Scenario',titlefont=dict(family='Balto', size=16, color='black'),),
                        plot_bgcolor='white', )
        if height!=None:
            fig.update_layout(height=height)
        if width!=None:
            fig.update_layout(width=width)        

        if PlotMode==3:
        
            return _iplot(fig)
            
        elif PlotMode==2:
            
            image_filename='ScenarioProbability.html'
            _plot(fig,filename=image_filename)
            
        else:
            fig.show()
        # fig.update_xaxes(dict(zerolinecolor="black",
        #                       title='x',
        #                       titlefont=dict(family='Balto', size=18, color='black'),
        #                             ))
        # fig.update_yaxes(dict(zerolinecolor="black",
        #                       title='y',
        #                       titlefont=dict(family='Balto', size=18, color='black'),
        #                             ))
        
            
                
            
            
        
        
        
        
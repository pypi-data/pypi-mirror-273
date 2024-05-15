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
 
 Revision: 4/30/2024
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


class ObjsRecorderPP():


    def __init__(self,ObjsRecorer_filename='',Number_Of_LOC_Histogram_Bins=100):
        
        
        
        
        files=_os.listdir()
        
        #If user didn't define any file or file doesn't exist
        if ObjsRecorer_filename=='':
            raise ValueError('No file has been defined or .Log or .OPR file not found!')

        if ObjsRecorer_filename+'.Log' not in files:
            raise ValueError(f'{ObjsRecorer_filename+".Log"} not found and not loaded!')

        if ObjsRecorer_filename+'.OPR' not in files:
            raise ValueError(f'{ObjsRecorer_filename+".OPR"} not found and not loaded!')
            return -1  
            
        self.ObjsRecorer_filename=ObjsRecorer_filename
        self.Number_Of_LOC_Histogram_Bins=Number_Of_LOC_Histogram_Bins
        
        #Get Total Number of Analysis
        self.TotalScenario=_opr.Recorders.Objs_recorder_loader.TotalNumberOfAnalysis(ObjsRecorer_filename)
        
        #Get number of scenarios
        NumberOfScenarios=_opr.Recorders.Objs_recorder_loader.TotalNumberOfScenarios(ObjsRecorer_filename)

        #Load other subpackages that are not recorded by user
        _opr.Recorders.Objs_recorder_loader.LoadOtherSubPackages(ObjsRecorer_filename)

        #Define variables
        self.DamagedLevelListVar=[]     #list of the plant units Damage level list, each value is a Dictionary of Damage level of the plant units for each recorded scenario
        self.FragilityTagListVar=[]     #List of the plant units happend fragility tag Dictionaries, 
        self.LOCListVar=[]              #List of the PlantUnits tag and max Loss of Containment value Dictionary
        self.NodesGroupDamageListVar=[] #List of NodesGroup isDamaged Dict, each Dictionary is NodesGroupTag and corresponding Damagelist
        self.HazardMagnitudeVar=[]      #List of the hazard tags and magnitudes (tag as key and magnitude as value)
        self.NodesGroupRadiationList=[]     #list of NodesGroup Radiation Data, key: NodesGroup tag and value:Radiation Value (Just to get data)
        self.NodesGroupOverPressureList=[]  #list of NodesGroup OverPressure List, key: NodesGroup tag and value:Radiation Value
        self.NodesGroupOVPProbitList=[]
        self.NodesGroupRadProbitList=[]        

        #Star Opening all recorded files to export data
        for scenariotag in range(1,NumberOfScenarios+1):

            #Load Scenario
            _opr.Recorders.Objs_recorder_loader.load1ScenarioItt(scenariotag, ObjsRecorer_filename)

            #Fill variables for loaded scenario
            self.DamagedLevelListVar.append({i.tag:i.DamageLevel for i in _opr.PlantUnits.ObjManager.Objlst})
            self.FragilityTagListVar.append({i.tag:i.DamageFragilityTag for i in _opr.PlantUnits.ObjManager.Objlst})
            self.LOCListVar.append({i.tag:(i.OutFlowModelObject.TotalMassLiquid_Release if i.OutFlowModelObject!=None else None) for i in _opr.PlantUnits.ObjManager.Objlst})
            self.NodesGroupDamageListVar.append({NG.tag:([(0 if i==False else 1) for i in NG.isDamagedList] if NG.isDamagedList!=[] else [0]*len(NG.xGlobalList)) for NG in _opr.NodesGroups.ObjManager.Objlst})
            self.NodesGroupRadiationList.append({NG.tag:NG.Radiation_Intensity for NG in _opr.NodesGroups.ObjManager.Objlst} )
            self.NodesGroupOverPressureList.append({NG.tag:NG.OverPressure_Intensity for NG in _opr.NodesGroups.ObjManager.Objlst})
            self.NodesGroupOVPProbitList.append({NG.tag:NG.OverPressure_Probit for NG in _opr.NodesGroups.ObjManager.Objlst})
            self.NodesGroupRadProbitList.append({NG.tag:NG.Radiation_Probit for NG in _opr.NodesGroups.ObjManager.Objlst})
            self.HazardMagnitudeVar.append({i.tag:(i.SampledMagnitude) for i in _opr.Hazard.ObjManager.Objlst})

        #Modify LOCList to maximum loss value or 0
        self.LOCListVar=[{tag:(max(loss) if loss!=None else 0) for tag,loss in LossDic.items()} for LossDic in self.LOCListVar]
        
        
    def DamagedLevelList(self):
        return self.DamagedLevelListVar
        
    def FragilityTagList(self):
        return self.FragilityTagListVar
        
    def LOCList(self):
    
                
        return self.LOCListVar
      
    def NodesGroupDamageList(self):
        return self.NodesGroupDamageListVar
    
    def NodesGroupTypeDict(self):
     
        #NodesGroupTypeDict Dictionray of each NodesGroup object that keys are tag of nodes group and values are the type of the nodes group
        NodesGroupTypeDictVar={NG.tag:NG.Type for NG in _opr.NodesGroups.ObjManager.Objlst}    
        
        return NodesGroupTypeDictVar

    def NodesGroupDamageProbability(self):
        
        NodesGroupDamProb={}    #Dictionray of each NodesGroup object that keys are tag of nodes group and values are the probability of their damage

        #----NodesGroupDamProb calculate each nodesgroup damage probability at each node
        #calculate nodesgroup tag and number of the nodes
        NodesGroupDamageList=[i for i in self.NodesGroupDamageList() if i!={}]
        
        for NG in NodesGroupDamageList:
            
            NGtag=list(NG.keys())[0]

            #If nodes not in the NodesGroupDamProb add it as new and if is, add values to its values
            if NGtag not in list(NodesGroupDamProb.keys()):
                NodesGroupDamProb[NGtag]=NG[NGtag]
            else:
                NodesGroupDamProb[NGtag]=[i+j for i,j in zip(NodesGroupDamProb[NGtag],NG[NGtag])]

        #convert to expected Value
        for NG in NodesGroupDamProb.keys():
            NodesGroupDamProb[NG]=[i/self.TotalScenario for i in NodesGroupDamProb[NG]]    
        
        return NodesGroupDamProb
        
    def TotalLOCList(self):
        
        #----Probability of Loss of Containment 
        ListOfLoc=[sum(list(LOCDIC.values())) for LOCDIC in self.LOCList()]
        
        return ListOfLoc
        
    def LOC_bins_hist_probloc(self):
    
        minLoc=min([i for i in self.TotalLOCList() if i!=0])
        maxLoc=max([i for i in self.TotalLOCList() if i!=0])
        nbins=self.Number_Of_LOC_Histogram_Bins
        hist, bins=_np.histogram(self.TotalLOCList(),bins=[minLoc+(maxLoc-minLoc)/nbins*i for i in range(nbins+1)]) #length of the bins always should be one more than length of the hist
        probloc=[i/self.TotalScenario for i in hist] 

        
        return [bins,hist,probloc]
        
    def Damagelevel_eLOC(self):
        DmglvlLOC={}   #Damagelevel and corresponding expected loss of containment
        
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
    
        UnitsZeroDamageProbVar={}  #Probability of each PlantUnit zero level damage
        
        #Calculate some probabilities from above results
        #------ Probability of Units Zero Level Damage
        UnitsZeroDamageProbVar={obj.tag:0 for obj in _opr.PlantUnits.ObjManager.Objlst}
        for DamLevelDict in self.DamagedLevelList():
            for tag,DamLev in DamLevelDict.items() :
                if DamLev==0: UnitsZeroDamageProbVar[tag]=UnitsZeroDamageProbVar[tag]+1

        #convert to probability
        UnitsZeroDamageProbVar={tag:DamLev/self.TotalScenario for tag,DamLev in UnitsZeroDamageProbVar.items()}    
    
        return UnitsZeroDamageProbVar
        
    def ProbOfFragilities(self):
        ProbOfFragilitiesVar={}    #Probability of each fragility or probit happening or governing

        #------ Probability of happening Fragilities and probits
        ProbOfFragilitiesVar={obj.tag:0 for obj in _opr.Fragilities.ObjManager.Objlst}
        for FragDict in self.FragilityTagList():
            for Fragtag in FragDict.values() :
                if Fragtag!=None: ProbOfFragilitiesVar[Fragtag]=ProbOfFragilitiesVar[Fragtag]+1

        #convert to probability
        ProbOfFragilitiesVar={tag:Num/self.TotalScenario for tag,Num in ProbOfFragilitiesVar.items()}
        
        return ProbOfFragilitiesVar
        
    def ScenariosAnalyzeNumbers(self):
        
        #------ Probability of Damage levels and scenarios and subscenarios and Scenarios analyze number
        Results={}                    #Store scenario and number of happening (ScenariosProbability)
        ScenariosAnalyzeNumbersVar={} #Store scenario(key)  and number of alnazed scenarios list (Value)
        DamlvlScenDict=self.Damagelevel_Scenario_Dict()             #Dictionary of damage level (key) and corresponding Scenarios set (Value)
        for ScenarioNum,damagelistrow in enumerate(self.DamagedLevelList()):
            LevelList=ObjsRecorderPP._LevelList(damagelistrow)
            LevelList=['-'.join(LevelList[:i])  for i in range(1,len(LevelList)+1)]

            #Fill Results for ScenariosProbability
            if LevelList!=[]: 
                
                for i in  LevelList:
                    if i not in Results.keys():
                        Results[i]=1
                    else:
                        Results[i]=Results[i]+1
            
            #Fill Results for ScenariosProbability
            if LevelList!=[]: 
                i=LevelList[-1]
                if i not in ScenariosAnalyzeNumbersVar.keys():
                    ScenariosAnalyzeNumbersVar[i]=[ScenarioNum]
                else:
                    ScenariosAnalyzeNumbersVar[i].append(ScenarioNum)
        
        return ScenariosAnalyzeNumbersVar
        
    def ScenariosProbability(self):

        #------ Probability of Damage levels and scenarios and subscenarios and Scenarios analyze number
        Results={}                    #Store scenario and number of happening (ScenariosProbability)
        DamlvlScenDict=self.Damagelevel_Scenario_Dict()             #Dictionary of damage level (key) and corresponding Scenarios set (Value)
        for ScenarioNum,damagelistrow in enumerate(self.DamagedLevelList()):
            LevelList=ObjsRecorderPP._LevelList(damagelistrow)
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

        #------ Probability of Damage levels and scenarios and subscenarios and Scenarios analyze number
        Results={}                    #Store scenario and number of happening (ScenariosProbability)
        DamlvlScenDict=self.Damagelevel_Scenario_Dict()             #Dictionary of damage level (key) and corresponding Scenarios set (Value)
        for ScenarioNum,damagelistrow in enumerate(self.DamagedLevelList()):
            LevelList=ObjsRecorderPP._LevelList(damagelistrow)
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

        DamlvlScenDict={}             #Dictionary of damage level (key) and corresponding Scenarios set (Value)
        for ScenarioNum,damagelistrow in enumerate(self.DamagedLevelList()):
            LevelList=ObjsRecorderPP._LevelList(damagelistrow)
            LevelList=['-'.join(LevelList[:i])  for i in range(1,len(LevelList)+1)]
            #fill DamlvlScenDict
            for lvl,name in enumerate(LevelList):
                if lvl not in DamlvlScenDict.keys():
                    DamlvlScenDict[lvl]=set([name])
                else:
                    DamlvlScenDict[lvl].update([name])        
        
        return DamlvlScenDict
        
    def HazardMagnitude(self):
    
        return self.HazardMagnitudeVar
        
    def ScenarioName_DamageLevel_Dict(self):
        ScenNameDamLvlDict={}   #Dictionary that its key is Scenario name and the value is its corresponding Damage level Dictionary
        
        for dmlvl in self.DamagedLevelList():
            ScenNameDamLvlDict["-".join(ObjsRecorderPP._LevelList(dmlvl))]=dmlvl    
            
        return ScenNameDamLvlDict
        
    def NodesGroupRadiationDict(self):
    
        NodesGroupRadiationAveDict={}  #Dictionary of NodesGroup Radiation Data, and keys is Nodes Group tag and value is the list of Radiation values Average 
        
        #Modify NodesGroup Radiation and overpressure Dictionaries in better format
        NodesGroupRadiationAveDict={NG.tag:[0 for i in NG.xGlobalList] for NG in _opr.NodesGroups.ObjManager.Objlst}
        
        #sum values
        for Dict in self.NodesGroupRadiationList:
            for NGtag in Dict.keys():
                NodesGroupRadiationAveDict[NGtag]=[i+j for i,j in zip(Dict[NGtag],NodesGroupRadiationAveDict[NGtag])]
        
        #Convert above values to average
        for NGtag in NodesGroupRadiationAveDict.keys():
            NodesGroupRadiationAveDict[NGtag]=[i/self.TotalScenario for i in NodesGroupRadiationAveDict[NGtag]]
            
        return NodesGroupRadiationAveDict
        
    def NodesGroupOverPressureDict(self):
        
        NodesGroupOverPressureAveDict={}  #Dictionary of NodesGroup OverPressure Data, and keys is Nodes Group tag and value is the list of OverPressure values Average
        
        #Modify NodesGroup Radiation and overpressure Dictionaries in better format
        NodesGroupOverPressureAveDict={NG.tag:[0 for i in NG.xGlobalList] for NG in _opr.NodesGroups.ObjManager.Objlst}

        #sum values
        for Dict in self.NodesGroupOverPressureList:
            for NGtag in Dict.keys():
                NodesGroupOverPressureAveDict[NGtag]=[i+j for i,j in zip(Dict[NGtag],NodesGroupOverPressureAveDict[NGtag])]     

        #Convert above values to average
        for NGtag in NodesGroupOverPressureAveDict.keys():
            NodesGroupOverPressureAveDict[NGtag]=[i/self.TotalScenario for i in NodesGroupOverPressureAveDict[NGtag]]
            
        return NodesGroupOverPressureAveDict
        
    def NodesGroup_OVP_Probit_Dict(self):
        NodesGroupOVPProbAveDict={}     #Dictionary of NodesGroup OverPressure corresponding Probit Data, and keys is Nodes Group tag and value is the list of Probit(OverPressure) values Average 
        
        #Modify NodesGroup Radiation and overpressure Dictionaries in better format
        NodesGroupOVPProbAveDict={NG.tag:[0 for i in NG.xGlobalList] for NG in _opr.NodesGroups.ObjManager.Objlst}

        #sum values
        for Dict in self.NodesGroupOVPProbitList:
            for NGtag in Dict.keys():
                NodesGroupOVPProbAveDict[NGtag]=[i+j for i,j in zip(Dict[NGtag],NodesGroupOVPProbAveDict[NGtag])]

        #Convert above values to average
        for NGtag in NodesGroupOVPProbAveDict.keys():
            NodesGroupOVPProbAveDict[NGtag]=[i/self.TotalScenario for i in NodesGroupOVPProbAveDict[NGtag]]
            
        return NodesGroupOVPProbAveDict

    def NodesGroup_Rad_Probit_Dict(self):
        NodesGroupRadProbAveDict={}     #Dictionary of NodesGroup Radiation Probit Data, and keys is Nodes Group tag and value is the list of Probit(Radiation) values Average
        
        #Modify NodesGroup Radiation and overpressure Dictionaries in better format
        NodesGroupRadProbAveDict={NG.tag:[0 for i in NG.xGlobalList] for NG in _opr.NodesGroups.ObjManager.Objlst}

        #sum values
        for Dict in self.NodesGroupRadProbitList:
            for NGtag in Dict.keys():
                NodesGroupRadProbAveDict[NGtag]=[i+j for i,j in zip(Dict[NGtag],NodesGroupRadProbAveDict[NGtag])]        

        #Convert above values to average
        for NGtag in NodesGroupRadProbAveDict.keys():
            NodesGroupRadProbAveDict[NGtag]=[i/self.TotalScenario for i in NodesGroupRadProbAveDict[NGtag]]
            
        return NodesGroupRadProbAveDict


    @staticmethod    
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
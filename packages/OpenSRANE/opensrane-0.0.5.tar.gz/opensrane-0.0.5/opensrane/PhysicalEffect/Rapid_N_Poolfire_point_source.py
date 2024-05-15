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
 Created: 3/20/2024
 
 Revision: -
 By & Date: -
'''


#This is a Sample File and any new Model is better to be constructed by a copy of this file
from opensrane.Misc._NewClass import _NewClass
from .ObjManager import *
from opensrane.Misc.WarningRecorder import *
from ._GlobalParameters import _GlobalParameters
import math as _math
import random as _rnd
import opensrane as _opr

class Rapid_N_Poolfire_point_source(_NewClass,_GlobalParameters):
    
    '''
    In this module, fire point source according to documentation of Rapid-N is modeled.
    THIS model is just for POOL FIRE and for other type of fires will not work!
    
    Source: https://publications.jrc.ec.europa.eu/repository/bitstream/JRC130323/JRC130323_01.pdf Equation (8)
    
    Radiative_Fraction=Radiative Fraction of heat of combustion, This value will modify the heat of combustion of material. This factor will be multiply in specific heat of combustion of material or substace.
    '''
    Title='Rapid-N Fire Point Source Physical Effect'
    
    def __init__(self,tag,Radiative_Fraction=1):
        
        #---- Fix Part for each class __init__ ----
        ObjManager.Add(tag,self)
        _NewClass.__init__(self,tag)
        #------------------------------------------
        
        
        _GlobalParameters.__init__(self)
        
        
        
        self.R=Radiative_Fraction
        self.wipeAnalysis()
    
    def wipeAnalysis(self):
        # properties that are defined in _GlobalParameters should also be reset
        self.wipeAnalysisGlobal()
        
        # properties that are not constant and among each analysis will change should be define here
        pass
        
    @property
    def name(self):    
        return f'Rapid-N Fire Point Source Physical Effect for unit with tag {self.UnitObject.tag} ' if self.UnitObject!=None else 'Fire Point Source Physical Effect But still No Plant unit is assigned to it'
        

    def Thermal_Radiation_at_Point(self,x,y,z):
        #This function calculate the thermal radiation in point x,y (Rapid-N model do not consider vertical direction and only considers horizontal distance
        
        UnitObject=self.UnitObject #self.UnitObject has been defined in _GlobalParameters
        if UnitObject==None:         
            warning('(Rapid-N PoolFire_Point_Source) Because of no assigned plant unit, module will not do any calculations')
            return None
        
        PoolRadius=UnitObject.DispersionSpreadModelObject.LiquidRadious
        PoolCenter=UnitObject.DispersionSpreadModelObject.LiquidCenter
        if PoolRadius==None or PoolCenter==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because of pool radius or pool center is None so pool fire does not exist and no calculations has done!')
            return None
        Xcp,Ycp=PoolCenter[-1]
        Apool=PoolRadius[-1]**2*_math.pi
        
        SiteObject=_opr.Sites.ObjManager[UnitObject.SiteTag]
        if SiteObject==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because of No site tag has been defined for metioned Plant unit Object')
            return None 
            
        Ta=SiteObject.Temperature #Site Temperature or air Temperature
        if Ta==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because of Ambient Temperature (Ta) or Site Humidity (Hr) has not been defined for the site with tag{UnitObject.SiteTag}')
            return None
        
    
        #Get Substance that is assigned to the unit Object
        SubstanceObject=_opr.Substance.ObjManager[UnitObject.SubstanceTag] if UnitObject.SubstanceTag!=None else None
        if SubstanceObject==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because of No substance is defined for the mnetioned Plant unit Object')
            return None  

        
        Hc=SubstanceObject.Specific_Heat_of_Combustion          #heat of combustion of the pool substance )j/kg
        Hv=SubstanceObject.Specific_Heat_of_Vaporization        #heat of vaporization of the pool substance j/kg
        Cp=SubstanceObject.Specific_Heat_Capacity               #heat capacity of the pool substance j.K/kg
        Tb=SubstanceObject.Boiling_Point                        #Boiling point of the pool substance K
        if Hc==None or Hv==None or Cp==None or Tb==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because for its substance with tag {UnitObject.SubstanceTag} Specific_Heat_of_Combustion or Specific_Heat_of_Vaporization or Specific_Heat_Capacity or Boiling_Point has not been defined')
            return None
        
        #Modify heat of combustion by multipling in Radiative_Fraction
        Hc=Hc*self.R
        
        D=((x-Xcp)**2+(y-Ycp)**2)**0.5         #Horizontal distance from pool center
        
        

        
        return Hc**2*0.4*0.001*Apool**2/4/_math.pi/D**2/(Hv+Cp*(Tb-Ta))
        

   
    def RadiationBoundary(self,Radiation,Height,PointNumber):
        
        
        #This function returns N PointNumber location that have equal radiation value (Radiation) at z=Height
        Resluts={}
        
        z=Height
        N=PointNumber
        q=Radiation
        
        UnitObject=self.UnitObject #self.UnitObject has been defined in _GlobalParameters
        if UnitObject==None:         
            warning('(Rapid-N PoolFire_Point_Source) Because of no assigned plant unit, module will not do any calculations')
            return None
        
        PoolRadius=UnitObject.DispersionSpreadModelObject.LiquidRadious
        PoolCenter=UnitObject.DispersionSpreadModelObject.LiquidCenter
        if PoolRadius==None or PoolCenter==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because of pool radius or pool center is None so pool fire does not exist and no calculations has done!')
            return None
        Xcp,Ycp=PoolCenter[-1]
        Apool=PoolRadius[-1]**2*_math.pi
        
        SiteObject=_opr.Sites.ObjManager[UnitObject.SiteTag]
        if SiteObject==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because of No site tag has been defined for metioned Plant unit Object')
            return None 
            
        Ta=SiteObject.Temperature #Site Temperature or air Temperature
        if Ta==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because of Ambient Temperature (Ta) or Site Humidity (Hr) has not been defined for the site with tag{UnitObject.SiteTag}')
            return None
        
    
        #Get Substance that is assigned to the unit Object
        SubstanceObject=_opr.Substance.ObjManager[UnitObject.SubstanceTag] if UnitObject.SubstanceTag!=None else None
        if SubstanceObject==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because of No substance is defined for the mnetioned Plant unit Object')
            return None  

        
        Hc=SubstanceObject.Specific_Heat_of_Combustion          #heat of combustion of the pool substance )j/kg
        Hv=SubstanceObject.Specific_Heat_of_Vaporization        #heat of vaporization of the pool substance j/kg
        Cp=SubstanceObject.Specific_Heat_Capacity               #heat capacity of the pool substance j.K/kg
        Tb=SubstanceObject.Boiling_Point                        #Boiling point of the pool substance K
        if Hc==None or Hv==None or Cp==None or Tb==None:
            warning(f'(Rapid-N PoolFire_Point_Source) for Plant unit {UnitObject.tag} because for its substance with tag {UnitObject.SubstanceTag} Specific_Heat_of_Combustion or Specific_Heat_of_Vaporization or Specific_Heat_Capacity or Boiling_Point has not been defined')
            return None
            
        #Modify heat of combustion by multipling in Radiative_Fraction
        Hc=Hc*self.R

        R=D=Hc*(0.4*0.001*Apool/4/_math.pi/q/(Hv+Cp*(Tb-Ta)))**0.5
        
        Phi=[i*2*_math.pi/N for i in range(N)]

        for phi in Phi:

            x=Xcp+R*_math.cos(phi)
            y=Ycp+R*_math.sin(phi)
            Resluts[phi]=(x,y)
   
        return Resluts
            
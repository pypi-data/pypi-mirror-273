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
 Created: 12/23/2023
 
 Revision: -
 By & Date: -
'''


from opensrane.Misc._NewClass import _NewClass
from .ObjManager import *
from ._GlobalParameters import _GlobalParameters
import math as _math
from opensrane.Misc.WarningRecorder import *


class SphericalTank(_NewClass,_GlobalParameters):
    '''
    Above Ground Spherical Tank
    '''
    Title="Above Ground Spherical Tank"
    
    def __init__(self,tag,SiteTag=None,DikeTag=None, SafetyTag=None, SubstanceTag=None, FragilityTagNumbers=None,
                      Horizontal_localPosition=0,Vertical_localPosition=0, Surface_Roughness=None,
                      Pressure=0,Temperature=0, SubstanceVolumeRatio=None,
                      Diameter=None,Botton_Point_Height=None,
                      GroundTemperature=None,Ks_Soil_Thermal_conductivity=None,Alphas_Soil_thermal_diffusivity=None,
                      boundary_points_Number=20,Number_of_boundary_points_height_levels=10,
                      pressure_probit_tag=None, radiation_probit_tag=None, RadiationDifferenceDose=1000):
         
        #---- Fix Part for each class __init__ ----
        ObjManager.Add(tag,self)
        _NewClass.__init__(self,tag)
        #------------------------------------------
        
        _GlobalParameters.__init__(self,SiteTag,GroundTemperature,Ks_Soil_Thermal_conductivity,Alphas_Soil_thermal_diffusivity, pressure_probit_tag,
                                        radiation_probit_tag,Horizontal_localPosition,Vertical_localPosition,Pressure,Temperature,
                                        FragilityTagNumbers,SubstanceTag,SafetyTag,Surface_Roughness,RadiationDifferenceDose)
        
        
        self.DikeTag=DikeTag
        #Check For error Message if Containment tag Number is not defined before---
        #------------------------------------------------------------------------
        
        
        
        self.d_Storage=Diameter
        self.h_Botton=Botton_Point_Height
        

        
        if self.d_Storage==None or self.h_Botton==None:
            warning(f'ِ(SphericalTank) Diameter or height from bottom of spherical tank with tag {tag} Has not been defined By the user'+
                  f'So the code do not calculate any thing for this Plant Unit')
            pass
        else:
            self.V_unit=_math.pi*4/3*(self.d_Storage/2)**3 #The Total Object(SphericalTank) Volume
            
        if SubstanceVolumeRatio==None or self.V_unit==None:
            pass
        else:
            if SubstanceVolumeRatio<0:SubstanceVolumeRatio=0
            if SubstanceVolumeRatio>1:SubstanceVolumeRatio=1
            self.V_subs=self.V_unit*SubstanceVolumeRatio     #The Total Object(Tank) Containment Volume

        
        self.name=f'(SphericalTank) Above Ground Spherical Tank {tag} with dimeter ={Diameter} and height from bottom={Botton_Point_Height} and substance tag {SubstanceTag}'
        
        self.boundary_points_Number=boundary_points_Number   #Number of boundary points 
        self.Number_of_boundary_points_height_levels=Number_of_boundary_points_height_levels # number of levels that will be consider for boundary points


        self.wipeAnalysis()
    
    def wipeAnalysis(self):
        # properties that are defined in _GlobalParameters should also be reset
        self.wipeAnalysisGlobal()
        
        # properties that are not constant and among each analysis will change should be define here
        pass
        
        
    @property
    def boundary_points(self):
        N=int(self.boundary_points_Number)
        Nh=int(self.Number_of_boundary_points_height_levels)
        h0=self.h_Botton
        x0=self.Hlocalcoord
        y0=self.Vlocalcoord
        if self.d_Storage==None: return None
        R=self.d_Storage/2
        
        Hi=[n/Nh*2*R for n in range(Nh+1)]         #list of heights or levels from bottom of the tank (Not from ground level)]
        RH=[(R**2-(R-hi)**2)**0.5 for hi in Hi]    #list of radius of each height or level
        Phi=[i/N*2*_math.pi for i in range(N)]     #list of angles of points at each level (For all levels we have similar number or points and 
        
        result=[]
        for h,r in zip(Hi,RH):
            result.extend([(x0+r*_math.cos(phi),y0+r*_math.sin(phi),h+h0) for phi in Phi])
        
        return result
        
        
        
    #This Function is needed for ZeroLevel Analysis so Any new     
    def _isSimilar(self,Obj):
    
        '''
        This Function Sould be Availble in all PlantUnit Classes
        and it shows if Other PlantUnit Object is similar to This Object
        And the Rule of similarity are as below code.
        This similarity is used in Zerolevel Analysis to Distinguish 
        Similar Objects.
        Attention, The input Should be an PlantUnit Object
        '''
        
        if self.__class__!=Obj.__class__:
            return False
        if self.d_Storage!=Obj.d_Storage:
            return False
        if self.h_Storage!=Obj.h_Storage:
            return False
        
        return True
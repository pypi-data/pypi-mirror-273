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


class _GlobalParameters():
    '''
    In this Global Parameters that any plant unit should have and the other 
    Classes and functyions and ... use them
    '''

    
    def __init__(self):

        self.wipeAnalysis()
                
    def wipeAnalysisGlobal(self):      
        #The below variables are for storing samples data. When GetRandomWindِSample a sample create, Code should store it in the below variables
        self.WindClass=None
        self.WindDirection=None
        self.WindSpeed=None
        self.AlphaCOEF=None
        self.isCalmn=False
        
    def wipeAnalysis(self):
        self.wipeAnalysisGlobal()
        pass         
        
    @property
    def GetRandomWindِSample(self):
        
        self.WindClass=None
        self.WindDirection=None
        self.WindSpeed=None
        self.AlphaCOEF=None
        self.isCalmn=False
        
        return {'WindClass':self.WindClass, 'WindDirection':self.WindDirection,'WindSpeed':self.WindSpeed, 'AlphaCOEF':self.AlphaCOEF, 'isCalmn':self.isCalmn}
        
 

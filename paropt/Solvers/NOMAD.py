import sys
import os

from ..core.solver import Solver
from ..core import utility
#from ..core.blackbox import BlackBox as BB

class Parameter:
    def __init__(self,name=None,value=None,**kwargs):
        self.name = name
        self.value = value
        pass
    
    def str(self):
        if (self.name is not None) and (self.value is not None):
            return self.name + ' ' + str(self.value)
        return ""
    

class NOMADSolver(Solver):
    def __init__(self,**kwargs):
        Solver.__init__(self,name='NOMAD',command='nomad',parameter='nomad-param.txt',**kwargs)
        self.paramFileName = 'nomad-param.txt'
        self.resultFileName = 'nomad-result.txt'
        self.solutionFileName = 'nomad-solution.txt'
        self.parameter_settings = [] # List of line in parameter file
        pass

    def read_input(self,argv):
        inputValues = []
        if len(argv) < 1:
            return inputValues
        inputFile = open(argv[1],'r')
        inputValues = utility.readwords(inputFile)
        inputFile.close()
        return inputValues

    def write_output(self,objectiveValue,constraintValues):
        print >> sys.stdout, objectiveValue,
        if len(constraintValues) > 0:
            for i in range(len(constraintValues)):
                print >> sys.stdout,constraintValues[i],
            print ""
        return
    
    def initialize(self,blackbox):
        descriptionFile = open(self.paramFileName,"w")
        descriptionFile.write('DIMENSION ' + str(blackbox.nVar) + '\n')
        descriptionFile.write('DISPLAY_DEGREE 4\n')
        descriptionFile.write('DISPLAY_STATS EVAL& BBE & SOL&  &OBJ \\\\ \n')
        #descriptionFile.write('BB_EXE "$python ' + self.executableFileName + '"\n')
        descriptionFile.write('BB_EXE ' + blackbox.executableFileName + '\n')
        bbTypeStr = 'BB_OUTPUT_TYPE OBJ'
        for i in range(blackbox.mCon):
            bbTypeStr = bbTypeStr + ' PB'
        descriptionFile.write(bbTypeStr + '\n')
        descriptionFile.write('SOLUTION_FILE ' + self.solutionFileName + '\n')
        pointStr = str(blackbox.initialPoint)
        descriptionFile.write('X0 ' +  pointStr.replace(',',' ') + '\n')
        descriptionFile.write('STATS_FILE ' + self.resultFileName + ' EVAL& BBE & BBO & SOL&  &OBJ \\\\ \n')
        for param_setting in self.parameter_settings:
            descriptionFile.write(param_setting + '\n')
        descriptionFile.close()
        return

    def set_parameter(self,name=None,value=None):
        #descriptionFile = open(self.paramFileName,'a')
        #descriptionFile.write(param.str() + '\n')
        #descriptionFile.close()
        param = Parameter(name=name,value=value)
        self.parameter_settings.append(param.str())
        return

NOMAD = NOMADSolver()

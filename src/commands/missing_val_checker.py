import pandas as pd
from uploading_command import UploadingCommand
import sys
sys.path.append("../temhelp")
from template_handler import TemplateHandler

class MissingValChecker(UploadingCommand):

    def __init__(self, template_name):
        ''' (MissingValChecker, Dataframe, TemplateHandler) -> None
        
        Initializes a MissingValChecker object with it's dataframe to
        parse and TemplateHandler to reference
        '''
        UploadingCommand.__init__(self, template_name);
        

    def execute(self, df):
        ''' (MissingValChecker, DataFrame) -> List of [Tuple of (String, int)]
        
        Given a MissingValChecker object parses the DataFrame and returns
        a tuple of all empty mandatary fields as in the TemplateHandle
        
        If an entire column is missing, row will be set to -1
        Row is 0 indexed
        '''
        self._exec_status = 0;
        mandatory_headers = self._template_name.get_mandatary_headers()
        missing_fields = []
        
        # loop through all mandatory_headers
        for header in mandatory_headers:
            column = df.get(header)
            # if the mandatory column is in the DataFrame
            if column is not None:
                # loop through all fields
                for row in range(len(df.index)):
                    if (df.get(header)[row].isnull()):
                        # add any empty fields to missing_fields
                        missing_fields.append([header, row])
            # if the mandatory column is not in the DataFrame
            else:
                # add the entire column to missing_fields
                missing_fields.append([header, -1])
        
        # if method reaches here, it executed properly
        self._exec_status = 1;
        
        return missing_fields
    
    def executed_properly(self):
        '''
        (Command) -> boolean

        Returns a boolean to determine if this command was executed properly
        '''
        return self._exec_status
    
mv = MissingValChecker("hello")
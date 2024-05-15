class CameraMeta():

    def __init__(self):
        '''
  string serialNumber = 1;
  string modelName = 2;
  string manufactureName = 3;
  string deviceVersion = 4;
  string userDefinedName = 5;
  map<string, string> info = 6;
        '''

        self.cameraType = ""
        self.serialNumber = ""
        self.modelName = ""
        self.manufactureName = ""
        self.deviceVersion = ""
        self.userDefinedName = ""
        self.info = {}

    def add_info(self, k: str, v: str):
        if self.info is None:
            self.info = {}

        self.info[k] = v

    def get_sn(self):
        return self.serialNumber


from altunityrunner.commands.base_command import BaseCommand
import time
import base64
class GetPNGScreenshot(BaseCommand):

    def __init__(self, socket,request_separator,request_end,path):
        super().__init__(socket,request_separator,request_end)
        self.path=path
    
    def execute(self):
            response=self.send_data(self.create_command('getPNGScreenshot'))
            screenshot_data=""
            if(response=="Ok"):
                screenshot_data=self.recvall(print_output=False)
                screenshot_data_bytes=base64.b64decode(screenshot_data)
                f =open(self.path,'wb')
                f.write(screenshot_data_bytes)
                f.close()

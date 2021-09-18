from altunityrunner.commands.base_command import BaseCommand
class Drag(BaseCommand):
    def __init__(self, socket,request_separator,request_end,x,y,alt_object):
        super(Drag, self).__init__(socket,request_separator,request_end)
        self.x=x
        self.y=y
        self.alt_object=alt_object
    
    def execute(self):
        position_string = self.vector_to_json_string(self.x, self.y)
        data = self.send_data(self.create_command('dragObject', position_string, self.alt_object))
        return self.handle_errors(data)

import datetime
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

class WorkPlugin(WillPlugin):

    @respond_to("^working on (?P<task>.*)$")
    def working_on(self, message, task):
        """working on ___ : Announce the task you are working on."""
        if task:
            current_tasks = self.load("current_tasks", {})
            current_task = current_tasks[message.sender.nick]
            if current_task:
                pass
            current_tasks[message.sender.nick] = {
                "name": message.sender.name,
                "date": datetime.datetime.now(),
                "task": task,
            }
            self.save("current_tasks", current_tasks)
            self.say("okay", message=message)

    @respond_to("^work status\?$")
    def work_status(self, message):
        current_tasks = self.load("current_tasks", {})
        current_task = current_tasks[message.sender.nick]
        if current_task:
            self.say("""you are working on: {task}
since: {date}""".format(task=current_task['task'], date=current_task['date']), message=message)
        else:
            self.say("no task", message=message)


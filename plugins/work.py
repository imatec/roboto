import datetime
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

class WorkPlugin(WillPlugin):

    def current_tasks(self):
        current_tasks = self.load("current_tasks", {})
        return current_tasks if current_tasks else None

    def past_tasks(self):
        past_tasks = self.load("past_tasks", {})
        return past_tasks if past_tasks else None

    def insert_past_task(self, task):
        past_tasks = self.past_tasks() or []
        past_tasks.append(task)
        self.save("past_tasks", past_tasks)

    def update_current_task(self, nick, name, task):
        tasks = self.current_tasks() or {}
        tasks[nick] = {
            "name": name,
            "ini": datetime.datetime.now(),
            "task": task,
        }
        self.save("current_tasks", tasks)

    def end_task(self, nick):
        tasks = self.current_tasks() or {}
        task = tasks.pop(nick, None)
        self.save("current_tasks", tasks)
        if task:
            task["end"] = datetime.datetime.now()
            self.insert_past_task(task)

    @respond_to("^working on (?P<task>.*)$")
    def working_on(self, message, task):
        """working on ___ : Announce the task you are working on."""
        if task:
            self.end_task(message.sender.nick)
            self.update_current_task(message.sender.nick, message.sender.name, task)
            self.say("okay", message=message)

    @respond_to("^not working$")
    def not_working(self, message):
        """not working ___ : Announce you are not working."""
        self.end_task(message.sender.nick)
        self.say("okay", message=message)

    @respond_to("^work status\?$")
    def work_status(self, message):
        current_tasks = self.current_tasks() or {}
        current_task = current_tasks.get(message.sender.nick, None)
        if current_task:
            self.say("""you are working on: {task}
since: {date}""".format(task=current_task['task'], date=current_task['ini']), message=message)
        else:
            self.say("no task", message=message)

    @respond_to("^show past tasks$")
    def show_past_tasks(self, message):
        alltasks = ""
        past_tasks = self.past_tasks() or []
        for task in past_tasks:
            alltasks += str(task)
        self.say("past tasks: {alltasks}".format(alltasks=alltasks), message=message)

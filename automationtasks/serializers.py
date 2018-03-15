from models import automationTasks

from rest_framework import serializers

class tasksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = automationTasks
        fields = (
            "taskId",
            "taskName",
            "taskTypelist",
            "taskDescription",
            "taskRequester",
            "taskProject",
            "taskCIlist",
            "taskConfigvars",
            "taskTicketrequired",
            "taskRundatetime",
            "taskChangeticket",
            "taskAssignee",
            "taskStatus",
            "taskTicketstatus"
        )



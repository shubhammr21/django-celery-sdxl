from core import celery_app


def get_tasks():
    i = celery_app.control.inspect()
    active = i.active()  # tasks that are currently active
    scheduled = i.scheduled()  # tasks that are scheduled
    reserved = i.reserved()  # tasks that have been reserved
    return {"active": active, "scheduled": scheduled, "reserved": reserved}

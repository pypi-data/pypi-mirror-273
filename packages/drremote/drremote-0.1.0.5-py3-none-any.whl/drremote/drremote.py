#!/usr/bin/env python

"""
"""
from .parse import parse_args
import logging
import tempfile
import os
import time

from .get_resolve import GetResolve
from .output import OutputWriter

SUCCESS = 0
ERROR_DATABASE_NOT_FOUND = 1
ERROR_PROJECT_NOT_FOUND = 2
ERROR_TIMELINE_NOT_FOUND = 3
ERROR_NO_CURRENT_PROJECT = 4
ERROR_NO_CURRENT_TIMELINE = 5
ERROR_DAVINIC_DOES_NOT_RESPOND = 6
ERROR_PROJECTMANAGER_NOT_FOUND = 7


def set_current_timeline(project_manager, args, output: OutputWriter) -> int:
    """ function which sets/changes the current Davinci Resolve Timeline

    :param project_manager: Instance of Davinci Resolve ProjectManager
    :param args: The arguments passed from command line
    :param output: Instance of class OutputWriter used for results/error messages
    :return: SUCCESS if successful set the timeline, otherwise an error value (constant of ERROR_*)
    """
    output.logdebug("set_current_timeline: start")

    if args.database:
        current_db = project_manager.GetCurrentDatabase()
        db_list = args.database.split(":")
        # We change only the db when it is necessary (time consuming)
        if current_db["DbName"] != db_list[0]:
            if len(db_list) == 2:
                db_dict = {"DbName": db_list[0], "DbType": db_list[1]}
            else:
                db_dict = {"DbName": db_list[0], "DbType": db_list[1], "IpAddress": db_list[2]}
            if not project_manager.SetCurrentDatabase(db_dict):
                output.error("Database \"" + args.database + "\" could not be found.")
                return ERROR_DATABASE_NOT_FOUND

    project = project_manager.LoadProject(args.project)
    if not project:
        output.error("Project \"" + args.project + "\" could not be found.")
        return ERROR_PROJECT_NOT_FOUND

    timeline_count = project.GetTimelineCount()
    timeline_found = False
    for index in range(0, int(timeline_count)):
        timeline = project.GetTimelineByIndex(index + 1)
        logging.debug("timeline " + str(index + 1) + ": " + timeline.GetName())
        if timeline.GetName() == args.timeline:
            timeline_found = project.SetCurrentTimeline(timeline)
            break
    if not timeline_found:
        output.error("Timeline \"" + args.timeline + "\" could not be found.")
        return ERROR_TIMELINE_NOT_FOUND
    else:
        output.success("Timeline " + args.timeline + " was set successfully.")

    output.logdebug("set_current_timeline: end")
    return SUCCESS


def get_current_timeline(project_manager, output: OutputWriter) -> int:
    """function which writes the timeline IDs (db info, name of project, name of timeline) to output

    :param project_manager: Instance of Davinci Resolve ProjectManager
    :param output: Instance of class OutputWriter used for results/error messages
    :return: SUCCESS if successful set the timeline, otherwise an error value (constant of ERROR_*)
    """
    output.logdebug("get_current_timeline: start")

    project = project_manager.GetCurrentProject()
    if not project:
        output.error("No current project.")
        return ERROR_NO_CURRENT_PROJECT

    timeline = project.GetCurrentTimeline()
    if not timeline:
        output.error("No current timeline.")
        return False
    else:
        db = project_manager.GetCurrentDatabase()
        if len(db) == 2:
            output.success(
                "project=" + project.GetName() + "\ntimeline=" + timeline.GetName() + "\ndatabase=" + db[
                    "DbName"] + ":" + db[
                    "DbType"])
        else:
            output.success(
                "project=" + project.GetName() + "\ntimeline=" + timeline.GetName() + "\ndatabase=" + db[
                    "DbName"] + ":" + db[
                    "DbType"] + ":" + db["IpAddress"])

    output.logdebug("get_current_timeline: end")
    return SUCCESS


# Get currently open project
def main():
    """main function
    Connects to Davinci Resolve and executes the function which were passed by the commandline (argument --mode).
    If Davinci Resolve does not respond, it waits 15 seconds and then retry. Because if an external application started
    Davinci Resolve before calling this Python modul, Davinci Resolve needs sometime to accept request.

    :return: SUCCESS if successful set the timeline, otherwise an error value (constant of ERROR_*)
    """
    logfile = tempfile.gettempdir() + os.path.sep + 'drremote.log'
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    args = parse_args()
    output = OutputWriter(args.output_path)

    output.logdebug("mode=" + args.mode)
    output.logdebug("database=" + str(args.database))
    output.logdebug("project=" + str(args.project))
    output.logdebug("timeline=" + str(args.timeline))
    output.logdebug("output-path=" + str(args.output_path))
    output.logdebug("wait=" + str(args.wait))

    resolve = GetResolve()
    if not resolve and args.wait > 0:
        output.loginfo("Davinci Resolve not available. Wait " + str(args.wait) + " more seconds.")
        time.sleep(args.wait)
        resolve = GetResolve()
    if not resolve:
        output.error("Davinci Resolve doesn't respond.")
        exit(ERROR_DAVINIC_DOES_NOT_RESPOND)

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        output.error("Project manager not found.")
        exit(ERROR_PROJECTMANAGER_NOT_FOUND)

    if args.mode == "settimeline":
        return set_current_timeline(project_manager, args, output)
    else:
        if args.mode == "gettimeline":
            return get_current_timeline(project_manager, output)


if __name__ == "__main__":
    main()

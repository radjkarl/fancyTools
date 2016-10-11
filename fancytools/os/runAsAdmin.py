from __future__ import print_function
from __future__ import absolute_import
# WINDOWS ONLY AT THE MOMENT
import sys
import os  # , traceback, types


def runAsAdmin(cmdLine=None, target_dir='', wait=True):
    '''
    run [cmdLine] as admin
    specify the location from where the code is executed through [target_dir]
    '''
    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")
    # import win32api,
    import win32con
    import win32event
    import win32process
    from win32com.shell.shell import ShellExecuteEx

    from win32com.shell import shellcon

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (tuple, list):
        raise ValueError("cmdLine is not a sequence.")

    cmd = '"%s"' % (cmdLine[0],)
    # XXX TODO: isn't there a function or something we can call to message
    # command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    #cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    #showCmd = win32con.SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)
    print(target_dir, cmd, params)
    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params,
                              lpDirectory=target_dir)
    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        # print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None
    return rc

if __name__ == '__main__':
    from . import isAdmin

    runAsAdmin(('python', isAdmin.__file__[:-1]))

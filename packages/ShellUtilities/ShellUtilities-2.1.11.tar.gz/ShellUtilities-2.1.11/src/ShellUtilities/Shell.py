import subprocess
import logging
import time
from ShellUtilities.ShellCommandException import ShellCommandException
from ShellUtilities.ShellCommandResults import ShellCommandResults, AsynchronousShellCommandResults
import os
import threading
import queue
import asyncio
import json
import platform
from unittest.mock import patch, MagicMock

logger = logging.getLogger(__name__).parent


def __execute_shell_command(command, env, cwd, executable=None):
    # Create the process and wait for the exit
    process, executable = __execute_shell_command_async(command, env, cwd, executable)
    (stdout, stderr) = process.communicate()
    exitcode = process.returncode

    # The stderr and stdout are byte objects... lets change them to strings
    stdout = stdout.decode()
    stderr = stderr.decode()

    # Sanitize the variables and remove trailing newline characters
    stdout = stdout.rstrip("\n")
    stderr = stderr.rstrip("\n")

    return exitcode, stdout, stderr, executable


def __execute_shell_command_async(command, env, cwd, executable=None):

    args = [command]
    kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "shell": True,
        "close_fds": 'posix',
    }
    if executable:
        logging.debug(f"Executable set to: {executable}")
        kwargs["executable"] = executable
    if env:
        logging.debug(f"Environment set to: " + os.linesep + json.dumps(env, indent = 4))
        kwargs["env"] = env
    if cwd:
        logging.debug(f"CWD set to: {cwd}")
        kwargs["cwd"] = cwd

    # Create the process
    # Note: We have to do this nasty patch in order to determine the executable
    # being uses by the subprocess module
    original_method = None
    patch_method = None 
    system_name = platform.system()
    patch_called = False
    if system_name == "Windows":
        import _winapi
        original_method =_winapi.CreateProcess
        def patch_method(*args, **kwargs):
            nonlocal executable
            executable = args[0]
            logging.debug(f"Executable determined to be: {executable}")
            nonlocal patch_called
            patch_called = True
            return original_method(*args, **kwargs)
    else:
        import _posixsubprocess
        original_method = _posixsubprocess.fork_exec
        def patch_method(*args, **kwargs):
            nonlocal executable
            executable = args[1][0]
            logging.debug(f"Executable determined to be: {executable}")
            nonlocal patch_called
            patch_called = True
            return original_method(*args, **kwargs)
    
    process = None  
    if system_name == "Windows":
        with patch("_winapi.CreateProcess", side_effect=patch_method, autospec=True) as mock_bar:
            process = subprocess.Popen(*args, **kwargs)
    else:
        with patch("_posixsubprocess.fork_exec", side_effect=patch_method, autospec=True) as mock_bar:
            process = subprocess.Popen(*args, **kwargs)
    logging.debug("Process opened.")
    if not patch_called:
        logging.warning("Unable to determine the executable used by the process.")
    return process, executable


def execute_shell_command(command, max_retries=1, retry_delay=1, env=None, cwd=None, blocking=True, executable=None, async_buffer_funcs={}):

    try:

        if cwd and not os.path.isdir(cwd):
            raise Exception("The working directory '{0}' does not exist.".format(cwd))

        logging.debug("Running shell command:")
        logging.debug(command)

        for i in range(0, max_retries):

            # Run the shell command
            if blocking:
                exitcode, stdout_string, stderr_string, executable = __execute_shell_command(command, env, cwd, executable)
            else:
                process, executable = __execute_shell_command_async(command, env, cwd, executable)
                return AsynchronousShellCommandResults(command, executable, process, async_buffer_funcs)

            # If successful, return the results
            if exitcode == 0:
                logging.debug("Command STDOUT:")
                for line in stdout_string.split("\n"):
                    if line:
                        logging.debug(line)
                logging.debug("Command STDERR:")
                for line in stderr_string.split("\n"):
                    if line:
                        logging.error(line)
                return ShellCommandResults(command, executable, stdout_string, stderr_string, exitcode)

            # If an error occurred we need to determine if this is the last retry attempt
            last_retry = i == max_retries - 1

            # If it is not the last retry we must determine whether or not we can ignore the error
            # To do this we must see if our retry conditions have been satisfied
            if not last_retry:
                logging.debug("Retrying...(%s)" % i)
                time.sleep(retry_delay)
                continue
            else:
                err_msg = "Maximum retries (%s) exceeded for shell command."
                err_msg += " An error will be generated."
                logging.error(err_msg % max_retries)
                logging.error("Stdout:")
                for line in stdout_string.split("\n"):
                    logging.error(line)
                logging.error("Stderr:")
                for line in stderr_string.split("\n"):
                    logging.error(line)
                logging.error("Exit code: {0}".format(exitcode))

                raise ShellCommandException(command, stdout_string, stderr_string, exitcode)

    except Exception as ex:
        raise Exception("An error occurred while executing the shell command.") from ex

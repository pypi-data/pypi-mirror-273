from unittest import TestCase
from ShellUtilities import Shell
from ShellUtilities.ShellCommandResults import ShellCommandResults
import platform
import os
import time
import threading
import queue
import tracemalloc
import logging
import io
import sys

logging.basicConfig(level=logging.DEBUG)


tracemalloc.start()


class Test_Shell(TestCase):

    def test__execute_shell_command__success__print_env_var(self):
        shell_command_string = "echo $MYVAR"
        shell_command_result = Shell.execute_shell_command(shell_command_string, env={"MYVAR": "Hello, World!"})
        self.assertEqual(0, shell_command_result.ExitCode)
        self.assertEqual("", shell_command_result.Stderr)
        self.assertNotEqual("", shell_command_result.Stdout)
        self.assertIsNotNone(shell_command_result.Executable)

    def test__execute_shell_command__success__simple_pwd(self):
        system_name = platform.system()
        if system_name == 'Windows':
            shell_command_string = r'cd'
        else:
            shell_command_string = "pwd"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        shell_command_result = Shell.execute_shell_command(shell_command_string, env={}, cwd=current_dir)
        self.assertEqual(0, shell_command_result.ExitCode)
        self.assertEqual("", shell_command_result.Stderr)
        self.assertNotEqual("", shell_command_result.Stdout)
        self.assertEqual(current_dir, shell_command_result.Stdout.strip())
        self.assertIsNotNone(shell_command_result.Executable)

    def test__execute_shell_command__success__pwd_from_cwd(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        system_name = platform.system()
        if system_name == 'Windows':
            shell_command_string = r'cd'
        else:
            shell_command_string = "pwd"
        shell_command_result = Shell.execute_shell_command(shell_command_string, cwd=parent_dir)
        self.assertEqual(0, shell_command_result.ExitCode)
        self.assertEqual("", shell_command_result.Stderr)
        self.assertNotEqual("", shell_command_result.Stdout)
        self.assertEqual(parent_dir, shell_command_result.Stdout.strip())
        self.assertIsNotNone(shell_command_result.Executable)

    def test__execute_shell_command__success__non_blocking(self):
        shell_command_string = r"echo 'a'; sleep 2; echo 'b'"
        shell_command_result = Shell.execute_shell_command(shell_command_string, blocking=False)
        shell_command_result.wait()
        system_name = platform.system()
        if system_name == 'Windows':
            expected_stdout = "'a'; sleep 2; echo 'b'\r\r\n"
            expected_stdout_lines = 1
        else:
            expected_stdout = "a" + os.linesep + "b" + os.linesep
            expected_stdout_lines = 2
        self.assertFalse(shell_command_result.command_running())
        self.assertEqual(0, shell_command_result.ExitCode)
        self.assertTrue(shell_command_result.pid > 0)
        self.assertIsNotNone(shell_command_result.Stdout)
        self.assertEqual(expected_stdout, shell_command_result.Stdout)
        self.assertEqual("", shell_command_result.Stderr)
        self.assertEqual(expected_stdout_lines, len(shell_command_result.stdout_lines))
        self.assertEqual(0, len(shell_command_result.stderr_lines))
        self.assertIsNotNone(shell_command_result.Executable)

    def test__execute_shell_command__success__default_shell(self):
        shell_command_string = 'echo "$SHELL"'
        shell_command_result = Shell.execute_shell_command(shell_command_string)
        system_name = platform.system()
        if system_name == 'Windows':
            expected_stdout = '"$SHELL"\r'
        else:
            expected_stdout = "/bin/bash"
        self.assertEqual(0, shell_command_result.ExitCode)
        self.assertEqual("", shell_command_result.Stderr)
        self.assertEqual(expected_stdout, shell_command_result.Stdout)
        self.assertIsNotNone(shell_command_result.Executable)

    def test__execute_shell_command__success__bash_shell(self):
        shell_command_string = 'echo "$SHELL"'
        system_name = platform.system()
        if system_name != 'Windows':
            shell_command_result = Shell.execute_shell_command(shell_command_string, executable="/bin/bash")
            self.assertEqual(0, shell_command_result.ExitCode)
            self.assertEqual("", shell_command_result.Stderr)
            self.assertEqual("/bin/bash", shell_command_result.Stdout)
            self.assertIsNotNone(shell_command_result.Executable)

    def test__execute_shell_command__success__sh_shell(self):
        # The shell variable is set by the parent shell, which is bash in most environments
        # So it will be misleading
        shell_command_string = 'echo "$SHELL"'
        system_name = platform.system()
        if system_name != 'Windows':
            shell_command_result = Shell.execute_shell_command(shell_command_string, executable="/bin/sh")
            self.assertEqual(0, shell_command_result.ExitCode)
            self.assertEqual("", shell_command_result.Stderr)
            self.assertEqual("/bin/bash", shell_command_result.Stdout)
        
            # Something gets screwed up and we do not see exactly the same thing as the command line
            shell_command_string = r"cat /proc/$$/cmdline"
            shell_command_result = Shell.execute_shell_command(r'echo "/proc/$$/cmdline" | xargs -I {} cat {}')
            self.assertEqual(0, shell_command_result.ExitCode)
            self.assertEqual("", shell_command_result.Stderr)
            self.assertIn("/bin/sh", shell_command_result.Stdout)

            self.assertIsNotNone(shell_command_result.Executable)


    def test__handle_asynchronous_output__success__shell_command(self):
        shell_command_string = r"echo 'a'; sleep 2; echo 'b'; sleep 2; echo 'c'; sleep 2; echo 'd';"
        shell_command_result = Shell.execute_shell_command(shell_command_string, blocking=False)
        shell_command_result.wait()
        system_name = platform.system()
        if system_name == 'Windows':
            expected_stdout_lines = 1
        else:
            expected_stdout_lines = 4
        self.assertEqual(0, shell_command_result.process.poll())
        self.assertFalse(shell_command_result.command_running())
        self.assertEqual(0, shell_command_result.ExitCode)
        self.assertTrue(shell_command_result.pid > 0)
        self.assertEqual(expected_stdout_lines, len(shell_command_result.stdout_lines))
        self.assertEqual(0, len(shell_command_result.stderr_lines))
        self.assertIsNotNone(shell_command_result.Executable)

    def test__handle_asynchronous_output__success__script_using_module_code(self):
        # Run a script that takes 25 seconds to run and prints info to the stdout and stderr
        system_name = platform.system()
        if system_name == 'Windows':
            return
        current_directory = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_directory, "scripts", "loop.sh")
        shell_command_string = "bash '{0}'".format(script_path)
        shell_command_result = Shell.execute_shell_command(shell_command_string, blocking=False)
        shell_command_result.wait()
        self.assertEqual(0, shell_command_result.process.poll())
        self.assertFalse(shell_command_result.command_running())
        self.assertEqual(0, shell_command_result.ExitCode)
        self.assertTrue(shell_command_result.pid > 0)
        self.assertEqual(25, len(shell_command_result.stdout_lines))
        self.assertEqual(2, len(shell_command_result.stderr_lines))
        self.assertIsNotNone(shell_command_result.Executable)

    def test__handle_asynchronous_output__failure__python_script_raise_exception(self):
        system_name = platform.system()
        if system_name == 'Windows':
            return
        current_directory = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_directory, "scripts", "fail.py")
        shell_command_string = f"python3 '{script_path}'"
        shell_command_result = Shell.execute_shell_command(shell_command_string, blocking=False)
        with self.assertRaises(Exception) as context:
            shell_command_result.wait()

        self.assertEqual(1, shell_command_result.process.poll())
        self.assertFalse(shell_command_result.command_running())
        self.assertEqual(1, shell_command_result.ExitCode)
        self.assertTrue(shell_command_result.pid > 0)
        self.assertEqual(0, len(shell_command_result.stdout_lines))
        self.assertEqual(4, len(shell_command_result.stderr_lines))
        self.assertIsNotNone(shell_command_result.Executable)
        
        shell_command_exception = context.exception

        self.assertEqual(1, shell_command_exception.process.poll())
        self.assertEqual(1, shell_command_exception.ExitCode)
        self.assertTrue(shell_command_exception.pid > 0)
        self.assertEqual(0, len(shell_command_exception.stdout_lines))
        self.assertEqual(4, len(shell_command_exception.stderr_lines))


    def test__handle_asynchronous_output__success__shell_command_custom_pipes(self):
        system_name = platform.system()
        if system_name == 'Windows':
            return
        # Create a dummy string buffer to replace the default stdout
        # so that we can monitor the output of our test and show
        # that it executes asynchrously
        old_stdout = sys.stdout
        my_buffer = io.StringIO()
        sys.stdout = my_buffer
        
        try:
            
            # Define an async function to use when we execute the shell command
            def stdout_func(stdout_line):
                my_buffer.write(stdout_line + os.linesep)
                
            # Run the command and also output while the command is running
            shell_command_string = r"echo 'a'; sleep 2; echo 'b'; sleep 2; echo 'c'; sleep 2; echo 'd';"
            shell_command_result = Shell.execute_shell_command(shell_command_string, blocking=False, async_buffer_funcs={"stdout": [stdout_func]})
            time.sleep(1)
            print("hello")
            shell_command_result.wait()
            
            # Extract the output from stdout
            my_buffer.seek(0) # go to the start of the buffer
            output = my_buffer.readlines()
            
            # Show it ran async
            printed_message = "hello" + os.linesep
            self.assertTrue(printed_message in output)
            self.assertNotEqual(printed_message, output[0])
            self.assertNotEqual(printed_message, output[-1])

            
            # Do the normal checks
            self.assertEqual(0, shell_command_result.process.poll())
            self.assertFalse(shell_command_result.command_running())
            self.assertEqual(0, shell_command_result.ExitCode)
            self.assertTrue(shell_command_result.pid > 0)
            self.assertEqual(4, len(shell_command_result.stdout_lines))
            self.assertEqual(0, len(shell_command_result.stderr_lines))
            self.assertIsNotNone(shell_command_result.Executable)
            
        finally:
            # Set the buffer back
            sys.stdout = old_stdout

    def test__handle_asynchronous_output__success__shell_command_custom_pipes2(self):
        system_name = platform.system()
        if system_name == 'Windows':
            return
        # This is really just to see the output in the command line when running manually
        # It's a sanity check for the prior test
        
        # Define an async function to use when we execute the shell command
        def stdout_func(stdout_line):
            print(stdout_line)
            
        # Run the command and also output while the command is running
        shell_command_string = r"echo 'a'; sleep 2; echo 'b'; sleep 2; echo 'c'; sleep 2; echo 'd';"
        shell_command_result = Shell.execute_shell_command(shell_command_string, blocking=False, async_buffer_funcs={"stdout": [stdout_func]})
        time.sleep(1)
        print("hello")
        shell_command_result.wait()

        # Do the normal checks
        self.assertEqual(0, shell_command_result.process.poll())
        self.assertFalse(shell_command_result.command_running())
        self.assertEqual(0, shell_command_result.ExitCode)
        self.assertTrue(shell_command_result.pid > 0)
        self.assertEqual(4, len(shell_command_result.stdout_lines))
        self.assertEqual(0, len(shell_command_result.stderr_lines))
        self.assertIsNotNone(shell_command_result.Executable)

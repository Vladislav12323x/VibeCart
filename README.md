# VibeCart

# This is a description of how to install Langflow for technical support purposes, this is suitable for people who want to run everything on localhost.

To download the LangFlow environment, you need to open Windows Powershell and paste the following: pip install Langflow.
If the download stops at the inscription: 'Connection database', you need to stop the process with the key combination ctrl + c, enter 2 commands:
"netsh int up reset", "netsh winsock reset", then restart the computer and run "pip install Langflow" again.
Next we write: "uv- pip install UV", "pip install uv".
After completing all the previous steps, write: "uv run langflow run", this command will create localhost langflow. 
Then download .json and open the site at the address offered to you in the console. Create a Basic promting on the site. 
Upload .json in your project than open it and click on the button "share" and "embed in a site" and copy text.

# AIX System Check Script
Check the AIX operating system and automatically generate a report in html format.    
The The sample file is report.html.
## Description
Script usage instructions：
- Recommended to use python3.The writer uses Python 3.7.6
- The script tries to avoid using python third-party libraries
- Recommend AIX system version 7.1 or above.The writer uses AIX7100-04-03-1642
- Need AIX system root user authority to run
- If system using non-IBM multipath software, the path check script may be useless
- If several pagespaces are used, the information may be inaccurate，modify it when I have time
- The PowerHA check in the script has not been tested because there is no environment

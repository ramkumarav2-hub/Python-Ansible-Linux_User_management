User Management Script Workflow and User Guide

Overview

This document explains the workflow of the Python script `user_management.py` used for managing users on Linux systems via Ansible. 
The script dynamically generates an Ansible playbook based on user input and executes it to create, modify, or remove users.

Prerequisites

•	Python 3 installed on the control node

•	Ansible installed and configured

•	SSH access to managed nodes

•	Inventory file specifying target hosts

•	Proper sudo privileges for user management


Script Flow

1.	Display a banner and prompt user for execution mode (existing playbook or new).
2.	If new playbook: Collect user details interactively (username, state, shell, groups, password, sudo access).
3.	Generate an Ansible playbook dynamically based on inputs.
4.	Write the playbook to `user_management.yml`.
5.	Execute the playbook using `ansible-playbook`.
   
Key Functions (Function	Description)

read_user()	Collects user details interactively from the console.

generate_playbook(users)	Creates a list of Ansible tasks based on user input.

write_playbook(playbook)	Writes the generated playbook to a YAML file.

run_playbook(filename)	Executes the generated playbook using Ansible.

Execution Steps

1.	Navigate to the project directory: `cd /home/rvi2815-2/user_management`.
2.	Run the script: `python3 user_management.py`.
3.	Follow prompts to either execute an existing playbook or create a new one.
4.	Verify user creation on target hosts using `id <username>` or `getent passwd`.

 
Detailed Workflow Explanation with Questions

Start

The script begins execution and displays a banner: 'Redhat User Management'.

Check if existing playbook should be run

Question: Do you want to run existing playbook (yes/no):
Logic: If yes, run ansible-playbook user_management.yml; if no, proceed to collect user details.

Read User Data (Interactive Questions)

Questions asked for each user:
1. Enter how many users needs to be created:
2. Enter the username:
3. Enter state (present/absent):
4. Enter comment (optional):
5. Enter shell (optional):
6. Enter group (optional):
7. Enter groups (optional):
8. Enter password (optional):
   
Password expiry options:
Choose an option:
1 - Force password change on first login
2 - Set maximum password expiry days
If 2, then: Enter maximum days of expiry:

Sudo access: Should user have sudo access? (yes/no):

Generate Ansible Playbook

Creates tasks for user management, password expiry, and sudoers configuration.

Write Playbook to File

Saves the generated playbook as user_management.yml.

Run Generated Playbook

Executes ansible-playbook user_management.yml.

import csv
import yaml
import json
import sys
import subprocess

def read_user():
    users = []
    user_count = int(input("Enter how many users needs to be created: ").strip())
    for i in range(user_count):
        print("\n" + "*" * 90)
        print(f"\n### User {i+1} Details ###")
        print("\n" + "*" * 90 + "\n")
        username = input(" 1. Enter the username: ").strip()      
        state = input(" 2. Enter state (present/absent): ").strip()
        comment = input(" 3. Enter comment (optional): ").strip()
        shell = input(" 4. Enter shell (optional): ").strip()
        group = input(" 5. Enter group (optional): ").strip()
        groups = input(" 6. Enter groups (optional): ").strip()
        password = input(" 7. Enter password (optional): ").strip()
        print(f"\nChoose an option:\n1 - Force password change on first login\n2 - Set maximum password expiry days\n")
        chage = input("Enter your choice (1 or 2): ").strip()
        chage_max = None
        if chage == "2":
            chage_max = input("Enter maximum days of expiry: ").strip()
        sudo = input("\n 8. Should user have sudo access? (yes/no): ").strip().lower() == "yes"


        users.append({
            "username" : username,
            "state": state,
            "comment": comment,
            "shell": shell if shell else None,
            "group": group if group else None,
            "groups": groups if groups else None,
            "password": password if password else None,
            "chage": chage if chage else None,
            "chage_max": chage_max if chage_max else None,
            "sudo": sudo
            })

    return users

def generate_playbook(users):
    tasks = []
    for user in users:
        if user.get("password") == None:
            task = {
                "name": f"Manage user {user['username']}",
                "ansible.builtin.user": {
                    "name": user["username"],
                    "state": user["state"],  # present or absent
                 }
            }
        else:
            user_password = user["password"]
            task = {
                "name": f"Manage user {user['username']}",
                "ansible.builtin.user": {
                    "name": user["username"],
                    "state": user["state"],  # present or absent
                    "password": f"{{{{ \"{user_password}\" | password_hash(\'sha512\') }}}}"
                 }
            }
		
        #handle if inputs are available
        if user.get("comment"):
            task["ansible.builtin.user"]["comment"] = user["comment"]
		
        if user.get("shell"):
            task["ansible.builtin.user"]["shell"] = user["shell"]

        if user.get("group"):
            task["ansible.builtin.user"]["group"] = user["group"]

        if user.get("groups"):
            task["ansible.builtin.user"]["groups"] = user["groups"]

        tasks.append(task)

        # Password expiry
        if user.get("chage") or user.get("chage_max"):
            if user.get("chage") == "2":
                chage_task = {
                    "name": f"Set password expiry (maximum days) for {user['username']}",
                    "ansible.builtin.command": {
                        "cmd": f"chage -M {user['chage_max']} {user['username']}"
                        }
                    }
            else:
                chage_task = {
                    "name": f"Set password first login expiry for {user['username']}",
                    "ansible.builtin.command": {
                        "cmd": f"chage -d 0 {user['username']}"
                        }
                    }
        tasks.append(chage_task)

        # Add sudoers line if sudo=True
        if user.get("sudo"):
            sudo_task = {
                "name": f"Add {user['username']} to sudoers",
                "ansible.builtin.lineinfile": {
                    "path": "/etc/sudoers",
                    "state": "present",
                    "regexp": f"^{user['username']} ",
                    "line": f"{user['username']} ALL=(ALL) NOPASSWD:ALL",
                    "validate": "visudo -cf %s"
                }
            }
            tasks.append(sudo_task)

    playbook = [{
        "name": "User Management Workflow",
        "hosts": "all",
        "become": True,
        "tasks": tasks
    }]
    return playbook

def write_playbook(playbook, filename="user_management.yml"):
    yaml_text = yaml.dump(playbook, default_flow_style=False)
    yaml_text = yaml_text.replace("\n- name:", "\n\n- name:")

    with open(filename, "w") as f:
        f.write(yaml_text)

    print(f"Playbook generated: {filename}")
    return filename


def run_playbook(filename):
    print("Executing playbook...")
    subprocess.run(["ansible-playbook", filename])

if __name__ == "__main__":
    print("\n" + "#" * 90)
    print("#" + " " * 30 + "Redhat User Management" + " " * 36 + "#")
    print("#" * 90 + "\n")
    option = input("Do you want to run existing playbook (yes/no): ").strip()
    print("\n" + "*" * 90 + "\n")
    if option == "yes":
        print("Executing playbook...")
        subprocess.run(["ansible-playbook", "user_management.yml"])
    else:
        users = read_user()
        playbook = generate_playbook(users)
        filename = write_playbook(playbook)
        run_playbook(filename)



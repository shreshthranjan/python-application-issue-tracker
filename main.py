from database import (
    add_incident,get_all_incidents,search_incident,update_status,delete_incident,get_incident_report)
import logging_config
import logging
logging.info("Application started")

def add_incident_menu():
    incident_title=input("Enter Incident Title (q to cancel):")
    if incident_title.lower()=='q':
        print("Operation Cancelled")
        return
    issue_description=input("Enter Issue Description:")
    while True:
        priority=input("Enter Priority (High/Medium/Low):")
        if priority.lower() in ("high",'medium','low'):
            break
        print("Invalid Choice. Choice must be High/Medium/Low.")
    add_incident(
        incident_title,
        issue_description,
        priority,
        "Open"
    )
    logging.info(f"New Incident Added: {incident_title}.")
    print("Incident added successfully.")

def view_incidents_menu():
    data=get_all_incidents()
    if not data:
        logging.warning("Searched and found no incidents.")
        print("There are no incidents currently.")
    else:
        print("---All Incidents---")
        print("")
        for incident in data:
            print(f"ID: {incident[0]}")
            print(f"Title: {incident[1]}")
            print(f"Issue: {incident[2]}")
            print(f"Priority: {incident[3]}")
            print(f"Status: {incident[4]}\n")
        logging.info("All incidents shown successfully.")

def search_incident_menu():
    search_title=input("Enter the incident you want to display (q to cancel):")
    if search_title.lower()=="q":
        print("Cancelling Operation.")
        return
    incident=search_incident(search_title)
    if incident:
        logging.info(f"Incident searched successfully: {search_title}.")
    if not incident:
        logging.warning(f"Incident Search Failed: {search_title}")
    if incident:
        print(f"ID: {incident[0]}")
        print(f"Title: {incident[1]}")
        print(f"Issue: {incident[2]}")
        print(f"Priority: {incident[3]}")
        print(f"Status: {incident[4]}\n")    
    if not incident:
        print("You've entered wrong Title. Please try again.")

def update_incident_menu():
    update_title=input("Enter the title of the incident that you want to update (q to cancel):")
    if update_title.lower()=="q":
        print("Operation Cancelled.")
        return
    found=search_incident(update_title)
    if found:
        while True:
            incident_status=input("Enter the status of the incident(Open/In Progress/Resolved):")
            if incident_status.lower() in ['open','in progress','resolved']:
                break
            print("Incident status must be Open/In Progress/Resolved. Please try again.")
        result=update_status(update_title,incident_status)
        if result:
            logging.info(
            f"Incident Status Updated from {found[4]} to {incident_status}."
            )
            print('Status Updated!')
        else:
            logging.warning(f"Failed to update incident: {update_title}")
            print("Unable to update status.")
    else:
        print("Incident not found.")

def delete_incident_menu():
    delete_title=input("Enter the title of the incident you want to delete (q to cancel):")
    if delete_title.lower()=="q":
        print("Cancelling Operation.")
        return
    result=delete_incident(delete_title)
    if result:
        logging.info(f"Incident deleted: {delete_title}")
        print("Incident Removed.")
    else:
        logging.warning(f"Attempted to delete non-existing incident: {delete_title}")
        print("Incident not found.")

def incident_report_menu():
    report=get_incident_report()

    if report is None:
        print("Unable to generate report.")
        return

    total, status_counts, priority_counts = report

    print("==========INCIDENTS REPORT==========")
    print("")
    print(f"Total Incidents: {total}")
    print("")

    print("STATUS")
    print("--------------------")
    for status,count in status_counts:
        print(f"{status:<15}: {count}")

    print("")
    print("PRIORITY")
    print("--------------------")
    for priority,count in priority_counts:
        print(f"{priority:<15}: {count}")
    print("")
    
def main():
    while True:
        print("===============================")
        print("APPLICATION ISSUE TRACKER")
        print("===============================")
        print("")
        print("1. Add Incident")
        print("2. View All Incidents")
        print("3. Search Incident")
        print("4. Update Incident Status")
        print("5. Delete Incident")
        print("6. Incident Report")
        print("7. Exit")
        print("")
        choice=input("Enter your choice:")
        print("")
        if choice=="1":
            add_incident_menu() 
        elif choice=="2":
            view_incidents_menu()
        elif choice=="3":
            search_incident_menu()
        elif choice=="4":
            update_incident_menu()
        elif choice=="5":
            delete_incident_menu()
        elif choice=="6":
            incident_report_menu()
        elif choice=="7":
            print('Exiting Application. Goodbye!')
            break
        else:
            print("Invalid Choice. Please enter a number between 1 to 6. ")

if __name__=="__main__":
    main()

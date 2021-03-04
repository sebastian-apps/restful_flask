import requests 
import json


BASE = "http://127.0.0.1:5000/"



def main():


    data = [
        {
            "task": {"title": "Learn Flask", "desc": "Python framework"},
            "steps": [
                {"step_num": 1, "desc": "Learn frameworks basics"},
                {"step_num": 2, "desc": "Learn RESTful API"},
                {"step_num": 3, "desc": "Dockerize"},
            ]
        },
        {
            "task": {"title": "Exercise", "desc": "Bike 15 min every day"},
            "steps": []
        },
        {
            "task": {"title": "Car stuff", "desc": "Need to do before winter"},
            "steps": [
                {"step_num": 1, "desc": "Install winter tires"},
                {"step_num": 2, "desc": "Fix windshield cracks"},
            ]
        },
    ]



    """ LOAD DATABASE """
    # Initialize step_id
    step_id = -1
    # Iterate over data and load database with tasks and steps
    for task_id, task in enumerate(data):
        response = requests.post(f"{BASE}task/{task_id}", task.get("task"))
        # load steps related to that task
        for step in task.get("steps"):
            step.update({"task_id": task_id})
            step_id += 1
            response = requests.post(f"{BASE}step/{step_id}", step)
            




    """ QUERY DATABASE """

    # Get all data, including steps
    response = requests.get(BASE + "task")

    # Try to delete task 0, but it should not since it still has steps.
    response = requests.delete(BASE + "task/0")

    # Delete first two steps
    response = requests.delete(BASE + "step/0")
    response = requests.delete(BASE + "step/1")

    # Display only task 0 and its steps
    response = requests.get(BASE + "task/0")
    # pprint(response)
    assert len(response.json().get("steps"))==1, "Should be len(steps) = 1 for task 0"

    # Update task 1
    response = requests.put(BASE + "task/1", {"desc": "Bike 30 min every day"})
    assert response.json().get("desc")=="Bike 30 min every day", "Should be 'Bike 30 min every day'"

    # Attempt to add a new task with taken id   
    response = requests.post(BASE + "task/2", {"title": "Buy wine", "desc": "Dinner party"})
    assert response.json().get("message") == "Task id taken", "Should be 'Task id taken'"

    # Add a new task  
    response = requests.post(BASE + "task/3", {"title": "Buy wine", "desc": "Dinner party"})

    # Add a step to that task  
    response = requests.post(BASE + "step/5", {"task_id": 3, "step_num": 1, "desc": "Red or white?"})

    # Get all steps
    response = requests.get(BASE + "step/")
    assert response.json()[1].get("desc")=="Install winter tires", "Should be 'Install winter tires'"

    # Update a step to that task  
    response = requests.put(BASE + "step/5", {"desc": "Red"})
    assert response.json().get("desc")=="Red", "Should be 'Red'"


    response = requests.get(BASE + "task/")
    pprint(response)

    print("Everything passed.")






# pretty print
def pprint(resp):
    print(json.dumps(resp.json(), indent=4))



if __name__ == "__main__":
    main()





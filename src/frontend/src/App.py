from pathlib import Path
from flask import Flask, jsonify, render_template, request
import sys
import os
sys.path.append("c:\\Users\\Rican's Pooter\\GitHub\\group-project\\src\\frontend\\src\\Forms.py")

path = Path(os.path.dirname(os.path.realpath(__file__)))
parent_path = path.parent.absolute().parent.absolute()
parent_path_formatted = f"{parent_path}".replace('WindowsPath(','').replace('(','').replace(')','') + "\\" # type: ignore
sys.path.append(parent_path_formatted) # type: ignore
from shared.data import DB_FILEPATH, FuncReq, NonFuncReq, Project, Risks, project_data_to_json

#sys.path.append("C:\\Users\\Rican's Pooter\\GitHub\\group-project\\src\\shared\\data.py")
#print(sys.path)
from Forms import NewProject
#from shared import data
import json
import requests

# path = Path(os.path.dirname(os.path.realpath(__file__)))
# parent_path = path.parent.absolute()
# parent_path_formatted = f"{parent_path}".replace('WindowsPath(','').replace('(','').replace(')','') + "\\" # type: ignore
# sys.path.append(parent_path_formatted) # type: ignore
# print(parent_path_formatted)
# from shared.data import DB_FILEPATH, FuncReq, NonFuncReq, NewProject, Risks, NewProject_data_to_json 



app = Flask(__name__)   # Class handle to call Flask API
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/create', methods=['GET', 'POST'])
def create_requirement():
    NewProject_form = NewProject()
    if NewProject_form.is_submitted():
        print("form has been submitted")
        result = request.form
        result_dict = request.form.to_dict()
        current_data = requests.get('http://127.0.0.1:8000/user-read-datasets')
        response = current_data.content.decode("utf-8")
        
        
        try:
            project_id, func_id, nonfunc_id, risk_id = get_latest_ids(resp=response)
            fq = FuncReq(id=func_id+1, project_id=project_id+1, requirement=result_dict['func_requirement'], owner=result_dict['func_requirement_owner'])
            nfq = NonFuncReq(id=nonfunc_id + 1, project_id=project_id+1, requirement=result_dict['nonfunc_requirement'], owner=result_dict['nonfunc_requirement_owner'])
            risk = Risks(id=risk_id+1, project_id=project_id+1, risk=result_dict['risk'], risk_status=result_dict['risk_status'])
            prj = Project(project_id=project_id+1, project_name=result_dict['name'], project_desc=result_dict['desc'], project_owner=result_dict['owner'], 
                        team_members=[result_dict['members']], func_req=[fq], non_func_req=[nfq], analysis_hours=float(result_dict['analysis_hours']), 
                        design_hours=float(result_dict['design_hours']), coding_hours=float(result_dict['coding_hours']), testing_hours=float(result_dict['testing_hours']), 
                        mgt_hours=float(result_dict['mgt_hours']), risks=[risk])
            postdata = project_data_to_json(data=prj)
            requests.post('http://127.0.0.1:8000/user-create-datasets', data=postdata)
        except Exception as e:
            print(f"Exception while creating project... Error: {e}")
        return render_template('Project.html', result=result)
    return render_template('Form.html', form = NewProject_form)


@app.route('/read', methods=['GET'])  # Grabs data from flask app
def get_data():
    data = requests.get('http://127.0.0.1:8000/user-read-datasets')
    print(f"data = {data.content}")
    return data.content


def get_latest_ids(resp: str) -> tuple[int, int, int, int]:
    #print("test")
    # Remove '{}' from response to grab list
    json_dict = json.loads(json.loads(resp)[-1])
    project_id = int(json_dict['project_id'])
    func_req_id = int(json_dict['func_req'][-1]['id'])
    non_func_req_id = int(json_dict['non_func_req'][-1]['id'])
    risk_id = int(json_dict['risks'][-1]['id'])
    print(f"{project_id}, {func_req_id}, {non_func_req_id}, {risk_id}")
    return project_id, func_req_id, non_func_req_id, risk_id

# Used to for testing/troubleshooting purposes
if __name__ == '__main__':
    app.run(debug=True)  # Main entry point - start webserver

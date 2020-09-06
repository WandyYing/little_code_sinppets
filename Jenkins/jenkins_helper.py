from logging import setLogRecordFactory
import jenkins
import time

class JRunner:
    
    def __init__(self, server, username, password) -> None:
        self.server = jenkins.Jenkins(server, username=username, password=password)
        # print(self.server, dir(self.server))

    def build_job(self,job_name, job_params: dict):
        self.server.build_job(job_name, job_params)
    
    def build_info(self, build_number):
        # last_build_number = self.server.get_job_info('TMS_Execution_Task')['lastCompletedBuild']['number']
        return self.server.get_build_info('TMS_Execution_Task', build_number)

    def get_last_completed_build_number(self, job_name):
        return self.server.get_job_info(job_name)['lastCompletedBuild']['number']


if __name__ == "__main__":
    pass
    # jr = JRunner("", "", "")
    # jr.build_job("TMS_Execution_Task", {"project": "oms", "testcases": '["testcases/Smoke","testcases/cart","testcases/Smoke","testcases/cart"]'})
    # number = jr.get_last_completed_build_number()
    # jr.build_info()
    # time.sleep(5)
    # jr.build_info()
    # time.sleep(5)
    # jr.build_info()
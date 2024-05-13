import asyncio
import random
import re
import time

from cloudpss.job.view.view import View
from .view import getViewClass

from cloudpss.utils.IO import IO
from .messageStreamReceiver import MessageStreamReceiver

from cloudpss.utils.graphqlUtil import graphql_request
from .messageStreamSender import MessageStreamSender
from typing import Any, Callable, Generic, TypeVar
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T', bound=Callable[..., View])
class Job(Generic[T]):
    """docstring for Job"""
    __jobQuery = """query($_a:JobInput!){
            job(input:$_a){
                id
                args
                createTime
                startTime
                endTime
                status
                context
                user
                priority
                policy  { 
                    name
                    queue
                    tres {
                        cpu
                        ecpu
                        mem
                    } 
                    priority 
                    maxDuration 
                }
                machine {
                    id
                    name
                }
                input
                output
                position
            }
        }"""
    
    __createJobQuery = """mutation($input:CreateJobInput!){job:createJob(input:$input){id input output status position}}"""
    def __init__(
        self,
        id,
        args,
        createTime,
        startTime,
        endTime,
        status,
        context,
        user,
        priority,
        policy,
        machine,
        input,
        output,
        position,
    ):
        super(Job, self).__init__()
        self.id = id
        self.args = args
        self.createTime = createTime
        self.startTime = startTime
        self.endTime = endTime
        self.job_status = status #这里的status字段与原本的status()冲突
        self.context = context
        self.user = user
        self.priority = priority
        self.policy = policy  # type: ignore
        self.machine = machine # type: ignore
        self.input = input
        self.output = output
        self.position = position
        self.__receiver = None
        self.__sender = None
        self._result = None

    @staticmethod
    def fetch(id):
        """
        获取job信息
        """
        if id is None:
            raise Exception("id is None")
       
        variables = {"_a": {"id": id}}

        r =  graphql_request(Job.__jobQuery, variables)
        if "errors" in r:
            raise Exception(r["errors"])
        return Job(**r["data"]["job"])
        
    
    # @staticmethod
    # def fetchMany(*args):
    #     """
    #     批量获取任务信息
    #     """
    #     # jobs = CustomAsyncIterable(Job.fetch,*args)
    #     # return jobs 
    

    
    @staticmethod
    def __createJobVariables(job, config, revisionHash, rid, policy, **kwargs):
        # 处理policy字段
        if policy is None:
            policy = {}
            if policy.get("tres", None) is None:
                policy["tres"] = {}
            policy["queue"] = job["args"].get("@queue", 1)
            policy["priority"] = job["args"].get("@priority", 0)
            tres = {"cpu": 1, "ecpu": 0, "mem": 0}
            tresStr = job["args"].get("@tres", "")
            for t in re.split("\s+", tresStr):
                if t == "":
                    continue
                k, v = t.split("=")
                tres[k] = float(v)  # type: ignore
            policy["tres"] = tres
        function = job["rid"].replace("job-definition/cloudpss/", "function/CloudPSS/")
        implement = kwargs.get("implement", None)
        debug = job["args"].get("@debug", None )
        debugargs={}
        if debug is not None:
            t= [ i.split('=') for i in re.split(r'\s+',debug) if i.find('=')>0]
            for i in t:
                debugargs[i[0]]=i[1]
        variables = {
            "input": {
                "args": {
                    **job["args"],
                    "_ModelRevision": revisionHash,
                    "_ModelArgs": config["args"],
                    "implement":implement
                },
                "context": [
                    function,
                    rid,
                    f"model/@sdk/{str(int(time.time() * random.random()))}",
                ],
                "policy": policy,
                "debug":debugargs
            }
        }
        return variables
    @staticmethod
    def create(revisionHash, job, config, name=None, rid="", policy=None, **kwargs):
        """
        创建一个运行任务

        :params: revision 项目版本号
        :params: job 调用仿真时使用的计算方案，为空时使用项目的第一个计算方案
        :params: config 调用仿真时使用的参数方案，为空时使用项目的第一个参数方案
        :params: name 任务名称，为空时使用项目的参数方案名称和计算方案名称
        :params: rid 项目rid，可为空

        :return: 返回一个运行实例

        >>> runner = Runner.runRevision(revision,job,config,'')
        """
        variables=Job.__createJobVariables(job, config, revisionHash, rid, policy)
        r =  graphql_request(Job.__createJobQuery, variables)
        if "errors" in r:
            raise Exception(r["errors"])
        id = r["data"]["job"]["id"]
        return  Job.fetch(id)
        
    

    @staticmethod
    def load(file, format="yaml"):
        return IO.load(file, format)

    @staticmethod
    def dump(job, file, format="yaml", compress="gzip"):
        return IO.dump(job, file, format, compress)

    

    def read(self, receiver=None, **kwargs):
        """
        使用接收器获取当前运行实例的输出
        """
        if receiver is not None:
            self.__receiver = receiver
        if self.__receiver is None:
            self.__receiver = MessageStreamReceiver(self)
            self.__receiver.connect(**kwargs)
        return self.__receiver

    
    
    def write(self, sender=None,  **kwargs) -> MessageStreamSender:
        """
        使用发送器为当前运行实例输入
        """

        if sender is not None:
            self.__sender = sender
        if self.__sender is None:
            self.__sender = MessageStreamSender(self)
        self.__sender.connect_legacy(**kwargs)
        return self.__sender
    
    def status(self):
        """
        return: 0: 运行中 1: 运行完成 2: 运行失败
        """
        time.sleep(0)
        if self.__receiver is not None:
            return self.__receiver.status
        if self.__receiver is None:
            self.__connect()
        
        return 0
    
    def __connect(self):
        """
        连接接收器和发送器
        """
        viewType = getViewClass(self.context[0])
        self._result = self.view(viewType)
        
    @property
    def result(self)->T:
        """
        获取当前运行实例的输出
        """
        if self._result is None:
            self.__connect()
        return self._result
   
    
    def view(self, viewType:F=None)->F:
        """
        获取当前运行实例的输出
        """
        receiver =  self.read()
        sender =  self.write()
        if viewType is None:
            viewType = getViewClass(self.context[0])
        
        return viewType(receiver, sender)

    

    def abort(self,timeout=3):
        """
        中断当前运行实例
        """
        query = '''mutation ($input: AbortJobInput!) {
            job: abortJob(input: $input) {
                id
                status
            }
        }
        '''
        variables = {
            'input': {
                'id': self.taskId,
                'timeout': timeout
            }
        }
        graphql_request(query, variables)
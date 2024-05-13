from functools import wraps
from sanic.views import HTTPMethodView  # 基于类的视图
from sanic import Request
from co6co_db_ext.db_utils import db_tools, QueryPagedByFilterCallable
from co6co_db_ext.db_filter import absFilterItems
from co6co_db_ext.db_operations import DbPagedOperations, DbOperations, InstrumentedAttribute
from co6co_sanic_ext.model.res.result import Page_Result
from co6co_sanic_ext.utils import JSON_util
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import scoped_session
from typing import TypeVar, Dict, List, Any, Tuple
from co6co_sanic_ext.model.res.result import Result, Page_Result
import aiofiles
import os
import multipart
from io import BytesIO
from co6co_web_db.utils import DbJSONEncoder

from sqlalchemy import Select,Column, Integer, String, Update,Delete,Insert
from co6co_sanic_ext .view_model import BaseView
from co6co_db_ext.po import BasePO, TimeStampedModelPO, UserTimeStampedModelPO,CreateUserStampedModelPO
from datetime import datetime
from co6co.utils.tool_util import list_to_tree,get_current_function_name
from co6co_db_ext.db_utils import db_tools,  DbCallable, QueryOneCallable,UpdateOneCallable, QueryListCallable, QueryPagedByFilterCallable



from co6co.utils import log, getDateFolder

from ..model.params import associationParam
# from api.auth import authorized


def get_db_session(request: Request) -> AsyncSession | scoped_session:
    """
    获取db session
    """
    session = request.ctx.session
    if isinstance(session, AsyncSession):
        return session
    elif isinstance(session, scoped_session):
        return session
    raise Exception("未实现DbSession")


async def get_one(request: Request, select: Select,isPO:bool=True):
    """
    获取一条记录
    """
    call = QueryOneCallable(get_db_session(request))
    return await call(select,isPO) 

def errorLog(request: Request,module:str,method:str):
    log.err(f"执行[{request.method}]{request.path} 所属模块:{module}.{method} Error")


class BaseMethodView(BaseView):
    """
    视图基类： 约定 增删改查，其他未约定方法可根据实际情况具体使用
    views.POST  : --> query list
    views.PUT   :---> Add 
    view.PUT    :---> Edit
    view.DELETE :---> del

    """  
    def get_db_session(self, request: Request) -> AsyncSession | scoped_session:
        return get_db_session(request)

    async def get_one(self, request: Request, select: Select,isPO:bool=True):
        return await get_one(request, select,isPO)
    async def update_one(self, request: Request, select: Select,editFn:None ):
        """
        更新 PO
        editFn(session,basePO): 对select 的第一条记录赋值,没有赋值或者没有更改->不执行update
                                返回一个对象:http 应答，
                                        None:滚数据请求失败

        """
        try:
            call=UpdateOneCallable(self.get_db_session(request))
            result= await call(select,editFn)  
            if result!=None:return result
            else: return JSON_util.response(Result.fail(message=f"更新失败"))
        except Exception as e:
            errorLog(request,self.__class__,get_current_function_name())
            return Result.fail(message=f"请求异常：{e}")

    async def query_mapping(self, request: Request, select: Select, oneRecord: bool = False):
        """
        执行查询: 一个列表|一条记录
        """
        try:
            async with self.get_db_session(request) as session, session.begin():
                executer = await session.execute(select)
                if oneRecord:
                    result = executer.mappings().fetchone()
                    result = Result.success(db_tools.one2Dict(result))
                    return JSON_util.response(result)
                else:
                    result = executer.mappings().all()
                    result = Result.success(db_tools.list2Dict(result))
                    return JSON_util.response(result)
        except Exception as e:
            errorLog(request,self.__class__,get_current_function_name())
            return Result.fail(message=f"请求失败：{e}")

    async def _query(self, request: Request, select: Select  , isPO: bool = True, remove_db_instance: bool = True):
        """
        执行查询: 列表 
        """
        try:
            session: AsyncSession = request.ctx.session
            query = QueryListCallable(session)
            data = await query(select, isPO, remove_db_instance)
            result = db_tools.list2Dict(data)
            return result 
        except Exception as e:
            errorLog(request,self.__class__,get_current_function_name())
            return None 

    async def query_list(self, request: Request, select: Select,   isPO: bool = True, remove_db_instance: bool = True):
        """
        执行查询:  列表 
        """
        try:
            result=await self._query(request, select,   isPO , remove_db_instance)  
            return JSON_util.response(Result.success(data=result))
        except Exception as e:
            errorLog(request,self.__class__,get_current_function_name())
            result = Result.fail(message=f"请求失败：{e}")
            return JSON_util.response(Result.success(data=result))


    async def query_tree(self, request: Request, select: Select, rootValue: any = None, pid_field: str = "pid", id_field: str = "id", isPO: bool = True, remove_db_instance: bool = True):
        """
        执行查询: tree列表 
        """
        try: 
            result =   await self._query(request, select,   isPO , remove_db_instance)  
            if result ==None:treeList=[]
            else :treeList = list_to_tree(result, rootValue, pid_field, id_field)
            if len(treeList) == 0:
                return JSON_util.response(Result.success(data=[]))
            return JSON_util.response(Result.success(data=treeList))
        except Exception as e:
            errorLog(request,self.__class__,get_current_function_name())
            result = Result.fail(message=f"请求失败：{e}")
            return JSON_util.response(Result.success(data=result))

    async def query_page(self, request: Request, filter: absFilterItems, isPO: bool = True, remove_db_instance=True):
        """
        分页查询
        """
        filter.__dict__.update(request.json)
        try:
            query = QueryPagedByFilterCallable(self.get_db_session(request))
            total, result = await query(filter, isPO, remove_db_instance)
            pageList = Page_Result.success(result, total=total)
            return JSON_util.response(pageList) 
        except Exception as e:
            errorLog(request,self.__class__,get_current_function_name())
            pageList = Page_Result.fail(message=f"请求失败：{e}")
            return JSON_util.response(pageList)
        
    async def execSqls(self, request: Request,*sml:Update|Delete|Insert,callBck=None):
        callable = DbCallable(self.get_db_session(request))
        async def exec(session:AsyncSession):
            try:
                result=[]
                for sql in sml:  
                    r=await db_tools.execSQL(session,sql) 
                    result.append(r) 
                if callBck!=None: 
                    return await callBck(*result)
            except Exception as e:
                await session.rollback()
                errorLog(request,self.__class__,get_current_function_name())
                return JSON_util.response(Result.fail(e))

        return await callable(exec) 



    async def add(self, request: Request, po: BasePO, json2Po:bool=True, userId=None, beforeFun=None, afterFun=None):
        """
        增加 

        request: Request, 
        po: BasePO,      #实体类对象 
        userId=None, # 用户ID
        beforeFun(po, session, request),    # 执行一些其他操作，返回值将直接返回客户端，回滚数据库操作
        afterFun(po, session, request),     # 可在实体中获取 自增id

        return JSONResponse
        """
        try:
            if json2Po:po.__dict__.update(request.json)
            async def exec(session: AsyncSession): 
                if isinstance(po, UserTimeStampedModelPO): 
                    po.createTime = datetime.now() 
                    po.createUser = userId
                elif isinstance(po,TimeStampedModelPO):
                    po.createTime = datetime.now() 

                if beforeFun != None:
                    result = await beforeFun(po, session, request)
                    if result != None: 
                        await session.rollback() 
                        return result
                session.add(po)
                if afterFun != None:
                    session.flush()
                    await afterFun(po, session, request)
                return JSON_util.response(Result.success())

            callable = DbCallable(self.get_db_session(request))
            return await callable(exec) 
        except Exception as e: 
            errorLog(request,self.__class__,get_current_function_name())
            return JSON_util.response(Result.fail(message=e))

    async def edit(self, request: Request, pk: any, poType: TypeVar, po:BasePO=None, userId=None, fun=None,json2Po:bool=True):
        """
        编辑

        request: Request, 
        pk: any,          # 主键
        poType: TypeVar,  # 实体类型
        po:BasePO    ,    # None:根据传入的 poType创建,用 request.json赋值
        userId=None, # 用户ID
        fun=None,    # 执行一些其他操作，返回值将直接返回客户端，回滚数据库操作
        json2Po:bool # 根据 请求的json 转换的对象更新 实体对象，在 fun 之前执行

        return JSONResponse
        """
        try:
            if po==None:
                po=poType()
                po.__dict__.update(request.json)
            async with self.get_db_session(request) as session, session.begin():
                oldPo: poType = await session.get_one(poType, pk)
                if oldPo == None:
                    return JSON_util.response(Result.fail(message=f"未查到‘{pk}’对应的信息!"))
                if isinstance(oldPo, UserTimeStampedModelPO): 
                    oldPo.updateTime = datetime.now() 
                    oldPo.updateUser = userId
                elif isinstance(oldPo,TimeStampedModelPO):
                    oldPo.updateTime = datetime.now()  

                if json2Po:
                    oldPo.update(po)
                if fun != None:
                    result = await fun(oldPo, po, session, request) 
                    if result != None:
                        await session.rollback()
                        return result
                return JSON_util.response(Result.success())
        except Exception as e:
            await session.rollback()
            errorLog(request,self.__class__,get_current_function_name())
            return JSON_util.response(Result.fail(message=e))

    async def remove(self, request: Request, pk: any,poType: TypeVar,  beforeFun=None, afterFun=None):
        """
        删除 

        request: Request, 
        pk: any,      #主键值
        poType: TypeVar # 实体类型
        beforeFun(oldPo, session),    # 执行一些其他操作，返回值将直接返回客户端，回滚数据库操作
        afterFun(oldPo, session, request),     # 返回值将直接返回客户端，回滚数据库操作

        return JSONResponse
        """
        try:
            async with self.get_db_session(request) as session, session.begin():
                oldPo: poType = await session.get_one(poType, pk)
                if oldPo == None:
                    return JSON_util.response(Result.fail(message=f"未找到‘{pk}’对应的信息!"))
                if beforeFun != None:
                    result = await beforeFun(oldPo, session)
                    if result != None:
                        await session.rollback()
                        return result
                await session.delete(oldPo)
                if afterFun != None:
                    result = await afterFun(oldPo, session, request)
                    if result != None:
                        await session.rollback()
                        return result
                return JSON_util.response(Result.success())
        except Exception as e:
            await session.rollback()
            errorLog(request,self.__class__,get_current_function_name()) 
            return JSON_util.response(Result.fail(message=e))
    
    async def save_association(self, request: Request, currentUser:int,delSml:Delete,createPo:any,param:associationParam=None):
        """
        保存关联菜单
        delSml:Delete 删除语句
        createPo:(id)=>basePO
        """
        if param==None:
            param=associationParam()
            param.__dict__.update(request.json)   
        session:AsyncSession=self.get_db_session(request)
        callable=DbCallable(session) 
        async def exec(session:AsyncSession): 
            try: 
                isChanged=False
                # 移除
                if(param.remove!=None and len(param.remove)>0): 
                    result= await db_tools.execSQL(session,delSml)
                    if result>0:
                        isChanged=True
                # 增加
                if(param.add!=None and len(param.add)>0):
                    addpoList=[]
                    for id in param.add: 
                        po=await createPo(session,id)  
                        if isinstance(po, CreateUserStampedModelPO) or  isinstance(po,UserTimeStampedModelPO): 
                            po.createTime = datetime.now() 
                            po.createUser = currentUser 
                        addpoList.append(po)
                    if len(addpoList)>0:
                        isChanged=True
                        session.add_all(addpoList)  
                if isChanged: return JSON_util.response(Result.success())
                else:return JSON_util.response(Result.fail(message="未改变"))
            except Exception as e: 
                await session.rollback()
                return JSON_util.response(Result.fail(message=f"出现错误：{e}"))

        return await callable(exec) 



"""
class AuthMethodView(BaseMethodView): 
   decorators=[authorized] 


    def update():
         stmt = (
            Update(BoatGroupPO)
            .where(BoatGroupPO.groupType==Device_Group_type.site.key)
            .values(priority=99999)
        ) 
        return await session.execute(stmt) 
"""

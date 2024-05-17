import json
from urllib.parse import unquote

class MemoryService:
    def __init__(self, logger, portal_client):
        self.logger = logger
        self.portal_client = portal_client

    def retrieve_content_from_answer(self,content):
        '''处理历史消息中各式各样的markdown格式和json格式'''
        self.logger.info(f"retrieve_content_from_answer data:[{content}]")
        all_contents = ''
        try:
            data = json.loads(content)
            # 遍历列表，提取每个元素的content字段，并进行URL解码
            for item in data:
                content = unquote(item['content'])
                all_contents += content  # 添加换行符以区分不同内容
        except Exception as e:
            self.logger.error("加载历史消息时，发生%s异常", str(e), exc_info=True)
        return all_contents

    def retrieve_memory(self,session_id):
        self.logger.info(f'根据session_id[%s]从portal后端查询历史消息', session_id)
        portal_client = self.portal_client.get_value("portal_client")
        memories = []
        try:
            memory_resp = portal_client.get_chat_detail(session_id)
            self.logger.info(f'根据session_id[%s]从portal后端查询历史消息,结果为[%s]', session_id, memory_resp)
            if memory_resp is None or memory_resp.get("data") is None or memory_resp.get("data").get("conversation") is None:
                self.logger.info(f'根据session_id[%s]从portal后端查询历史消息为空，请检查参数', session_id)
                return []
            chat_info_list = memory_resp.get('data').get('conversation')
            num = 0
            memory_length = 0
            for i in range(0, len(chat_info_list) - 2, 2):
                chat_memory = []
                if chat_info_list[i]['text'] is not None and chat_info_list[i+1]['text'] is not None:
                    chat = chat_info_list[i]["text"]
                    chat = chat.replace("\\n", "\n")
                    chat_memory.append(chat)
                    content = self.retrieve_content_from_answer(chat_info_list[i+1]['text'])
                    content = content.replace("\\n", "\n")
                    chat_memory.append(content)
                    memories.append(chat_memory)
                num += 1
                if chat_memory is not None:
                    memory_length = memory_length + len(chat_memory)
                if num >= 20:
                    self.logger.info(f'当前历史对话轮数超过20轮,不再新增历史对话,session_id[{session_id}]')
                    break
                if memory_length >= 4000:
                    self.logger.info(f'当前历史对话字符长度超过4000,不再新增历史对话,session_id[{session_id}]')
                    break
        except Exception as e:
            self.logger.error("获取历史消息时，发生%s异常", str(e), exc_info=True)
        self.logger.info(f'retrieve_memory,session_id[{session_id}],return[{memories}]')
        return memories


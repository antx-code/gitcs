import asyncio
from pocx import AioPoc
from loguru import logger
import json
from conf import CONF


class GiteeCS(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(GiteeCS, self).__init__()
        self.name = 'Gitee Code Search'
        self.gitee_token = CONF['Gitee']

    @logger.catch(level='ERROR')
    async def ping(self):
        resp = await self.aio_get(
            f'https://gitee.com/api/v5/search/repositories?access_token={self.gitee_token}&q=%40baidu.com')
        if resp.status_code == 200:
            return True
        else:
            if resp.status_code == 401:
                logger.error('Gitee Token is invalid, please check your gitee Token.')
            return False

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        target = target.replace('@', '%40')
        search_content = target
        scopes = ['repositories', 'issues', 'users']
        results = {
            'repositories': [],
            'issues': [],
            'users': [],
        }
        ids = []
        page_num = 1
        per_page_num = 50
        limit_num = 500
        if not await self.ping():
            logger.success('Gitee module found 0 code related records.')
            return 0, []
        for scope in scopes:
            while True:
                base_url = f'https://gitee.com/api/v5/search/{scope}?access_token={self.gitee_token}&q={search_content}&page={page_num}&per_page={per_page_num}&order=desc'
                resp = await self.aio_get(base_url)
                if not resp:
                    break
                items = json.loads(resp.text)
                if not items:
                    break
                for item in items:
                    if item:
                        ids.append(item['id'])
                    results[scope].append(item)
                page_num += 1
                # 搜索条数限制
                if page_num * per_page_num > limit_num:
                    break
                await asyncio.sleep(0.5)
        total_count = len(ids)
        logger.success(f'Gitee module found {total_count} code related records.')
        return total_count, results

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    gitcs = GiteeCS()
    gitcs.run('target')
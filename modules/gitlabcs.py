import asyncio
from pocx import AioPoc
from loguru import logger
from gitlab import Gitlab, const
from conf import CONF


class GitlabCS(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(GitlabCS, self).__init__()
        self.name = 'Gitlab Code Search'
        self.gitlab_token = CONF['Gitlab']

    @logger.catch(level='ERROR')
    def ping(self):
        gl = Gitlab(private_token=self.gitlab_token)
        try:
            gl.auth()
            return True
        except Exception as e:
            if '401' in str(e):
                logger.error(f'Gitlab token is invalid.')
            return False

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        search_content = target
        results = {
            'projects': [],
            'issues': [],
            'merge_requests': [],
            'milestones': [],
            'wiki_blobs': [],
            'commits': [],
            'blobs': [],
            'users': [],
            'snippet_titles': [],
            'notes': [],
        }
        ids = []
        per_page_num = 10
        limit_num = 100
        gl = Gitlab(private_token=self.gitlab_token)
        if not self.ping():
            logger.success('Gitlab module found 0 code related records.')
            return 0, []
        for scope in const.SearchScope:
            page_num = 1
            for item in gl.search(scope, search_content, iterator=True):
                if item:
                    ids.append(item['id'])
                results[scope].append(item)
                page_num += 1
                # 搜索条数限制
                if page_num * per_page_num > limit_num:
                    break
                await asyncio.sleep(0.5)
        total_count = len(ids)
        logger.success(f'Gitlab module found {total_count} code related records.')
        return total_count, results

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    # https://docs.gitlab.com/ee/api/search.html
    # https://python-gitlab.readthedocs.io/en/stable/gl_objects/search.html
    gitcs = GitlabCS()
    gitcs.run('target')

import asyncio
from pocx import AioPoc
from loguru import logger
import json
from conf import CONF


class GithubCS(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        super(GithubCS, self).__init__()
        self.name = 'Github Code Search'
        self.github_token = CONF['Github']

    @logger.catch(level='ERROR')
    async def poc(self, target: str, is_detail: bool = False):
        target = target.replace('@', '%40')
        search_content = target
        results = []
        total_count = 0
        page_num = 1
        per_page_num = 100
        limit_num = 1000
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Aoyou/R0dwN2AqeFhWC2FdImhDMtYPbepzCaq2ExzA-PnBDq2QBC-jrWu35ZNZ',
            'Accept': 'application/vnd.github.v3.text-match+json',
            'Authorization': f"token {self.github_token}"
        }
        self.set_headers(headers=header)
        while True:
            url = f'https://api.github.com/search/code?q={search_content}&page={page_num}&per_page={per_page_num}&sort=indexed&order=desc'
            resp = await self.aio_get(url)
            if not resp:
                break
            if resp.status_code == 200:
                total_count = resp.json()['total_count']
                items = resp.json()['items']
                if not items:
                    break
                for item in items:
                    if is_detail:
                        rep = await self.aio_get(item['url'].split('?')[0])
                        try:
                            detail = json.loads(rep.text)
                            item['url_detail'] = detail
                            results.append(item)
                        except Exception as e:
                            logger.error(f'Github search detail got an error, error code: {resp.status_code}. Stop page: {page_num}, error detail url:{item["url"]}.')
                            break
                    else:
                        results.append(item)
            elif resp.status_code == 401:
                logger.error('Invalid github access token for credentials.')
                break
            else:
                logger.error(f'Github search code got an error, error code: {resp.status_code}. Stop page: {page_num}, error code url: {url}.')
                break
            page_num += 1
            # 搜索条数限制
            if page_num * per_page_num > limit_num:
                break
            await asyncio.sleep(1)
        logger.success(f'Github module found {total_count} code related records.')
        return total_count, results

    @logger.catch(level='ERROR')
    def dia(self, target: str):
        return asyncio.run(self.poc(target))


if __name__ == '__main__':
    # https://docs.github.com/en/rest/search#search-code
    gitcs = GithubCS()
    gitcs.run('target')

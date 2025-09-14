import asyncio
import aiohttp
import base64
import re
from typing import Set

async def fetch_url(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore, results: Set[str]):
    """异步获取单个URL的内容"""
    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    content = await response.text()
                    process_content(content, results)
                    print(f"Successfully processed: {url}")
                else:
                    print(f"Failed to fetch {url}: Status {response.status}")
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")

def process_content(content: str, results: Set[str]):
    """处理获取的内容"""
    content = content.strip()
    
    # 检查是否是Base64编码
    if re.match(r'^[A-Za-z0-9+/=]+$', content):
        try:
            # 尝试解码Base64
            decoded = base64.b64decode(content).decode('utf-8')
            lines = decoded.split('\n')
            for line in lines:
                line = line.strip()
                if line and line not in results:
                    results.add(line)
            return
        except:
            pass  # 如果不是有效的Base64，继续处理原始内容
    
    # 处理文本内容
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and line not in results:
            results.add(line)

async def main():
    """主函数，异步获取所有URL的内容"""
    # 从文件读取URL列表
    with open('urls.txt', 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"Found {len(urls)} URLs to process")
    
    # 限制并发数，避免过多请求
    semaphore = asyncio.Semaphore(5)  # 减少并发数以避免被限制
    results = set()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_url(session, url, semaphore, results))
            tasks.append(task)
        
        # 等待所有任务完成
        await asyncio.gather(*tasks)
    
    # 将去重后的内容写入文件
    with open('merged_subscriptions.txt', 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')
    
    print(f"完成! 共收集 {len(results)} 条唯一订阅信息")

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())

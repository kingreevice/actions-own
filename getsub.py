import requests
import base64
import asyncio
import aiohttp
import time
from typing import List, Set
import re

def load_urls_from_file(filename: str) -> List[str]:
    """从文件读取URL列表"""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# 用于去重的集合
unique_content: Set[str] = set()

async def fetch_url(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore):
    """异步获取单个URL的内容"""
    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    content = await response.text()
                    await process_content(content, url)
                else:
                    print(f"Failed to fetch {url}: Status {response.status}")
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")

async def process_content(content: str, url: str):
    """处理获取的内容"""
    # 检查是否是Base64编码
    if re.match(r'^[A-Za-z0-9+/=]+$', content.strip()):
        try:
            # 尝试解码Base64
            decoded = base64.b64decode(content).decode('utf-8')
            lines = decoded.split('\n')
            for line in lines:
                line = line.strip()
                if line and line not in unique_content:
                    unique_content.add(line)
        except:
            # 如果不是有效的Base64，直接使用原始内容
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and line not in unique_content:
                    unique_content.add(line)
    else:
        # 直接处理文本内容
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and line not in unique_content:
                unique_content.add(line)

async def main():
    """主函数，异步获取所有URL的内容"""
    # 从文件读取URL列表
    urls = load_urls_from_file('urls.txt')
    print(f"Found {len(urls)} URLs to process")
    
    # 限制并发数，避免过多请求
    semaphore = asyncio.Semaphore(10)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_url(session, url, semaphore))
            tasks.append(task)
        
        # 等待所有任务完成
        await asyncio.gather(*tasks)
    
    # 将去重后的内容写入文件
    with open('merged_subscriptions.txt', 'w', encoding='utf-8') as f:
        for line in unique_content:
            f.write(line + '\n')
    
    print(f"完成! 共收集 {len(unique_content)} 条唯一订阅信息")

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())

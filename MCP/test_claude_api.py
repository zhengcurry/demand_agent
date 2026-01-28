"""
Claude API测试脚本
使用Anthropic API接口
"""

import requests
import json
import sys
import io

# 设置标准输出为UTF-8编码，避免Windows控制台乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# API配置
API_URL = "http://172.16.40.227:3000/v1/messages"
API_KEY = "sk-KQOp0xA8cTk8bZf77cP79m74shnMYH8tPeMAURuWI4lzGhxb"
MODEL = "claude-sonnet-4-5-20250929"  # 可选: claude-3-5-sonnet-20241022, claude-opus-4-5-20251101


def test_chat_completion(prompt: str):
    """
    测试Claude聊天补全API

    Args:
        prompt: 用户输入的提示词
    """
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        print(f"发送请求到: {API_URL}")
        print(f"使用模型: {MODEL}")
        print(f"提示词: {prompt}\n")

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        # 检查响应状态
        response.raise_for_status()

        # 解析响应
        result = response.json()

        # 打印结果
        print("=" * 50)
        print("API响应成功!")
        print("=" * 50)

        if "content" in result and len(result["content"]) > 0:
            content = result["content"][0]["text"]
            print(f"\n回答:\n{content}\n")

            # 打印使用情况
            if "usage" in result:
                usage = result["usage"]
                print(f"Token使用情况:")
                print(f"  - 输入tokens: {usage.get('input_tokens', 'N/A')}")
                print(f"  - 输出tokens: {usage.get('output_tokens', 'N/A')}")
        else:
            print("响应格式异常:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
    except Exception as e:
        print(f"发生错误: {e}")


def test_streaming_chat(prompt: str):
    """
    测试Claude流式聊天API

    Args:
        prompt: 用户输入的提示词
    """
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.7,
        "stream": True
    }

    try:
        print(f"\n发送流式请求到: {API_URL}")
        print(f"使用模型: {MODEL}")
        print(f"提示词: {prompt}\n")

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        )

        response.raise_for_status()

        print("=" * 50)
        print("流式响应:")
        print("=" * 50)
        print()

        # 处理流式响应
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]  # 移除 'data: ' 前缀
                    if data == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data)
                        if chunk.get("type") == "content_block_delta":
                            delta = chunk.get("delta", {})
                            content = delta.get("text", "")
                            if content:
                                print(content, end='', flush=True)
                    except json.JSONDecodeError:
                        continue

        print("\n\n流式响应完成!")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    # 测试普通聊天补全
    print("测试1: 普通聊天补全")
    print("=" * 50)
    test_chat_completion("你好，请介绍一下你自己。")

    print("\n\n")

    # 测试流式聊天
    print("测试2: 流式聊天")
    print("=" * 50)
    test_streaming_chat("用Python写一个快速排序算法。")

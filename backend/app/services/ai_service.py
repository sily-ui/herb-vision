"""AI大模型调用服务模块（阶跃星辰 Step 3.7 Flash）"""
import base64
import json

import httpx

from app.config import settings

# 中药鉴定系统提示词
IDENTIFY_SYSTEM_PROMPT = """你是一位资深中药鉴定专家，精通《中国药典》标准。请根据图片识别该中药标本，按以下JSON格式输出（不要输出任何其他内容，只输出纯JSON）：
{
  "name": "药典标准名称",
  "aliases": "别名1,别名2",
  "family": "科属",
  "source": "来源（植物/动物/矿物及药用部位）",
  "nature_taste": "性味",
  "meridian_tropism": "归经",
  "efficacy": "功效",
  "indications": "主治",
  "usage_dosage": "用法用量",
  "contraindications": "禁忌",
  "appearance": {
    "color": "颜色",
    "texture": "质地",
    "fracture": "断面特征",
    "odor": "气味"
  },
  "authenticity_tips": "真伪鉴别要点，描述正品特征和常见伪品区别",
  "confusable_herbs": "易混淆药材1,易混淆药材2",
  "confidence": "高/中/低"
}

注意事项：
1. 严格按照中国药典标准描述，用词准确规范
2. 如无法确定具体品种，请给出最可能的判断并在confidence中标注"低"
3. 真伪鉴别要点要具体，便于实际操作
4. 易混淆药材要列出临床常见的混淆品种
5. 只输出JSON，不要添加任何解释文字"""

# 模糊搜索系统提示词
FUZZY_SEARCH_SYSTEM_PROMPT = """你是一位中药学专家。用户会描述一个中药的外观特征，请根据描述推断最可能的药材名称。
请按以下JSON格式输出（只输出纯JSON）：
{
  "results": [
    {"name": "药材名1", "confidence": 0.9, "reason": "匹配原因"},
    {"name": "药材名2", "confidence": 0.7, "reason": "匹配原因"},
    {"name": "药材名3", "confidence": 0.5, "reason": "匹配原因"}
  ]
}
最多返回5个最可能的药材，按置信度从高到低排列。只输出JSON，不要添加任何解释文字。"""


async def identify_herb(image_bytes: bytes) -> dict:
    """通过图片识别中药

    Args:
        image_bytes: 图片字节数据

    Returns:
        结构化识别结果字典
    """
    # 将图片转base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # 构建请求体（Step 3.7 Flash 多模态模型，兼容 OpenAI 格式）
    payload = {
        "model": settings.STEP_MODEL,
        "messages": [
            {
                "role": "system",
                "content": IDENTIFY_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                    {
                        "type": "text",
                        "text": "请识别图片中的中药标本",
                    },
                ],
            },
        ],
        "temperature": 0.1,
    }

    headers = {
        "Authorization": f"Bearer {settings.STEP_API_KEY}",
        "Content-Type": "application/json",
    }

    # 异步调用阶跃星辰API
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(settings.STEP_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

    # 解析返回结果
    content = result["choices"][0]["message"]["content"]

    # 尝试解析JSON
    try:
        # 去除可能的markdown代码块标记
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        identify_result = json.loads(content)
    except json.JSONDecodeError:
        identify_result = {"raw_response": content, "parse_error": True}

    return identify_result


AI_COMPARE_SYSTEM_PROMPT = """你是一位资深中药鉴定专家，精通《中国药典》标准。请对以下两种中药材进行专业对比分析，按以下JSON格式输出（不要输出任何其他内容，只输出纯JSON）：
{
  "summary": "一段话总结两者核心区别，便于快速辨识",
  "comparisons": [
    {
      "field": "外观特征",
      "field_en": "appearance",
      "herb1": "药材1的具体外观描述",
      "herb2": "药材2的具体外观描述",
      "difference": "两者的外观区别要点"
    },
    {
      "field": "质地断面",
      "field_en": "texture",
      "herb1": "药材1的质地断面描述",
      "herb2": "药材2的质地断面描述",
      "difference": "两者的质地断面区别要点"
    },
    {
      "field": "气味",
      "field_en": "odor",
      "herb1": "药材1的气味描述",
      "herb2": "药材2的气味描述",
      "difference": "两者的气味区别要点"
    },
    {
      "field": "功效主治",
      "field_en": "efficacy",
      "herb1": "药材1的功效主治",
      "herb2": "药材2的功效主治",
      "difference": "两者的功效主治区别要点"
    },
    {
      "field": "真伪鉴别",
      "field_en": "authenticity",
      "herb1": "药材1的真伪鉴别要点",
      "herb2": "药材2的真伪鉴别要点",
      "difference": "两者真伪鉴别上的区别要点"
    },
    {
      "field": "临床注意",
      "field_en": "clinical_notes",
      "herb1": "药材1的临床使用注意",
      "herb2": "药材2的临床使用注意",
      "difference": "两者临床使用上的区别注意"
    }
  ]
}

注意事项：
1. 严格按中国药典和临床常规表述，不要夸大疗效
2. 每个字段都要给出可操作的鉴别差异，不要写空泛套话
3. 如果某一字段信息不足，请写"暂无明确记载"
4. summary 控制在100字以内，直击要害
5. 只输出JSON，不要添加任何解释文字"""


async def ai_compare_herbs(herb1: dict, herb2: dict) -> dict:
    """调用大模型对两种药材进行智能对比

    Args:
        herb1: 药材1字典
        herb2: 药材2字典

    Returns:
        结构化对比结果字典
    """
    payload = {
        "model": settings.STEP_MODEL,
        "messages": [
            {
                "role": "system",
                "content": AI_COMPARE_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""请对以下两种中药材进行专业对比：

药材1：{herb1.get('name', '未知')}
- 来源：{herb1.get('source', '')}
- 性味：{herb1.get('nature_taste', '')}
- 归经：{herb1.get('meridian_tropism', '')}
- 功效：{herb1.get('efficacy', '')}
- 性状：颜色{herb1.get('appearance_color', '')}，质地{herb1.get('appearance_texture', '')}，断面{herb1.get('appearance_fracture', '')}，气味{herb1.get('appearance_odor', '')}
- 鉴别要点：{herb1.get('authenticity_tips', '')}
- 禁忌：{herb1.get('contraindications', '')}

药材2：{herb2.get('name', '未知')}
- 来源：{herb2.get('source', '')}
- 性味：{herb2.get('nature_taste', '')}
- 归经：{herb2.get('meridian_tropism', '')}
- 功效：{herb2.get('efficacy', '')}
- 性状：颜色{herb2.get('appearance_color', '')}，质地{herb2.get('appearance_texture', '')}，断面{herb2.get('appearance_fracture', '')}，气味{herb2.get('appearance_odor', '')}
- 鉴别要点：{herb2.get('authenticity_tips', '')}
- 禁忌：{herb2.get('contraindications', '')}""",
            },
        ],
        "temperature": 0.3,
    }

    headers = {
        "Authorization": f"Bearer {settings.STEP_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(settings.STEP_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()

        content = result["choices"][0]["message"]["content"]

        try:
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            compare_result = json.loads(content)
            return compare_result
        except json.JSONDecodeError:
            return {
                "summary": content[:200],
                "comparisons": [],
                "parse_error": True,
                "raw_response": content,
            }
    except httpx.HTTPStatusError as exc:
        return {
            "summary": f"大模型请求失败：{exc.response.status_code}",
            "comparisons": [],
            "error": True,
        }
    except Exception as exc:
        return {
            "summary": f"智能对比失败：{str(exc)}",
            "comparisons": [],
            "error": True,
        }


async def fuzzy_search_by_description(description: str) -> list:
    """通过外观描述模糊搜索药材

    Args:
        description: 用户描述的中药外观特征

    Returns:
        匹配的药材列表
    """
    payload = {
        "model": settings.STEP_MODEL,
        "messages": [
            {
                "role": "system",
                "content": FUZZY_SEARCH_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": description,
            },
        ],
        "temperature": 0.3,
    }

    headers = {
        "Authorization": f"Bearer {settings.STEP_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(settings.STEP_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

    content = result["choices"][0]["message"]["content"]

    try:
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        search_result = json.loads(content)
        return search_result.get("results", [])
    except json.JSONDecodeError:
        return []

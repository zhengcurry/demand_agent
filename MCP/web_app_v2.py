"""
飞书项目管理 - Web界面 V2
改进版：获取所有数据，支持完整筛选
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
from typing import List, Dict
import time

# 添加MCP目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'MCP'))

from get_view_workitems import get_view_detail, parse_view_response

app = Flask(__name__)

# 配置
VIEW_ID = "8SReqkNvg"
PROJECT_KEY = "662ef8e0b2b6c06ce1ef28db"

# 全局缓存
ALL_WORKITEMS = []
FILTER_OPTIONS = {
    'projects': [],
    'versions': [],
    'businesses': []
}
CACHE_LOADED = False
TOTAL_PAGES = 24  # 根据API响应，总共24页


def load_all_workitems():
    """
    加载所有页面的工作项数据
    """
    global ALL_WORKITEMS, FILTER_OPTIONS, CACHE_LOADED

    if CACHE_LOADED:
        return

    print("\n" + "=" * 80)
    print("正在加载所有工作项数据...")
    print("=" * 80)

    all_items = []

    # 循环获取所有页面
    for page in range(1, TOTAL_PAGES + 1):
        print(f"正在获取第 {page}/{TOTAL_PAGES} 页...")

        try:
            result = get_view_detail(view_id=VIEW_ID, page_num=page)

            if result:
                workitems = parse_view_response(result)
                all_items.extend(workitems)
                print(f"  ✓ 第 {page} 页: {len(workitems)} 条记录")
            else:
                print(f"  ✗ 第 {page} 页: 获取失败")

            # 避免请求过快
            time.sleep(0.5)

        except Exception as e:
            print(f"  ✗ 第 {page} 页出错: {e}")
            continue

    ALL_WORKITEMS = all_items

    # 提取筛选选项
    projects = sorted(set([
        item.get('field_c13a6c', '')
        for item in all_items
        if item.get('field_c13a6c')
    ]))

    versions = sorted(set([
        item.get('field_ab3f51', '')
        for item in all_items
        if item.get('field_ab3f51')
    ]))

    businesses = sorted(set([
        item.get('business', '')
        for item in all_items
        if item.get('business')
    ]))

    FILTER_OPTIONS = {
        'projects': projects,
        'versions': versions,
        'businesses': businesses
    }

    CACHE_LOADED = True

    print("=" * 80)
    print(f"✅ 数据加载完成!")
    print(f"   总记录数: {len(ALL_WORKITEMS)}")
    print(f"   项目数: {len(projects)}")
    print(f"   版本数: {len(versions)}")
    print(f"   业务线数: {len(businesses)}")
    print("=" * 80 + "\n")


def filter_workitems_server(
    workitems: List[Dict],
    project_filter: str = None,
    version_filter: str = None,
    business_filter: str = None
) -> List[Dict]:
    """
    在服务端对全部数据进行筛选

    Args:
        workitems: 全部工作项列表
        project_filter: 项目筛选条件
        version_filter: 版本筛选条件
        business_filter: 业务线筛选条件

    Returns:
        筛选后的工作项列表
    """
    filtered = workitems

    if project_filter:
        filtered = [
            item for item in filtered
            if project_filter.lower() in str(item.get('field_c13a6c', '')).lower()
        ]

    if version_filter:
        filtered = [
            item for item in filtered
            if version_filter.lower() in str(item.get('field_ab3f51', '')).lower()
        ]

    if business_filter:
        filtered = [
            item for item in filtered
            if business_filter.lower() in str(item.get('business', '')).lower()
        ]

    return filtered


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/api/workitems')
def get_workitems():
    """
    获取工作项列表API（改进版）

    参数:
        page: 前端分页页码（默认1）
        page_size: 每页显示数量（默认50）
        project: 项目筛选
        version: 版本筛选
        business: 业务线筛选
    """
    try:
        # 确保数据已加载
        if not CACHE_LOADED:
            load_all_workitems()

        # 获取参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 50))
        project_filter = request.args.get('project', '').strip()
        version_filter = request.args.get('version', '').strip()
        business_filter = request.args.get('business', '').strip()

        # 在全部数据上进行筛选
        filtered_items = filter_workitems_server(
            ALL_WORKITEMS,
            project_filter=project_filter if project_filter else None,
            version_filter=version_filter if version_filter else None,
            business_filter=business_filter if business_filter else None
        )

        # 计算分页
        total_items = len(filtered_items)
        total_pages = (total_items + page_size - 1) // page_size
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        # 获取当前页的数据
        page_items = filtered_items[start_idx:end_idx]

        return jsonify({
            'success': True,
            'data': {
                'workitems': page_items,
                'total': total_items,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        })


@app.route('/api/filter_options')
def get_filter_options():
    """
    获取所有筛选选项（从全部数据中提取）
    """
    try:
        # 确保数据已加载
        if not CACHE_LOADED:
            load_all_workitems()

        return jsonify({
            'success': True,
            'data': FILTER_OPTIONS
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        })


@app.route('/api/reload')
def reload_data():
    """
    重新加载数据
    """
    global CACHE_LOADED
    CACHE_LOADED = False

    try:
        load_all_workitems()

        return jsonify({
            'success': True,
            'message': f'数据重新加载成功，共 {len(ALL_WORKITEMS)} 条记录'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'重新加载失败: {str(e)}'
        })


@app.route('/api/workitem/<work_item_id>')
def get_workitem_detail(work_item_id):
    """
    获取单个工作项的详细信息

    参数:
        work_item_id: 工作项ID
    """
    try:
        # 确保数据已加载
        if not CACHE_LOADED:
            load_all_workitems()

        # 在缓存中查找工作项
        workitem = None
        for item in ALL_WORKITEMS:
            if str(item.get('work_item_id')) == str(work_item_id):
                workitem = item
                break

        if workitem:
            return jsonify({
                'success': True,
                'data': workitem
            })
        else:
            return jsonify({
                'success': False,
                'message': f'未找到工作项 ID: {work_item_id}'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        })


if __name__ == '__main__':
    print("=" * 80)
    print("飞书项目管理 - Web界面 V2")
    print("=" * 80)
    print(f"视图ID: {VIEW_ID}")
    print(f"项目Key: {PROJECT_KEY}")
    print(f"\n⚠️  首次启动会加载所有数据，请稍候...")
    print("=" * 80)

    # 启动时加载所有数据
    load_all_workitems()

    print("\n访问地址: http://127.0.0.1:5000")
    print("=" * 80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)

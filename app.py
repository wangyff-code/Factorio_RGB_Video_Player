# app.py
import webview
import json
from engine import get_video_info, gen_video_blueprint,get_preview_base64
import sys       # <--- 新增
import os        # <--- 新增
# ====== 新增：资源路径解析函数 ======
def get_resource_path(relative_path):
    """获取资源的绝对路径，兼容 PyInstaller 单文件打包模式"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的运行临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
# ==================================

class Api:
    def __init__(self):
        # 【关键修复】必须使用下划线 _window ！
        # 否则 pywebview 会尝试将整个底层操作系统窗口暴露给 JS，导致跨线程崩溃和无限递归死锁！
        self._window = None

    def select_file(self):
        """只负责打开文件对话框获取路径，绝不在此处理视频，防止卡死"""
        file_types = ('Video Files (*.mp4;*.mkv;*.avi;*.gif)', 'All files (*.*)')
        result = self._window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        
        if result and len(result) > 0:
            return result[0]  # 返回字符串路径
        return None
    
    def get_frame_preview(self, path, frame_idx):
        return get_preview_base64(path, frame_idx)

    def process_video(self, file_path):
        """前端显示加载动画后，调用此接口进行重负载视频分析"""
        info = get_video_info(file_path)
        if info["success"]:
            info["path"] = file_path
        return info

    def generate_blueprint(self, path, fps, start_frame, end_frame, frame_interval):
        """生成蓝图字符串"""
        try:
            fps = float(fps)
            start_frame = int(start_frame)
            end_frame = int(end_frame)
            frame_interval = int(frame_interval)
            
            # === 新增：进度回调函数 ===
            def progress_handler(percent, message):
                if self._window:
                    # 使用 JSON 转义确保字符串传给 JS 时不会引起引号冲突报错
                    safe_msg = json.dumps(message)
                    # 调用前端写好的 updateProgress(百分比, 提示文字)
                    self._window.evaluate_js(f"updateProgress({percent}, {safe_msg})")

            # 将回调传给引擎
            bp_string = gen_video_blueprint(
                path, fps, start_frame, end_frame, frame_interval,
                progress_callback=progress_handler
            )
            return {"success": True, "blueprint": bp_string}
        except Exception as e:
            return {"success": False, "error": str(e)}


def bind_drag_drop(window):
    """在网页加载完毕后绑定全局拖拽事件，由 Python 截获绝对路径"""
    try:
        from webview.dom import DOMEventHandler
        
        def on_drop(e):
            """当用户把视频拖拽进来时触发"""
            try:
                files = e.get("dataTransfer", {}).get("files", [])
                if len(files) > 0:
                    file_path = files[0].get("pywebviewFullPath")
                    if file_path:
                        # 转义路径中的反斜杠，并通知前端 JS 进入处理流程
                        safe_path = json.dumps(file_path)
                        window.evaluate_js(f"handleDroppedFile({safe_path})")
            except Exception as ex:
                print("Drop error:", ex)

        # 阻断浏览器默认行为（防止拖入视频时直接全屏播放视频）
        window.dom.document.events.dragover += DOMEventHandler(lambda e: None, True, True)
        window.dom.document.events.drop += DOMEventHandler(on_drop, True, True)
        window.dom.document.events.dragenter += DOMEventHandler(lambda e: None, True, True)
        window.dom.document.events.dragleave += DOMEventHandler(lambda e: None, True, True)
    except Exception as e:
        print("当前环境无法绑定拖拽事件 (推荐环境: pywebview>=5.0) :", e)


if __name__ == '__main__':
    api = Api()
    # 建立 pywebview 窗口
    html_path = get_resource_path('index.html')
    window = webview.create_window(
        'Factorio Video Blueprint Generator (异星工场视频蓝图生成器)', 
        html_path, 
        js_api=api, 
        width=950, 
        height=800,
        background_color='#1E1E1E',
        text_select=True
    )
    # 正确绑定内部 _window 对象
    api._window = window
    
    # 【关键修复2】确保在 HTML DOM 真正加载完成后，再绑定拖拽事件
    window.events.loaded += lambda: bind_drag_drop(window)
    
    # 启动应用
    webview.start(debug=False)
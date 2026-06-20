
# build.py
import PyInstaller.__main__
import os

if __name__ == '__main__':
    print("🚀 开始打包 异星工场视频蓝图生成器...")
    
    PyInstaller.__main__.run([
        'app.py',                           # 主入口文件
        '--name=Factorio_Video_Blueprint',  # 生成的 exe 名字
        '--windowed',                       # 隐藏控制台黑框 (GUI程序必备)
        '--onefile',                        # 打包成一个独立的 exe 文件
        '--add-data=index.html;.',          # 将 index.html 封装进 exe 里 (注意 Windows 是分号 ;)
        '--hidden-import=av',               # 强制引入 pyav (防 imageio 找不到解码器)
        '--hidden-import=imageio.plugins.pyav', # 同上
        '--clean',                          # 打包前清理临时文件
        '--copy-metadata=imageio',
        '--icon=output.ico',                 # 如果你有图标文件 app.ico，把这行注释取消掉
    ])
    
    print("\n✅ 打包完成！请在 dist 文件夹中查找 Factorio_Video_Blueprint.exe")
import sqlite3
import sys
import os
import subprocess

def init_db():
    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            name TEXT PRIMARY KEY,
            type TEXT,
            path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_command(name, cmd_type, path):
    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT OR REPLACE INTO commands (name, type, path) VALUES (?, ?, ?)',
                       (name, cmd_type, path))
        conn.commit()
        print(f'命令 {name} 创建成功')
    except Exception as e:
        print(f'创建命令失败: {str(e)}')
    finally:
        conn.close()

def execute_command(name):
    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT type, path FROM commands WHERE name = ?', (name,))
        result = cursor.fetchone()
        if result:
            cmd_type, path = result
            if cmd_type == 'app':
                subprocess.Popen(path)
                print(f'启动应用程序: {path}')
            elif cmd_type == 'cmd':
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        commands = f.readlines()
                    for cmd in commands:
                        cmd = cmd.strip()
                        if cmd:
                            print(f'执行命令: {cmd}')
                            subprocess.run(cmd, shell=True)
                else:
                    print(f'命令文件不存在: {path}')
        else:
            print(f'未找到命令: {name}')
    except Exception as e:
        print(f'执行命令失败: {str(e)}')
    finally:
        conn.close()

def main():
    init_db()
    
    if len(sys.argv) < 2:
        print('使用方法：')
        print('创建应用程序快捷方式: filec create <name> -app <path>')
        print('创建批处理命令: filec create <name> -cmd <path>')
        print('执行命令: filec <name>')
        print('显示作者信息: filec about')
        return

    if sys.argv[1] == 'about':
        print('作者：Rdtuetr')
        return

    if sys.argv[1] == 'create':
        if len(sys.argv) != 5:
            print('创建命令格式错误')
            return
        name = sys.argv[2]
        cmd_type = sys.argv[3].lstrip('-')
        path = sys.argv[4]
        create_command(name, cmd_type, path)
    else:
        name = sys.argv[1]
        execute_command(name)

if __name__ == '__main__':
    main()
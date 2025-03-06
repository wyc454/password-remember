'''使用过ai进行代码修改'''
import tkinter as tk
from tkinter import messagebox
import json
import os

class PasswordManage:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("密码管理器")
        self.window.geometry("400x300")

        # 存储数据的文件
        self.data_file = "passwords.json"
        self.accounts = self.load_data()

        # 创建界面元素
        tk.Label(self.window, text="网站/应用:").pack(pady=5)
        self.site_entry = tk.Entry(self.window)
        self.site_entry.pack()

        tk.Label(self.window, text="用户名:").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        tk.Label(self.window, text="密码:").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        # 按钮
        tk.Button(self.window, text="保存", command=self.save_account).pack(pady=10)
        tk.Button(self.window, text="查看所有账户", command=self.show_accounts).pack(pady=5)
        tk.Button(self.window, text="修改密码", command=self.modify_password).pack(pady=8)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.accounts, f)

    def save_account(self):
        site = self.site_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not all([site, username, password]):
            messagebox.showerror("错误", "请填写所有字段！")
            return

        if site not in self.accounts:
            self.accounts[site] = {}
        self.accounts[site][username] = password
        self.save_data()

        messagebox.showinfo("成功", "账户信息已保存！")
        self.clear_entries()

    def show_accounts(self):
        if not self.accounts:
            messagebox.showinfo("账户列表", "没有保存的账户")
            return

        account_window = tk.Toplevel(self.window)
        account_window.title("所有账户")
        account_window.geometry("300x400")

        text_widget = tk.Text(account_window)
        text_widget.pack(fill=tk.BOTH, expand=True)

        for site in self.accounts:
            text_widget.insert(tk.END, f"\n站点: {site}\n")
            for username, password in self.accounts[site].items():
                text_widget.insert(tk.END, f"用户名: {username}\n")
                text_widget.insert(tk.END, f"密码: {password}\n")
                text_widget.insert(tk.END, "-" * 20 + "\n")

        text_widget.config(state=tk.DISABLED)

    def clear_entries(self):
        self.site_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def modify_password(self):
        modify_window = tk.Toplevel(self.window)
        modify_window.title("修改密码")
        modify_window.geometry("300x200")

        tk.Label(modify_window, text="应用网站RR:").pack(pady=5)
        site_entry = tk.Entry(modify_window)
        site_entry.pack()

        tk.Label(modify_window, text="用户名:").pack(pady=5)
        username_entry = tk.Entry(modify_window)
        username_entry.pack()

        tk.Label(modify_window, text="新密码:").pack(pady=5)
        new_password_entry = tk.Entry(modify_window, show="*")
        new_password_entry.pack()

        def update_password():
            site = site_entry.get()
            username = username_entry.get()
            new_password = new_password_entry.get()

            if not all([site, username, new_password]):
                messagebox.showerror("错误", "请填写所有字段！")
                return

            if site not in self.accounts or username not in self.accounts[site]:
                messagebox.showerror("错误", "未找到该账户！")
                return

            self.accounts[site][username] = new_password
            self.save_data()
            messagebox.showinfo("成功", "密码已更新！")
            modify_window.destroy()

        tk.Button(modify_window, text="更新密码", command=update_password).pack(pady=10)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PasswordManage()
    app.run()
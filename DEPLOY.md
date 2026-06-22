# 部署说明

## 步骤1：创建GitHub仓库
1. 打开 https://github.com/new
2. 仓库名称输入：`food-picker`
3. 选择 **Public**（公开）
4. 点击 **Create repository**

## 步骤2：连接本地仓库
创建仓库后，复制仓库的URL（格式：https://github.com/你的用户名/food-picker.git），然后运行：

```bash
git remote add origin https://github.com/你的用户名/food-picker.git
git branch -M main
git push -u origin main
```

## 步骤3：启用GitHub Pages
1. 进入仓库 Settings
2. 左侧菜单选择 Pages
3. Source 选择 **Deploy from a branch**
4. Branch 选择 **main**，文件夹选择 **/ (root)**
5. 点击 Save

## 步骤4：访问你的网站
等待1-2分钟后，访问：`https://你的用户名.github.io/food-picker/`

---

## 首次推送代码更新
```bash
git add .
git commit -m "更新内容"
git push
```

# 张斌诚的个人博客

面向 GitHub 账号 BincZhang 的静态个人博客。包含首页、文章搜索、项目展示、关于页面、三篇文章、RSS 与手机布局。描述采用：我会是精英新生代，我努力翻江覆雨倒海。

## 发布到 GitHub Pages

1. 登录 **BincZhang**，创建公开仓库 **BincZhang.github.io**。
2. 将本文件夹内的文件和子目录上传至仓库根目录，`index.html` 应直接位于仓库根目录。不要只上传 ZIP 文件或把整个文件夹再嵌套一层。
3. Settings → Pages → Source 选择 Deploy from a branch；Branch 选择 main、/(root)，保存。
4. 等待 GitHub Pages 构建成功，访问 https://binczhang.github.io/ 。

项目不需要 npm、Ruby、Jekyll、数据库或访问密钥。`.nojekyll` 用于直接发布已生成的静态文件。

## 写文章

1. 在 content/ 中新增一个 Markdown 文件，可使用正文、`## 小标题`、`- 列表`、`**加粗**`、反引号代码和独占一行的 Markdown 图片。本生成器支持上述基础语法。
2. 在 site.json 的 posts 数组中增加标题、摘要、分类、日期、英文 slug 和文件路径。日期填写实际发布日期，新文章放在数组前面。
3. 在本目录运行 `python build.py`，上传更新后的文件到仓库。所有 HTML、RSS 和站点地图会重新生成。

修改姓名、描述、GitHub 用户名等信息时，编辑 site.json 后再次运行生成脚本。页面中的个人介绍与项目说明位于 build.py；颜色与排版位于 assets/style.css。

## 本地预览

在本目录运行 `python -m http.server 8765`，浏览器访问 http://localhost:8765 。也可直接双击 index.html，页面主要功能无需网络。

## 内容来源

成绩、荣誉与经历依据个人国奖答辩材料整理。学业成绩明确标注2025—2026学年；课程均分为答辩时数据。两张项目照片来自个人答辩PPT。未包含身份证号、学号、手机号或出生日期。

三篇初始文章是基于已有经历整理的第一人称稿件，发布前可按个人表达习惯修改。
